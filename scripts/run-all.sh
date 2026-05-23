#!/usr/bin/env bash
# zhicai·main 完整管线 — 从原子提取到知识包生成再到构建
# 用法: bash scripts/run-all.sh [--skip-extract] [--build-only]
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "=========================================="
echo " zhicai·main 管线"
echo " 项目: $ROOT_DIR"
echo " 时间: $(date '+%Y-%m-%d %H:%M')"
echo "=========================================="

# 参数
SKIP_EXTRACT=false
BUILD_ONLY=false
for arg in "$@"; do
    case "$arg" in
        --skip-extract) SKIP_EXTRACT=true ;;
        --build-only) BUILD_ONLY=true ;;
    esac
done

if [ "$BUILD_ONLY" = true ]; then
    echo ""
    echo "[3/3] 构建 skill 包..."
    bash tools/build-skills.sh
    echo "✅ 完成"
    exit 0
fi

if [ "$SKIP_EXTRACT" = false ]; then
    echo ""
    echo "[1/3] 从 02-Wiki知识库 提取原子..."
    python3 scripts/extract-wiki-atoms.py
    echo "✅ wiki 原子提取完成"

    echo ""
    echo "[1.5/3] 从 01-原始资料 分析文件提取原子..."
    python3 scripts/extract-raw-analysis.py
    echo "✅ 原始资料原子提取完成"
else
    echo ""
    echo "[1/3] ⏭️ 跳过原子提取（--skip-extract）"
fi

echo ""
echo "[2/3] 从原子生成知识包..."
python3 scripts/generate-knowledge-packages.py
echo "✅ 知识包生成完成"

echo ""
echo "[3/3] 构建 skill 包..."
bash tools/build-skills.sh
echo "✅ 构建完成"

echo ""
echo "=========================================="
echo " 管线完成"
echo " 产物: dist/skills/zhicai-$(cat VERSION | tr -d '[:space:]').zip"
echo "=========================================="
