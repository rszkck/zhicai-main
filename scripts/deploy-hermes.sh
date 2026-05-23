#!/usr/bin/env bash
# 将 zhicai·main 的 19 个 skill 部署到 Hermes
# 用法: bash scripts/deploy-hermes.sh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HERMES_DIR="$HOME/.hermes/skills"
SKILLS_DIR="$ROOT_DIR/skills"

echo "=========================================="
echo " zhicai → Hermes 一键部署"
echo " 源: $SKILLS_DIR"
echo " 目标: $HERMES_DIR"
echo "=========================================="

count=0
for skill_dir in "$SKILLS_DIR"/*/; do
    skill_name="$(basename "$skill_dir")"
    target="$HERMES_DIR/$skill_name"

    mkdir -p "$target"
    cp "$skill_dir/SKILL.md" "$target/SKILL.md"
    echo "  ✅ $skill_name → $target"
    ((count++))
done

echo ""
echo "=========================================="
echo " 部署完成: $count skills → $HERMES_DIR"
echo " 在 Hermes 中可用 skill_view() 加载"
echo "=========================================="
