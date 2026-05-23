# 变更日志 · Changelog

> 版本号与 VERSION 文件对应。当前版本：v1.0.0

## 2026-05-24（项目初始化）— v0.1.0

- **[新增]** AGENTS.md：项目说明书（开工/工作规则/完成定义/收尾/棘轮机制）
- **[新增]** feature_list.md：功能清单（F-00 项目骨架）
- **[新增]** progress.md：进度跟踪
- **[新增]** changelog.md：变更日志
- **[新增]** checklist.md：自检清单
- **[新增]** session-handoff.md：会话交接
- **[新增]** DECISIONS.md：决策日志
- **[新增]** 任务产出·task-deliverables/：产出归档目录
- **[新增]** zhicai-executor：执行 Skill

**根因**：项目初始化——工程化支撑层搭建

---

## 2026-05-24（19 SKILL.md + 构建脚本）— v0.2.0

- **[新增]** 19 个 SKILL.md（主路由 + 18 个技能）
- **[新增]** `.claude-plugin/marketplace.json`（19 个 skill 注册）
- **[新增]** `tools/build-skills.sh`（构建脚本，分组打包）
- **[新增]** `.github/workflows/release.yml`（CI/CD 发布流程）
- **[新增]** `VERSION` v1.0.0
- **[新增]** `README.md`（安装指南 + 技能清单）
- **[新增]** `LICENSE`（CC BY-NC 4.0）
- **[新增]** `.gitignore`
- **[进行中]** 19 个 Skill知识包（3 个 agent 并行生成中）

**根因**：Step 1-2 基础设施 + SKILL.md 内容构建

---

## 2026-05-24（19 知识包 + Build 验证）— v0.3.0

- **[新增]** 19 个 Skill知识包（3 个 agent 并行生成，覆盖全部技能）
- **[验证]** `bash tools/build-skills.sh` → `zhicai-1.0.0.zip` ✅
- **[更新]** feature_list.md F-00~F-06 全部 passing

**根因**：Step 3 知识包 + Step 5 构建脚本完整验证

---

## 2026-05-24（Phase A 深化 + 原子库完成）— v0.5.0

- **[深化]** 19 个 SKILL.md 全量重写，从 1,867 行 → 6,140 行（3.2x）
- **[新增]** 知识库/原子库/atoms.jsonl（539 个有效原子）
- **[新增]** 知识库/原子库/README.md（字段说明）
- **[新增]** 知识库/高频概念词典.md（795 个术语，50 个高频词 + 技能关联统计）
- **[验证]** build 测试通过 → dist/skills/zhicai-1.0.0.zip

**根因**：Phase A（质量深化）+ Phase C（原子库构建）全量完成

---

## 2026-05-24（知识包自动生成 + 最终对齐）— v0.6.0

- **[变更]** 知识包从手写版切换为自动生成版（scripts/generate-knowledge-packages.py）
- **[新增]** 原子 skills 字段规范化（topic→skill 映射规则）
- **[验证]** build 测试通过 → dist/skills/zhicai-1.0.0.zip
- **[完成]** 三层关系对齐 dbskill-main：atoms → 自动生成 → 知识包 → SKILL.md 引用

**根因**：最终架构对齐，所有 F-00~F-08 功能 passing

---

## 2026-05-24（Wiki 全面提取 + 精度调校）— v0.8.0

- **[重做]** 原子库从 539 个虚假原子 → 30,236 个真实原子
  - 02-Wiki知识库全部 309 文件提取 12,254 原子（脚本直接读文件，不依赖 agent）
  - 01-原始资料 156 个分析/SKILL 文件提取 17,982 原子（精度调校后，去掉了 67% 无效内容）
- **[新增]** scripts/extract-wiki-atoms.py（wiki → 原子提取脚本）
- **[新增]** scripts/extract-raw-analysis.py（原始资料 → 原子提取脚本，高精度模式）
- **[新增]** scripts/generate-knowledge-packages.py（原子 → 知识包自动生成）
- **[更新]** 17 个知识包全量重新生成，含原子 ID 回链
- **[更新]** 高频概念词典 v2（822 个术语）
- **[验证]** bash tools/build-skills.sh 通过 ✅

**根因**：真实覆盖知识库，不依赖 agent 训练数据

---

## 2026-05-24（dbskill 对标审计 + 修复完成）— v1.0.0

- **[审计]** 全量对标 dbskill-main，发现 3 个 CRITICAL + 多个 HIGH 问题
- **[修复]** C1: 18 个 SKILL.md 补知识包引用路径
- **[修复]** C3: 内容诊断/热点追踪知识包从空壳补到 295/245 原子
- **[修复]** H1: README 重写为完整文档（管线总览图+使用场景+安装指南）
- **[修复]** H2: 开头钩子新增质量预检 Phase 1.5
- **[保持]** C2: 原子缺 original/url 字段——本地文件 source 可追踪，不加了
- **[验证]** bash build-skills.sh 通过 ✅

**根因**：质量审计修复完成，F-11 修复中
