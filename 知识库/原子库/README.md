# 原子库说明

## 数据来源

- 来源：`知识库·内容创作者中心`（2738 个文件）
- 提取范围：100篇爆款分析报告、顶级创作者终极指南、写作框架完全指南、创作者技能文件、创作者分析报告
- 最终知识原子：539 个
- 生成日期：2026-05-24

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 格式：{来源}_{序号}，如 100_001、MASTER_042 |
| knowledge | string | 提炼后的知识点陈述句 |
| original | string | 原文（如果太长则截断） |
| source | string | 来源文件路径 |
| date | string | 提取日期 |
| topics | string[] | 主题标签 |
| skills | string[] | 关联 Skill |
| type | string | principle/method/data/insight/pattern |
| confidence | string | high/medium/low |

## 文件结构

- `atoms.jsonl` — 全量合并（539 条）
- `atoms_100篇分析.jsonl` — 100篇爆款合集分析报告（99 条）
- `atoms_大师终极指南.jsonl` — 顶级创作者终极指南（120 条）
- `atoms_写作框架.jsonl` — 写作框架完全指南（100 条）
- `atoms_创作者技能.jsonl` — 创作者技能文件（116 条）
- `atoms_创作者分析.jsonl` — 创作者分析报告（104 条）
