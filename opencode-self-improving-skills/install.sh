#!/usr/bin/env bash
# self-improving-skills for opencode —— 安装脚本
#
# 把插件 / 子代理 / 命令安装到 opencode 的配置目录。
# 用法:
#   ./install.sh             # 安装到全局 ~/.config/opencode/  （推荐，所有项目可用）
#   ./install.sh --project   # 安装到当前项目的 .opencode/      （仅本项目）
#   ./install.sh --uninstall # 从全局卸载（删符号链接）
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCOPE="global"
[[ "${1:-}" == "--project" ]] && SCOPE="project"
UNINSTALL=0
[[ "${1:-}" == "--uninstall" ]] && UNINSTALL=1

if [[ "$SCOPE" == "global" ]]; then
  DEST="${HOME}/.config/opencode"
else
  DEST="$(pwd)/.opencode"
fi

link_one() {  # <src-file> <dest-file>
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [[ "$UNINSTALL" == "1" ]]; then
    rm -f "$dst"; return
  fi
  ln -sfn "$src" "$dst"
  echo "  链接 $dst -> $src"
}

echo "[$SCOPE] 目标目录: $DEST"
if [[ "$UNINSTALL" == "1" ]]; then echo "卸载中..."; else echo "安装中(符号链接)..."; fi

# 插件（单个 ts 文件）
link_one "$SRC/plugin/self-improving-skills.ts" "$DEST/plugins/self-improving-skills.ts"

# 子代理
link_one "$SRC/agent/skill-distiller.md" "$DEST/agents/skill-distiller.md"

# 命令
for cmd in "$SRC"/commands/*.md; do
  link_one "$cmd" "$DEST/commands/$(basename "$cmd")"
done

# 建好状态目录（蒸馏技能与遥测会写入这里）
if [[ "$UNINSTALL" != "1" ]]; then
  mkdir -p "${HOME}/.config/opencode/skills" "${HOME}/.config/opencode/self-improve"
  echo "已确保存在 ~/.config/opencode/skills 和 ~/.config/opencode/self-improve"
fi

if [[ "$UNINSTALL" == "1" ]]; then
  echo "已卸载。学习技能(~/.config/opencode/skills)与遥测数据未删除。"
else
  echo "完成。请重启 opencode 使配置生效。"
fi
