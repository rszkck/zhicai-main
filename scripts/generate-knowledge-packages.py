#!/usr/bin/env python3
"""
从 atoms.jsonl 自动生成 Skill知识包。
对标 dbskill-main 的「自动生成」模式。

用法：python3 scripts/generate-knowledge-packages.py
"""

import json
import os
from collections import defaultdict

ATOMS_PATH = os.path.join(os.path.dirname(__file__), '..', '知识库', '原子库', 'atoms.jsonl')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '知识库', 'Skill知识包')

# 模块代码前缀 → skill 映射（最高优先级）
MODULE_TO_SKILL = {
    '00-总纲': 'zhicai-全流程编排',
    '01-选题系统': 'zhicai-选题决策',
    '02-标题公式库': 'zhicai-标题生成',
    '03-开头钩子': 'zhicai-开头钩子',
    '04-叙事结构': 'zhicai-叙事结构',
    '05-段落心法': 'zhicai-段落心法',
    '06-语言风格': 'zhicai-风格调校',
    '07-情感曲线': 'zhicai-情感曲线',
    '08-结尾收束': 'zhicai-结尾收束',
    '09-心理学武器': 'zhicai-心理学武器',
    '10-爆款预测': 'zhicai-爆款预测',
    '11-大师案例库': 'zhicai-大师写作法',
    '12-账号风格库': 'zhicai-跨平台分发',
    '13-IP人设与信任构建': 'zhicai-IP人设构建',
    'AI去味': 'zhicai-AI去味',  # 无独立模块，从旧原子补
    '去AI味': 'zhicai-AI去味',
    'humanizer': 'zhicai-AI去味',
    'AI': 'zhicai-AI去味',
    '诊断': 'zhicai-内容诊断',  # 无独立模块
    '瓶颈': 'zhicai-内容诊断',
    '热点': 'zhicai-热点追踪',  # 无独立模块
    '素材': 'zhicai-素材工坊',  # 无独立模块
    'SOP': 'zhicai-素材工坊',
    '大师': 'zhicai-大师写作法',
    '写作技巧': 'zhicai-大师写作法',
}

# 主题 → skill 映射规则（次要优先级）
TOPIC_TO_SKILL = {
    '选题': 'zhicai-选题决策',
    '选题系统': 'zhicai-选题决策',
    '选题验证': 'zhicai-选题决策',
    '标题': 'zhicai-标题生成',
    '标题公式': 'zhicai-标题生成',
    '开头': 'zhicai-开头钩子',
    '钩子': 'zhicai-开头钩子',
    '叙事结构': 'zhicai-叙事结构',
    '结构': 'zhicai-叙事结构',
    '文章结构': 'zhicai-叙事结构',
    '写作框架': 'zhicai-叙事结构',
    '框架': 'zhicai-叙事结构',
    '段落': 'zhicai-段落心法',
    '金句': 'zhicai-段落心法',
    '过渡': 'zhicai-段落心法',
    '语言风格': 'zhicai-风格调校',
    '写作风格': 'zhicai-风格调校',
    '风格': 'zhicai-风格调校',
    '语气': 'zhicai-风格调校',
    '情感': 'zhicai-情感曲线',
    '情绪': 'zhicai-情感曲线',
    '结尾': 'zhicai-结尾收束',
    '收尾': 'zhicai-结尾收束',
    'CTA': 'zhicai-结尾收束',
    '心理学': 'zhicai-心理学武器',
    '说服': 'zhicai-心理学武器',
    '影响力': 'zhicai-心理学武器',
    '认知偏误': 'zhicai-心理学武器',
    '爆款': 'zhicai-爆款预测',
    'BPI': 'zhicai-爆款预测',
    '预测': 'zhicai-爆款预测',
    '大师': 'zhicai-大师写作法',
    '写作技巧': 'zhicai-大师写作法',
    '创作哲学': 'zhicai-大师写作法',
    '写作理念': 'zhicai-大师写作法',
    '方法论': 'zhicai-全流程编排',
    '创作流程': 'zhicai-全流程编排',
    'SOP': 'zhicai-素材工坊',
    '素材': 'zhicai-素材工坊',
    '卡片盒': 'zhicai-素材工坊',
    '灵感': 'zhicai-素材工坊',
    '小红书': 'zhicai-跨平台分发',
    '短视频': 'zhicai-跨平台分发',
    '公众号': 'zhicai-跨平台分发',
    '平台': 'zhicai-跨平台分发',
    '跨平台': 'zhicai-跨平台分发',
    'IP': 'zhicai-IP人设构建',
    '人设': 'zhicai-IP人设构建',
    '个人品牌': 'zhicai-IP人设构建',
    '信任': 'zhicai-IP人设构建',
    '热点': 'zhicai-热点追踪',
    '借势': 'zhicai-热点追踪',
    '去AI味': 'zhicai-AI去味',
    'AI': 'zhicai-AI去味',
    'humanizer': 'zhicai-AI去味',
    '诊断': 'zhicai-内容诊断',
    '瓶颈': 'zhicai-内容诊断',
    '写作困难': 'zhicai-内容诊断',
    '卡兹克': 'zhicai-大师写作法',
    '粥左罗': 'zhicai-大师写作法',
    '新世相': 'zhicai-大师写作法',
    '工具': 'zhicai-全流程编排',
    '工具箱': 'zhicai-全流程编排',
    '数据': 'zhicai-爆款预测',
    '变现': 'zhicai-全流程编排',
}

# 技能中文名
SKILL_CN = {
    'zhicai': '主路由',
    'zhicai-全流程编排': '全流程编排',
    'zhicai-选题决策': '选题决策',
    'zhicai-标题生成': '标题生成',
    'zhicai-开头钩子': '开头钩子',
    'zhicai-叙事结构': '叙事结构',
    'zhicai-段落心法': '段落心法',
    'zhicai-风格调校': '风格调校',
    'zhicai-情感曲线': '情感曲线',
    'zhicai-结尾收束': '结尾收束',
    'zhicai-心理学武器': '心理学武器',
    'zhicai-爆款预测': '爆款预测',
    'zhicai-大师写作法': '大师写作法',
    'zhicai-内容诊断': '内容诊断',
    'zhicai-AI去味': 'AI去味',
    'zhicai-跨平台分发': '跨平台分发',
    'zhicai-IP人设构建': 'IP人设构建',
    'zhicai-素材工坊': '素材工坊',
    'zhicai-热点追踪': '热点追踪',
}

SKILL_TOPIC = {
    'zhicai': '路由器',
    'zhicai-全流程编排': '全流程',
    'zhicai-选题决策': '选题决策',
    'zhicai-标题生成': '标题生成',
    'zhicai-开头钩子': '开头钩子',
    'zhicai-叙事结构': '叙事结构',
    'zhicai-段落心法': '段落心法',
    'zhicai-风格调校': '风格调校',
    'zhicai-情感曲线': '情感曲线',
    'zhicai-结尾收束': '结尾收束',
    'zhicai-心理学武器': '心理学武器',
    'zhicai-爆款预测': '爆款预测',
    'zhicai-大师写作法': '大师写作法',
    'zhicai-内容诊断': '内容诊断',
    'zhicai-AI去味': 'AI去味',
    'zhicai-跨平台分发': '跨平台分发',
    'zhicai-IP人设构建': 'IP人设构建',
    'zhicai-素材工坊': '素材工坊',
    'zhicai-热点追踪': '热点追踪',
}


def assign_skill(atom):
    """根据 topics 字段自动分配 skill：先匹配来源路径，再匹配模块前缀，再匹配主题关键词"""
    # 第0优先级：来源路径子模块关键词（瓶颈突破/社会热点等，优先于创作者名）
    source = atom.get('source', '')
    source_lower = source.lower()
    source_sub_skills = {
        '瓶颈突破': 'zhicai-内容诊断',
        '写作瓶颈': 'zhicai-内容诊断',
        '社会热点': 'zhicai-热点追踪',
        '热点话题': 'zhicai-热点追踪',
    }
    for kw, skill in source_sub_skills.items():
        if kw in source_lower:
            return [skill]

    # 第1优先级：来源路径创作者关键词匹配
    source_skills = {
        '卡兹克': 'zhicai-大师写作法',
        'khazix': 'zhicai-大师写作法',
        '粥左罗': 'zhicai-大师写作法',
        '阿test': 'zhicai-大师写作法',
        '正经比比': 'zhicai-大师写作法',
        'lsir': 'zhicai-大师写作法',
        'l先生': 'zhicai-大师写作法',
        'humanizer': 'zhicai-AI去味',
        '去ai': 'zhicai-AI去味',
        'ai痕迹': 'zhicai-AI去味',
        'operating': 'zhicai-跨平台分发',
        '运营': 'zhicai-跨平台分发',
        'ray': 'zhicai-IP人设构建',
        '新世相': 'zhicai-大师写作法',
        '洞见': 'zhicai-大师写作法',
        '大师': 'zhicai-大师写作法',
        'viral': 'zhicai-标题生成',
        '爆款': 'zhicai-爆款预测',
        '方法论': 'zhicai-全流程编排',
        'sop': 'zhicai-素材工坊',
        'skill': 'zhicai',
    }
    for kw, skill in source_skills.items():
        if kw in source_lower:
            return [skill]

    topics = atom.get('topics', [])

    # 第一优先级：模块代码前缀
    for topic in topics:
        for prefix, skill in MODULE_TO_SKILL.items():
            if topic.startswith(prefix):
                return [skill]

    # 第二优先级：主题关键词
    topics_lower = set(t.lower() for t in topics)
    matched_skills = set()
    for topic, skill in TOPIC_TO_SKILL.items():
        if topic.lower() in topics_lower:
            matched_skills.add(skill)
    return list(matched_skills) if matched_skills else ['zhicai']


def main():
    # 读取所有原子并分配 skills
    skill_atoms = defaultdict(list)
    with open(ATOMS_PATH) as f:
        for line in f:
            atom = json.loads(line)
            skills = assign_skill(atom)
            atom['skills'] = skills
            for skill in skills:
                skill_atoms[skill].append(atom)

    # 写回规范化后的 atoms.jsonl
    all_atoms = []
    for atoms in skill_atoms.values():
        all_atoms.extend(atoms)
    with open(ATOMS_PATH, 'w') as f:
        for atom in all_atoms:
            f.write(json.dumps(atom, ensure_ascii=False) + '\n')

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 生成每个技能的知识包
    for skill in sorted(skill_atoms.keys()):
        atoms = skill_atoms[skill]
        cn = SKILL_CN.get(skill, skill)
        topic = SKILL_TOPIC.get(skill, skill)

        md = f"# {cn}：{topic}知识原子\n\n"
        md += f"> 来源：{skill} | 共 {len(atoms)} 个知识原子 | 自动生成\n\n"

        # 按 type 分组
        by_type = defaultdict(list)
        for atom in atoms:
            by_type[atom.get('type', 'principle')].append(atom)

        type_labels = {
            'principle': '## 核心原则',
            'method': '## 方法',
            'data': '## 数据',
            'insight': '## 洞察',
            'pattern': '## 模式',
            'technique': '## 技法',
            'structure': '## 结构',
            'rule': '## 规则',
            'formula': '## 公式',
            'tool': '## 工具',
            'checklist': '## 清单',
            'model': '## 模型',
        }

        for type_name in ['principle', 'method', 'data', 'insight', 'pattern', 'technique',
                          'structure', 'rule', 'formula', 'tool', 'checklist', 'model']:
            if type_name not in by_type:
                continue
            label = type_labels.get(type_name, f'## {type_name}')
            md += f"\n{label}\n\n"
            for atom in by_type[type_name]:
                knowledge = atom.get('knowledge', '')
                original = atom.get('original', '')
                atom_id = atom.get('id', '')
                topics = ', '.join(atom.get('topics', []))
                date = atom.get('date', '')
                confidence = atom.get('confidence', 'medium')

                md += f"- 🔥 **{knowledge}**\n"
                md += f"  - `{atom_id}` | {date} | {topics}\n"
                if original:
                    # Truncate original to ~120 chars for readability
                    short_orig = original[:120] + ('...' if len(original) > 120 else '')
                    md += f"  - 原文：{short_orig}\n"
                md += "\n"

        filepath = os.path.join(OUTPUT_DIR, f'{skill}_知识包.md')
        # 路由器的知识包加「路由器」标识，避免和默认知识包混淆
        if skill == 'zhicai':
            filepath = os.path.join(OUTPUT_DIR, 'zhicai_路由器_知识包.md')
        with open(filepath, 'w') as f:
            f.write(md)
        print(f'  {skill}_知识包.md — {len(atoms)} atoms')

    print(f'\nDone: {len(skill_atoms)} knowledge packages generated')
    print(f'Total atoms assigned: {len(all_atoms)}')


if __name__ == '__main__':
    main()
