#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-"$ROOT_DIR/dist/skills"}"
VERSION="$(tr -d '[:space:]' < "$ROOT_DIR/VERSION")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python3 command is required" >&2
  exit 1
fi

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

INNER_DIR="$(mktemp -d)"
trap 'rm -rf "$INNER_DIR"' EXIT

# skill 名 → 分组目录
group_for() {
  case "$1" in
    zhicai)
      echo "必装入口" ;;
    zhicai-全流程编排)
      echo "全流程" ;;
    zhicai-选题决策|zhicai-标题生成|zhicai-开头钩子|zhicai-叙事结构|zhicai-段落心法|zhicai-风格调校|zhicai-情感曲线|zhicai-结尾收束)
      echo "核心创作管线" ;;
    zhicai-心理学武器|zhicai-爆款预测|zhicai-大师写作法|zhicai-内容诊断|zhicai-AI去味)
      echo "内容增强" ;;
    zhicai-跨平台分发|zhicai-IP人设构建|zhicai-素材工坊|zhicai-热点追踪)
      echo "平台与IP" ;;
    *)
      echo "未分组" ;;
  esac
}

build_one() {
  local skill_dir="$1"
  local name
  local group
  local stage_dir
  local target_dir
  local refs

  name="$(basename "$skill_dir")"
  group="$(group_for "$name")"
  target_dir="$INNER_DIR/$group"
  mkdir -p "$target_dir"

  stage_dir="$(mktemp -d)"

  cp "$skill_dir/SKILL.md" "$stage_dir/SKILL.md"

  refs="$(grep -Eo '知识库/[^`,。 、)]*\.md' "$skill_dir/SKILL.md" || true)"
  if [ -n "$refs" ]; then
    while IFS= read -r ref; do
      [ -n "$ref" ] || continue
      if [ -f "$ROOT_DIR/$ref" ]; then
        mkdir -p "$stage_dir/$(dirname "$ref")"
        cp "$ROOT_DIR/$ref" "$stage_dir/$ref"
      fi
    done <<< "$refs"
  fi

  python3 - "$stage_dir" "$target_dir/${name}.zip" <<'PY'
import os
import sys
import zipfile

source_dir, archive_path = sys.argv[1], sys.argv[2]

with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for root, _, files in os.walk(source_dir):
        for filename in files:
            path = os.path.join(root, filename)
            archive.write(path, os.path.relpath(path, source_dir))
PY

  rm -rf "$stage_dir"
  echo "built $group/${name}.zip"
}

for skill_md in "$ROOT_DIR"/skills/*/SKILL.md; do
  build_one "$(dirname "$skill_md")"
done

cat > "$INNER_DIR/README.md" <<EOF
# zhicai ${VERSION}

一个 zip 装一个 skill。按使用场景分文件夹，把里面的 zip 逐个拖进「上传技能」窗口。

## 必装入口

- **zhicai** — 主入口，自动路由到合适的 skill。其他 skill 都依赖它。

## 全流程

- **zhicai-全流程编排** — 从选题到发布一站式创作工作流

## 核心创作管线

- **zhicai-选题决策** — 选题生成、验证与差异化升级
- **zhicai-标题生成** — 18 种标题公式库
- **zhicai-开头钩子** — 17 种开头钩子类型
- **zhicai-叙事结构** — 85 个叙事结构 S/A/B 三级匹配
- **zhicai-段落心法** — 段落技法、金句生成、过渡转折
- **zhicai-风格调校** — 四维语气控制、大师风格模仿
- **zhicai-情感曲线** — 6 种情感类型、5 种曲线模板
- **zhicai-结尾收束** — 7 种结尾类型、Peak-End 法则

## 内容增强

- **zhicai-心理学武器** — 27 个心理学原理全链路部署
- **zhicai-爆款预测** — BPI 爆款潜力指数、五维诊断
- **zhicai-大师写作法** — 30+ 位顶级创作者方法论
- **zhicai-内容诊断** — 10 大写作痛点诊断、瓶颈突破
- **zhicai-AI去味** — 29 种 AI 模式检测、增量去味

## 平台与 IP

- **zhicai-跨平台分发** — 6 种内容形式跨平台适配
- **zhicai-IP人设构建** — 6 种人设类型、信任构建
- **zhicai-素材工坊** — 卡片盒系统、创作 SOP
- **zhicai-热点追踪** — 热点捕捉、选题挖掘

---

每个 zip 解压后根级是 SKILL.md（带 YAML frontmatter，含 name + description），格式遵循 Anthropic Skills 规范。
EOF

python3 - "$INNER_DIR" "$OUT_DIR/zhicai-${VERSION}.zip" <<'PY'
import os
import sys
import zipfile

inner_dir, archive_path = sys.argv[1], sys.argv[2]

with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for root, _, files in os.walk(inner_dir):
        for filename in sorted(files):
            path = os.path.join(root, filename)
            archive.write(path, os.path.relpath(path, inner_dir))
PY

echo
echo "done: $OUT_DIR/zhicai-${VERSION}.zip"
