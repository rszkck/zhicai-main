#!/usr/bin/env python3
"""
从 02-Wiki知识库 所有 14 个模块提取知识原子。
清洗格式残留，只输出有实质内容的原子。
用法：python3 scripts/extract-wiki-atoms.py
"""
import os, sys, json, re, glob

WIKI_ROOT = "/Users/hanzhicai/Library/Mobile Documents/iCloud~md~obsidian/Documents/知材的知识管理/知识库·内容创作者中心/02-Wiki知识库"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '知识库', '原子库')

MODULES = [
    ('00-总纲', 'zhicai-全流程编排'),
    ('01-选题系统', 'zhicai-选题决策'),
    ('02-标题公式库', 'zhicai-标题生成'),
    ('03-开头钩子', 'zhicai-开头钩子'),
    ('04-叙事结构', 'zhicai-叙事结构'),
    ('05-段落心法', 'zhicai-段落心法'),
    ('06-语言风格', 'zhicai-风格调校'),
    ('07-情感曲线', 'zhicai-情感曲线'),
    ('08-结尾收束', 'zhicai-结尾收束'),
    ('09-心理学武器', 'zhicai-心理学武器'),
    ('10-爆款预测', 'zhicai-爆款预测'),
    ('11-大师案例库', 'zhicai-大师写作法'),
    ('12-账号风格库', 'zhicai-跨平台分发'),
    ('13-IP人设与信任构建', 'zhicai-IP人设构建'),
]



def extract_frontmatter(content):
    """提取 frontmatter 字段"""
    fm = {}
    m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if m:
        for line in m.group(1).split('\n'):
            if ':' in line and not line.startswith('---'):
                key, val = line.split(':', 1)
                fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm


def is_real_sentence(text):
    """判断是否是一个完整的知识性句子"""
    if len(text) < 20 or len(text) > 400:
        return False
    if not re.search(r'[。！？]$', text):
        return False
    if '|' in text or '├' in text or '└' in text:
        return False
    if re.match(r'^[\d\s\-—·•*#_、，。！？；：""''【】《》（）\[\]{}%]+$', text):
        return False
    if not re.search(r'[一-鿿]', text):
        return False
    grammar_words = ['是', '的', '了', '在', '有', '不', '和', '与', '就', '也', '都', '要', '会', '能', '让', '把', '被', '从', '对', '为']
    has_grammar = any(gw in text for gw in grammar_words)
    chinese_chars = len(re.findall(r'[一-鿿]', text))
    return has_grammar and chinese_chars >= 8


def is_real_phrase(text):
    """判断是否是独立有意义的短语（用于粗体提取）"""
    if len(text) < 8 or len(text) > 150:
        return False
    if '|' in text or '├' in text:
        return False
    if not re.search(r'[一-鿿]', text):
        return False
    domain_kw = ['公式', '法则', '定律', '原理', '效应', '框架', '模型', '结构',
                 '方法', '技巧', '步骤', '模板', '策略', '体系', '核心', '本质', '关键',
                 '不要', '避免', '必须', '一定', '永远']
    return any(kw in text for kw in domain_kw)


def extract_atoms_from_md(filepath, module_code, skill_name):
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()

    file_rel = os.path.relpath(filepath, WIKI_ROOT)
    fm = extract_frontmatter(raw)
    body = re.sub(r'^---\s*\n.*?\n---\s*\n', '', raw, flags=re.DOTALL)

    # 去掉代码块
    body = re.sub(r'```[\s\S]*?```', '', body)
    # 去掉 Obsidian 链接，保留文字
    body = re.sub(r'\[\[([^\]]+)\]\]', r'\1', body)
    body = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', body)
    # 去掉表格
    body = re.sub(r'\|.+\|\s*\n\|[\s\-]+\|\s*(\n\|.+\|)*', '', body)
    body = re.sub(r'^\|.+\|$', '', body, flags=re.MULTILINE)
    # 去掉决策树线条
    body = re.sub(r'^[├└│─╲╱┃┗┏┓┛━\s]+.*$', '', body, flags=re.MULTILINE)

    paragraphs = re.split(r'\n\n+', body)
    atoms = []
    atom_id = 0
    seen = set()

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # 1. 提取粗体短语（高置信度）
        bold_phrases = re.findall(r'\*\*([^*]+)\*\*', para)
        for bp in bold_phrases:
            bp = bp.strip()
            if is_real_phrase(bp) and bp not in seen:
                seen.add(bp)
                atom_id += 1
                atom_type = 'principle' if any(kw in bp for kw in ['核心', '本质', '关键', '定律', '法则', '原理']) else 'method'
                atoms.append({
                    "id": f"WIKI_{module_code}_{atom_id:03d}",
                    "knowledge": bp,
                    "source": file_rel,
                    "topics": [module_code] + ([fm.get('category', '')] if fm.get('category') else []),
                    "skills": [skill_name] if skill_name else [],
                    "type": atom_type,
                    "confidence": "high"
                })

        # 2. 提取完整句子
        para_clean = re.sub(r'\*\*(.*?)\*\*', r'\1', para)
        sentences = re.split(r'(?<=[。！？])\s*', para_clean)
        for sent in sentences:
            sent = sent.strip()
            sent = re.sub(r'^[-*•·#]+\s*', '', sent)
            sent = re.sub(r'\s+', ' ', sent)
            if not sent or sent in seen:
                continue
            if not is_real_sentence(sent):
                continue
            seen.add(sent)
            atom_id += 1
            atom_type = 'insight'
            if any(kw in sent for kw in ['核心', '本质', '关键', '最重要', '定律', '法则', '不是']):
                atom_type = 'principle'
            elif any(kw in sent for kw in ['步骤', '方法', '公式', '模板', '如何', '方式', '策略']):
                atom_type = 'method'
            elif re.search(r'[%]', sent):
                atom_type = 'data'
            atoms.append({
                "id": f"WIKI_{module_code}_{atom_id:03d}",
                "knowledge": sent[:300],
                "source": file_rel,
                "topics": [module_code] + ([fm.get('category', '')] if fm.get('category') else []),
                "skills": [skill_name] if skill_name else [],
                "type": atom_type,
                "confidence": "medium"
            })

    return atoms


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total_atoms = 0
    all_atoms = []

    for module_code, skill_name in MODULES:
        module_path = os.path.join(WIKI_ROOT, module_code)
        if not os.path.exists(module_path):
            print(f"  [缺失] {module_code}")
            continue

        files = sorted(glob.glob(os.path.join(module_path, '**', '*.md'), recursive=True))
        module_atoms = []

        for fpath in files:
            atoms = extract_atoms_from_md(fpath, module_code, skill_name)
            module_atoms.extend(atoms)
            print(f"  {os.path.relpath(fpath, WIKI_ROOT)}: {len(atoms)} atoms")

        # 写入模块文件
        outpath = os.path.join(OUTPUT_DIR, f'atoms_wiki_{module_code}.jsonl')
        with open(outpath, 'w', encoding='utf-8') as f:
            for atom in module_atoms:
                f.write(json.dumps(atom, ensure_ascii=False) + '\n')

        print(f"  => {module_code}: {len(module_atoms)} atoms")
        total_atoms += len(module_atoms)
        all_atoms.extend(module_atoms)

    # 写入全量合并
    merged_path = os.path.join(OUTPUT_DIR, 'atoms_wiki.jsonl')
    with open(merged_path, 'w', encoding='utf-8') as f:
        for atom in all_atoms:
            f.write(json.dumps(atom, ensure_ascii=False) + '\n')

    print(f"\n{'='*50}")
    print(f"总计: {total_atoms} atoms from {len(MODULES)} modules")
    print(f"全量: {merged_path}")
    print(f"{'='*50}")


if __name__ == '__main__':
    main()
