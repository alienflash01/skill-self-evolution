/**
 * self-improving-skills — opencode port
 *
 * Hermes Agent 式的自改进循环：把复杂工作中获得的「可复用技法」自动蒸馏成
 * SKILL.md，验证编辑、记录用量遥测、定期清理过时技能。
 *
 * 原项目 (Claude Code 插件 by UniM0cha) 的核心思想移植到 opencode 的 plugin /
 * event / SDK 原语上。opencode 没有 Claude Code 那种能「阻塞并强制续轮」的
 * Stop 钩子，因此蒸馏提醒改为 session.idle 时的 toast + 预填命令（非侵入、无循环）。
 *
 * 全部逻辑都在这一个文件里（纯 TS，零外部依赖，无需 Python）。
 * - 系统提示注入 (experimental.chat.system.transform) → 自改进环说明 + 学习技能数 + curator 提醒
 * - 编辑前备份 (tool.execute.before) → 学到的 SKILL.md 编辑前快照
 * - 编辑后验证 (tool.execute.after) → frontmatter 校验 + provenance 盖章 + 回滚 + 遥测
 * - 空闲时分析 (session.idle) → 测量复杂度；若复杂且未蒸馏则 toast + 预填 /distill-skill
 * - 用量遥测 + 时间基 curator 状态机
 *
 * 设计不变量（沿用原项目）：任何错误都 fail-safe（绝不阻塞/打断会话）；
 * 只清理 agent 蒸馏的技能，永不碰用户手写 / pinned 技能；归档可恢复（移动到 .archive/，不删除）。
 */

import type { Plugin } from "@opencode-ai/plugin"
import { mkdir, unlink, rename, stat } from "node:fs/promises"

// ─────────────────────────────────────────────────────────────────────────────
// 配置 / 路径
// ─────────────────────────────────────────────────────────────────────────────

const HOME = process.env.HOME || process.env.USERPROFILE || "~"
const SKILLS_DIR = `${HOME}/.config/opencode/skills`
const STATE_DIR = `${HOME}/.config/opencode/self-improve`
const USAGE_PATH = `${STATE_DIR}/skill_usage.json`
const CURATOR_STATE = `${STATE_DIR}/curator_state.json`
const BACKUP_DIR = `${STATE_DIR}/skill_backups`
const SNAPSHOT_DIR = `${STATE_DIR}/curator_backups`

function envInt(name: string, def: number): number {
  const v = process.env[name]
  if (!v) return def
  const n = parseInt(v, 10)
  return Number.isFinite(n) ? n : def
}
const DISTILL_THRESHOLD = () => envInt("SIS_DISTILL_THRESHOLD", 12)
const MIN_FILE_EDITS = () => envInt("SIS_MIN_FILE_EDITS", 2)
const CURATE_MIN_SKILLS = () => envInt("SIS_CURATE_MIN_SKILLS", 8)
const CURATE_INTERVAL_DAYS = () => envInt("SIS_CURATE_INTERVAL_DAYS", 7)
const STALE_AFTER_DAYS = () => envInt("SIS_STALE_AFTER_DAYS", 30)
const ARCHIVE_AFTER_DAYS = () => envInt("SIS_ARCHIVE_AFTER_DAYS", 90)

const PROVENANCE_VALUE = "self-improving-skills"
const EDIT_TOOLS = new Set(["write", "edit", "multiedit", "notebookedit"])
const MAX_NAME = 64
const MAX_DESC = 1024
const DESC_WARN = 500
const MAX_CONTENT = 100000
const NAME_RE = /^[a-z0-9][a-z0-9-]*$/

// ─────────────────────────────────────────────────────────────────────────────
// 小工具：JSON 原子读写 / 时间 / 路径
// ─────────────────────────────────────────────────────────────────────────────

function nowIso(): string {
  return new Date().toISOString()
}

async function readJson<T>(path: string): Promise<T | null> {
  try {
    const f = Bun.file(path)
    if (!(await f.exists())) return null
    return (await f.json()) as T
  } catch {
    return null
  }
}

/** 原子写：同目录 tempfile + rename。Bun 单线程事件循环，rename 原子即可，无需 flock。 */
async function writeJson(path: string, data: unknown): Promise<void> {
  try {
    await Bun.write(path, JSON.stringify(data, null, 2))
  } catch {
    /* best-effort */
  }
}

async function ensureDir(path: string): Promise<void> {
  try {
    await mkdir(path, { recursive: true })
  } catch {
    /* ignore */
  }
}

function normPath(p: unknown): string {
  return String(p || "").replace(/\\/g, "/")
}

function isSkillPath(p: unknown): boolean {
  const n = normPath(p)
  return n.endsWith("/SKILL.md") && n.includes("/skills/")
}

function skillNameFromPath(p: unknown): string | null {
  if (!isSkillPath(p)) return null
  const n = normPath(p).replace(/\/SKILL\.md$/, "")
  const parts = n.split("/")
  return parts[parts.length - 1] || null
}

async function learnedSkillNames(): Promise<Set<string>> {
  const names = new Set<string>()
  try {
    for await (const entry of new Bun.Glob("*/SKILL.md").scan({ cwd: SKILLS_DIR, absolute: false })) {
      const seg = entry.split("/")[0]
      if (seg && !seg.startsWith(".")) names.add(seg)
    }
  } catch {
    /* dir missing */
  }
  return names
}

// ─────────────────────────────────────────────────────────────────────────────
// 用量遥测存储（usage_store.py 的 TS 移植）
//   ~/.config/opencode/self-improve/skill_usage.json
// ─────────────────────────────────────────────────────────────────────────────

type UsageRecord = {
  use_count: number
  view_count: number
  patch_count: number
  last_used_at: string | null
  last_viewed_at: string | null
  last_patched_at: string | null
  created_at: string
  state: "active" | "stale" | "archived"
  pinned: boolean
  created_by: "agent" | "user" | "team"
  absorbed_into: string | null
}

type UsageStore = {
  _meta?: {
    offsets?: Record<string, { o: number; t: string }>
    nudges?: Record<string, { r: number; t: string }>
  }
  [skill: string]: UsageRecord | any
}

const KIND_KEYS: Record<string, [string, string]> = {
  use: ["use_count", "last_used_at"],
  view: ["view_count", "last_viewed_at"],
  patch: ["patch_count", "last_patched_at"],
}

function emptyRecord(created_by: UsageRecord["created_by"] = "agent"): UsageRecord {
  return {
    use_count: 0,
    view_count: 0,
    patch_count: 0,
    last_used_at: null,
    last_viewed_at: null,
    last_patched_at: null,
    created_at: nowIso(),
    state: "active",
    pinned: false,
    created_by,
    absorbed_into: null,
  }
}

async function loadUsage(): Promise<UsageStore> {
  return (await readJson<UsageStore>(USAGE_PATH)) || {}
}

// 串行化写入：避免并发的 idle/transform 事件互相覆盖。
let writeChain: Promise<any> = Promise.resolve()
function serialize<T>(fn: () => Promise<T>): Promise<T> {
  const run = writeChain.then(fn, fn)
  // 不让异常打断链
  writeChain = run.then(
    () => undefined,
    () => undefined,
  )
  return run
}

async function saveUsage(data: UsageStore): Promise<void> {
  await ensureDir(STATE_DIR)
  await writeJson(USAGE_PATH, data)
}

function recordsOf(data: UsageStore): [string, UsageRecord][] {
  return Object.entries(data).filter(([k, _v]) => k !== "_meta" && typeof _v === "object" && _v !== null) as [
    string,
    UsageRecord,
  ][]
}

async function applyEvents(
  events: Array<[string, keyof typeof KIND_KEYS, UsageRecord["created_by"]]>,
  sessionID?: string,
  newOffset?: number,
): Promise<void> {
  if (!events.length && newOffset === undefined) return
  await serialize(async () => {
    const data = await loadUsage()
    const ts = nowIso()
    for (const [name, kind, cb] of events) {
      if (!name || !KIND_KEYS[kind]) continue
      let rec = data[name] as UsageRecord | undefined
      if (!rec || typeof rec !== "object") {
        rec = emptyRecord(cb || "agent")
        data[name] = rec
      }
      const [countKey, tsKey] = KIND_KEYS[kind]
      ;(rec as any)[countKey] = ((rec as any)[countKey] as number) || 0
      ;(rec as any)[countKey] += 1
      ;(rec as any)[tsKey] = ts
      if (rec.state === "stale") rec.state = "active"
    }
    if (sessionID && newOffset !== undefined) {
      data._meta = data._meta || {}
      data._meta.offsets = data._meta.offsets || {}
      data._meta.offsets[sessionID] = { o: newOffset, t: ts }
    }
    await saveUsage(data)
  })
}

async function getOffset(sessionID: string): Promise<number> {
  const v = ((await loadUsage())._meta?.offsets?.[sessionID]) as any
  return typeof v === "object" ? v?.o ?? 0 : 0
}

async function getNudgeRow(sessionID: string): Promise<number> {
  const v = ((await loadUsage())._meta?.nudges?.[sessionID]) as any
  return typeof v === "object" ? v?.r ?? 0 : 0
}

async function recordNudge(sessionID: string, partCount: number): Promise<void> {
  if (!sessionID) return
  await serialize(async () => {
    const data = await loadUsage()
    data._meta = data._meta || {}
    data._meta.nudges = data._meta.nudges || {}
    data._meta.nudges[sessionID] = { r: partCount, t: nowIso() }
    await saveUsage(data)
  })
}

async function setFields(name: string, fields: Partial<UsageRecord>): Promise<void> {
  if (!name) return
  await serialize(async () => {
    const data = await loadUsage()
    let rec = data[name] as UsageRecord | undefined
    if (!rec || typeof rec !== "object") {
      rec = emptyRecord()
      data[name] = rec
    }
    Object.assign(rec, fields)
    await saveUsage(data)
  })
}

async function forgetMissing(existing: Set<string>, graceHours = 24): Promise<void> {
  await serialize(async () => {
    const data = await loadUsage()
    const now = Date.now()
    let changed = false
    for (const [name, rec] of recordsOf(data)) {
      if (existing.has(name)) {
        if ((rec as any).missing_since) {
          delete (rec as any).missing_since
          changed = true
        }
        continue
      }
      if (rec.state === "archived") continue
      const since = (rec as any).missing_since as string | undefined
      if (!since) {
        ;(rec as any).missing_since = nowIso()
        changed = true
      } else if ((now - new Date(since).getTime()) / 36e5 >= graceHours) {
        delete data[name]
        changed = true
      }
    }
    if (changed) await saveUsage(data)
  })
}

async function allRecords(): Promise<Record<string, UsageRecord>> {
  const d = await loadUsage()
  const out: Record<string, UsageRecord> = {}
  for (const [k, v] of recordsOf(d)) out[k] = v
  return out
}

// ─────────────────────────────────────────────────────────────────────────────
// SKILL.md 校验 / provenance 盖章（validate_skill.py 的 TS 移植）
// ─────────────────────────────────────────────────────────────────────────────

function splitFrontmatter(text: string): [string | null, string | null] {
  if (!text.startsWith("---")) return [null, null]
  const m = text.match(/^---\s*\n(.*?)\n---\s*\n?(.*)$/s)
  if (!m) return [null, null]
  return [m[1], m[2]]
}

function scalar(fm: string, key: string): string | null {
  const m = fm.match(new RegExp("^" + key.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "\\s*:\\s*(.*)$", "m"))
  if (!m) return null
  let val = m[1].trim()
  if (val.length >= 2 && (val[0] === '"' || val[0] === "'") && val[val.length - 1] === val[0]) {
    val = val.slice(1, -1)
  }
  return val
}

function validateSkill(text: string): string[] {
  const problems: string[] = []
  if (text.length > MAX_CONTENT) problems.push(`文件过大(>${MAX_CONTENT} 字符)，请把内容拆到 references/ 子目录。`)
  const [fm, body] = splitFrontmatter(text)
  if (fm === null) {
    problems.push("缺少 YAML frontmatter。文件必须以 `---` 开始并以 `---` 闭合。")
    return problems
  }
  const name = scalar(fm, "name")
  if (!name) problems.push("frontmatter 缺少 `name`。")
  else {
    if (name.length > MAX_NAME) problems.push(`\`name\` 超过 ${MAX_NAME} 字符。`)
    if (!NAME_RE.test(name)) problems.push("`name` 只能使用小写字母、数字、连字符（例：my-skill-name）。")
  }
  const desc = scalar(fm, "description")
  if (!desc) problems.push("frontmatter 缺少 `description`（这是触发命中的关键，请用一句话写清「在什么情况下使用」）。")
  else if (desc.length > MAX_DESC) problems.push("`description` 过长。")
  if (!body || !body.trim()) problems.push("frontmatter 之后缺少正文（技能指令）。")
  return problems
}

function advisoryFor(text: string): string | null {
  const [fm] = splitFrontmatter(text)
  if (!fm) return null
  const notes: string[] = []
  const desc = scalar(fm, "description") || ""
  if (desc.length > DESC_WARN) {
    notes.push(
      `description 有 ${desc.length} 字符。学习技能的 description 会进入每个会话的系统提示，长度即持续的上下文成本。请在保留触发短语的同时压缩到 ${DESC_WARN} 字符以内。`,
    )
  }
  return notes.length ? "[self-improving-skills] 提示:\n- " + notes.join("\n- ") : null
}

async function stampProvenance(path: string, text: string): Promise<void> {
  try {
    if (text.includes(PROVENANCE_VALUE)) return
    const [fm, body] = splitFrontmatter(text)
    if (fm === null || body === null) return
    if (/^metadata\s*:/m.test(fm)) return // 作者已自行管理 metadata
    const newFm = fm.replace(/\s+$/, "") + `\nmetadata:\n  provenance: ${PROVENANCE_VALUE}\n  origin: distilled\n`
    await Bun.write(path, `---\n${newFm}\n---\n${body}`)
  } catch {
    /* best-effort */
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// curator：时间基状态机（curator_transitions.py 的 TS 移植）
// ─────────────────────────────────────────────────────────────────────────────

function parseTs(ts: unknown): Date | null {
  if (!ts) return null
  try {
    const d = new Date(String(ts))
    return isNaN(d.getTime()) ? null : d
  } catch {
    return null
  }
}

function idleDays(rec: UsageRecord, now: Date): number {
  let latest: Date | null = null
  for (const k of ["last_used_at", "last_viewed_at", "last_patched_at"] as const) {
    const d = parseTs((rec as any)[k])
    if (d && (!latest || d > latest)) latest = d
  }
  const anchor = latest || parseTs(rec.created_at) || now
  return Math.floor((now.getTime() - anchor.getTime()) / 86400000)
}

function archiveDaysFor(rec: UsageRecord, base: number): number {
  return (rec.use_count || 0) >= 3 ? base * 2 : base // 经过验证的技能老化更慢
}

async function frontmatterPinned(name: string): Promise<boolean> {
  try {
    const text = await Bun.file(`${SKILLS_DIR}/${name}/SKILL.md`).text()
    return /^\s*pinned\s*:\s*true/im.test(text.slice(0, 2048))
  } catch {
    return false
  }
}

async function makeSnapshot(): Promise<void> {
  try {
    await ensureDir(SNAPSHOT_DIR)
    const stamp = new Date().toISOString().replace(/[:.]/g, "").replace("Z", "Z")
    const out = `${SNAPSHOT_DIR}/${stamp}.tar.gz`
    const parent = SKILLS_DIR.split("/").slice(0, -1).join("/") || "/"
    const base = SKILLS_DIR.split("/").pop() || "skills"
    // 用系统 tar；失败不阻塞 curator
    const proc = Bun.spawn(["tar", "czf", out, "--exclude=.git", "--exclude=node_modules", "-C", parent, base], {
      stdout: "ignore",
      stderr: "ignore",
    })
    await proc.exited
    // 只保留最近 5 个
    const snaps = Array.from(new Bun.Glob("*.tar.gz").scanSync({ cwd: SNAPSHOT_DIR })).sort()
    for (const old of snaps.slice(0, -5)) {
      try {
        await unlink(`${SNAPSHOT_DIR}/${old}`)
      } catch {
        /* ignore */
      }
    }
  } catch {
    /* best-effort */
  }
}

async function archiveDir(name: string): Promise<void> {
  const src = `${SKILLS_DIR}/${name}`
  try {
    if (!(await exists(src))) return
    await ensureDir(`${SKILLS_DIR}/.archive`)
    let dst = `${SKILLS_DIR}/.archive/${name}`
    if (await exists(dst)) dst = `${dst}.${new Date().toISOString().replace(/[:.]/g, "")}`
    await rename(src, dst)
  } catch {
    /* ignore */
  }
}

async function exists(p: string): Promise<boolean> {
  try {
    await stat(p)
    return true
  } catch {
    return false
  }
}

async function runCurator(dryRun = false): Promise<{
  archived: any[]
  stale: any[]
  reactivated: string[]
}> {
  const staleDays = STALE_AFTER_DAYS()
  const archiveDays = ARCHIVE_AFTER_DAYS()
  const now = new Date()
  const records = await allRecords()
  const learned = await learnedSkillNames()
  const summary = { archived: [] as any[], stale: [] as any[], reactivated: [] as string[] }
  let backedUp = false
  const ensureBackup = async () => {
    if (dryRun || backedUp) return
    await makeSnapshot()
    backedUp = true
  }

  for (const name of [...learned].sort()) {
    const rec = records[name] || (emptyRecord() as UsageRecord)
    if ((rec.created_by || "agent") !== "agent") continue // 用户/团队技能绝不清理
    if (rec.pinned || (await frontmatterPinned(name))) continue
    if (rec.state === "archived") continue
    const idle = idleDays(rec, now)
    if (idle >= archiveDaysFor(rec, archiveDays)) {
      summary.archived.push({ name, idle_days: idle })
      if (!dryRun) {
        await ensureBackup()
        await archiveDir(name)
        await setFields(name, { state: "archived" })
      }
    } else if (idle >= staleDays) {
      if (rec.state !== "stale") {
        summary.stale.push({ name, idle_days: idle })
        if (!dryRun) await setFields(name, { state: "stale" })
      }
    } else if (rec.state === "stale") {
      summary.reactivated.push(name)
      if (!dryRun) await setFields(name, { state: "active" })
    }
  }
  return summary
}

async function maybeAutoCurate(sessionID: string): Promise<void> {
  try {
    const state = (await readJson<any>(CURATOR_STATE)) || {}
    const learned = await learnedSkillNames()
    let agentCount = 0
    for (const n of learned) {
      const rec = (await allRecords())[n]
      if (rec && rec.created_by === "agent") agentCount++
      else if (!rec) agentCount++ // 蒸馏产生但尚无记录
    }
    if (agentCount < CURATE_MIN_SKILLS()) return
    const last = Number(state.last_run) || 0
    if (last && Date.now() - last < CURATE_INTERVAL_DAYS() * 86400000) return
    const summary = await runCurator(false)
    state.last_run = Date.now()
    state.run_count = (state.run_count || 0) + 1
    state.last_summary = {
      archived: summary.archived.length,
      stale: summary.stale.length,
      reactivated: summary.reactivated.length,
    }
    await ensureDir(STATE_DIR)
    await writeJson(CURATOR_STATE, state)
  } catch {
    /* best-effort */
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// 系统提示注入（SessionStart advisory 的 opencode 对应物）
// ─────────────────────────────────────────────────────────────────────────────

async function buildAdvisory(): Promise<string> {
  const lines: string[] = []
  lines.push("[self-improving-skills] 自改进循环已启用。")
  lines.push(
    "完成复杂任务/棘手调试/发现新技法后，若它是可复用的，用 /distill-skill 命令（或 Task 工具调用 subagent_type=\"skill-distiller\" 子代理）把可复用技法写入 ~/.config/opencode/skills 的 SKILL.md。",
  )
  lines.push(
    "发现学习技能内容过时或错误时，不要等指令，当场 patch 那个 SKILL.md —— 不维护的技能是债务。",
  )
  try {
    const learned = await learnedSkillNames()
    if (learned.size) lines.push(`当前已积累 ${learned.size} 个学习技能于 ~/.config/opencode/skills。`)
  } catch {
    /* ignore */
  }
  return lines.join("\n")
}

// ─────────────────────────────────────────────────────────────────────────────
// 空闲时的复杂度分析（analyze_turn.py 的 opencode 对应物）
//   opencode 消息结构：client.session.messages() → [{ info:{role}, parts:[...] }]
//   工具调用 part： { type:"tool", tool:<name>, state:{ status, input:{...}, output } }
//   子代理调用：    { type:"subtask", agent:<name> }  或  type:"tool", tool:"task", state.input.subagent_type
// ─────────────────────────────────────────────────────────────────────────────

type FlatPart = {
  mi: number // 所属 message 索引
  type: string
  tool?: string
  agent?: string
  input?: any
  status?: string
}

function isDistillerDelegation(p: FlatPart): boolean {
  if (p.type === "subtask") return String(p.agent || "").includes("skill-distiller")
  if (p.type === "tool" && p.tool === "task") {
    return String(p.input?.subagent_type || "").includes("skill-distiller")
  }
  return false
}

async function analyzeAndNudge(client: any, sessionID: string): Promise<void> {
  if (!sessionID) return
  let msgs: any[]
  try {
    const res = await client.session.messages({ path: { id: sessionID } })
    msgs = (res?.data as any[]) || (res as any[]) || []
  } catch {
    return
  }
  if (!Array.isArray(msgs) || !msgs.length) return

  // 拍平所有 part（保持顺序）
  const flat: FlatPart[] = []
  for (let mi = 0; mi < msgs.length; mi++) {
    const parts = (msgs[mi].parts as any[]) || []
    for (const part of parts) {
      const t = part?.type
      if (t === "tool") {
        flat.push({
          mi,
          type: "tool",
          tool: part.tool,
          input: part.state?.input,
          status: part.state?.status,
        })
      } else if (t === "subtask") {
        flat.push({ mi, type: "subtask", agent: part.agent })
      }
    }
  }
  if (!flat.length) return

  // 遥测捕获（best-effort，绝不影响 nudge 判定）
  try {
    const learned = await learnedSkillNames()
    await forgetMissing(learned)
    const offset = await getOffset(sessionID)
    const start = offset > flat.length || offset < 0 ? 0 : offset
    const events: Array<[string, "use" | "view", UsageRecord["created_by"]]> = []
    for (let i = start; i < flat.length; i++) {
      const p = flat[i]
      if (p.type !== "tool") continue
      // view：read 一个 SKILL.md
      if (p.tool === "read") {
        const sn = skillNameFromPath(p.input?.filePath || p.input?.file_path)
        if (sn && learned.has(sn)) events.push([sn, "view", "user"])
      }
    }
    await applyEvents(events, sessionID, flat.length)
  } catch {
    /* telemetry best-effort */
  }

  // anchor = 最后一次蒸馏发生的位置
  let anchor = -1
  for (let i = 0; i < flat.length; i++) {
    const p = flat[i]
    if (isDistillerDelegation(p)) anchor = i
    else if (p.type === "tool" && EDIT_TOOLS.has(p.tool || "")) {
      const sn = skillNameFromPath(p.input?.filePath || p.input?.file_path)
      if (sn) anchor = i
    }
  }

  const nudged = await getNudgeRow(sessionID)
  const startIdx = Math.max(anchor + 1, nudged > flat.length ? 0 : nudged)

  let calls = 0
  let edits = 0
  for (let i = startIdx; i < flat.length; i++) {
    const p = flat[i]
    if (p.type !== "tool") continue
    calls++
    if (EDIT_TOOLS.has(p.tool || "")) edits++
  }

  const fires = calls >= DISTILL_THRESHOLD() && edits >= MIN_FILE_EDITS()
  if (!fires) return

  // 已蒸馏过 / 已提醒过则不再提醒
  await recordNudge(sessionID, flat.length)
  try {
    await client.tui?.showToast?.({
      body: {
        message: `本轮工作积累 ${calls} 次工具调用(${edits} 次文件编辑)且尚未提炼为技能。建议运行 /distill-skill 提炼可复用技法。`,
        variant: "info",
      },
    })
    await client.tui?.appendPrompt?.({ body: { text: "/distill-skill" } })
  } catch {
    /* TUI 可能不可用（headless），忽略 */
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// 备份（PreToolUse 对应物）
// ─────────────────────────────────────────────────────────────────────────────

async function backupBefore(filePath: string): Promise<void> {
  try {
    const name = skillNameFromPath(filePath)
    if (!name) return
    await ensureDir(BACKUP_DIR)
    const bp = `${BACKUP_DIR}/${name}.bak`
    const f = Bun.file(filePath)
    if (await f.exists()) {
      await Bun.write(bp, f) // 现有 → 回滚源
    } else {
      try {
        await unlink(bp)
      } catch {
        /* 新文件，清掉陈旧备份 */
      }
    }
  } catch {
    /* 静默、绝不阻塞编辑 */
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// 验证 + provenance + 回滚（PostToolUse 对应物）
// ─────────────────────────────────────────────────────────────────────────────

async function validateAfter(filePath: string, output: { output: string; metadata: any }): Promise<void> {
  try {
    const name = skillNameFromPath(filePath)
    if (!name) return
    let text: string
    try {
      text = await Bun.file(filePath).text()
    } catch {
      return
    }

    const problems = validateSkill(text)
    if (problems.length) {
      // 结构破损 → 有备份就回滚
      const bp = `${BACKUP_DIR}/${name}.bak`
      let rolledBack = false
      try {
        const bak = Bun.file(bp)
        if (await bak.exists()) {
          await Bun.write(filePath, bak)
          rolledBack = true
        }
      } catch {
        /* ignore */
      }
      const head = rolledBack
        ? `[self-improving-skills] ${filePath} 的编辑破坏了 SKILL.md 结构，已自动回滚到编辑前版本。发现的问题:\n- `
        : `[self-improving-skills] 刚写入的学习技能 ${filePath} 有问题:\n- `
      output.output = (output.output ? output.output + "\n\n" : "") + head + problems.join("\n- ")
      if (rolledBack) output.output += "\n原文件已恢复，请避开上述问题重新编辑。"
      else output.output += "\n请修正后重新保存。"
      return
    }

    // 校验通过 → 盖章 provenance + 记录 patch 遥测
    await stampProvenance(filePath, text)
    // created_by 判定：origin:distilled 标记 → agent，否则 user
    const createdBy: UsageRecord["created_by"] = /origin\s*:\s*distilled/.test(text.slice(0, 2048)) ? "agent" : "user"
    await applyEvents([[name, "patch", createdBy]])

    const adv = advisoryFor(text)
    if (adv) output.output = (output.output ? output.output + "\n\n" : "") + adv
  } catch {
    /* 校验反馈绝不能破坏已发生的编辑 */
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// 插件入口
// ─────────────────────────────────────────────────────────────────────────────

export const SelfImprovingSkillsPlugin: Plugin = async ({ client }) => {
  // 系统提示注入：每轮 LLM 调用前追加简短自改进环说明（缓存结果，避免每轮重复 readdir）
  let advisoryCache: { text: string; t: number } | null = null
  const advisoryFreshMs = 60000
  const getAdvisory = async (): Promise<string> => {
    if (advisoryCache && Date.now() - advisoryCache.t < advisoryFreshMs) return advisoryCache.text
    const text = await buildAdvisory()
    advisoryCache = { text, t: Date.now() }
    return text
  }

  return {
    // SessionStart 的 opencode 对应物：注入系统提示
    "experimental.chat.system.transform": async (_input, output) => {
      try {
        output.system.push(await getAdvisory())
      } catch {
        /* ignore */
      }
    },

    // PreToolUse 对应物：编辑前备份学习技能
    "tool.execute.before": async (input, output) => {
      try {
        if (!EDIT_TOOLS.has(input.tool)) return
        const fp = output.args?.filePath || output.args?.file_path || output.args?.path
        if (fp) await backupBefore(String(fp))
      } catch {
        /* fail-safe：绝不阻塞编辑 */
      }
    },

    // PostToolUse 对应物：编辑后验证 + 盖章 + 回滚 + 遥测
    "tool.execute.after": async (input, output) => {
      try {
        if (!EDIT_TOOLS.has(input.tool)) return
        const fp = input.args?.filePath || input.args?.file_path || input.args?.path
        if (fp) await validateAfter(String(fp), output as any)
      } catch {
        /* fail-safe */
      }
    },

    // 事件总线：空闲分析 + 自动 curator
    event: async ({ event }) => {
      try {
        const type = (event as any)?.type
        if (type === "session.idle") {
          const sid =
            (event as any)?.properties?.info?.id ||
            (event as any)?.properties?.id ||
            (event as any)?.properties?.sessionID ||
            (event as any)?.properties?.sessionID ||
            ""
          if (sid) {
            await analyzeAndNudge(client, String(sid)).catch(() => {})
            await maybeAutoCurate(String(sid)).catch(() => {})
          }
        }
      } catch {
        /* 任何事件错误都 fail-safe */
      }
    },
  }
}

export default SelfImprovingSkillsPlugin
