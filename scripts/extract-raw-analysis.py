#!/usr/bin/env python3
"""
从 01-原始资料 中只提取分析报告和 SKILL 文件。
规则：文件名含 SKILL/skill/分析/指南/报告/方法论/框架 的提取；
      原始文章目录（articles_raw/articles_sorted/文章/正文/raw）跳过。
用法：python3 scripts/extract-raw-analysis.py
"""
import os, sys, json, re, glob

RAW_ROOT = "/Users/hanzhicai/Library/Mobile Documents/iCloud~md~obsidian/Documents/知材的知识管理/知识库·内容创作者中心/01-原始资料"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '知识库', '原子库')

# 跳过不读的目录关键词（原始文章库）
SKIP_DIRS = ['articles_raw', 'articles_sorted', 'raw_articles', 'article_texts',
             'articles', '正文字', '文章库', '文章全文', 'article', 'dongjian_articles',
             'A_商业财经', 'B_历史文化', 'C_社会现象', 'D_科技互联网', 'E_国际政治',
             'F_影视娱乐', 'articles_classified', '01_个人成长', '02_情感人际',
             '03_社会洞察', '04_励志人物', 'articles_analysis', 'khazix-articles']

# 读的文件名关键词
INCLUDE_KEYWORDS = ['SKILL', 'skill', '分析', '指南', '报告', '方法论', '框架',
                    'method', 'guide', 'reference', 'template', 'checklist',
                    'research', '研究', '拆解', '体系', '模型', 'SOP', 'workflow']

def should_skip(dirpath):
    """判断目录是否应跳过（原始文章库）"""
    for skip in SKIP_DIRS:
        if '/' + skip in dirpath or dirpath.endswith('/' + skip):
            return True
    return False

def should_include(filename):
    """判断文件是否是分析/SKILL类"""
    for kw in INCLUDE_KEYWORDS:
        if kw in filename:
            return True
    return False

def is_high_quality(text):
    """判断句子是否含高价值内容"""
    if len(text) < 20:
        return False
    if len(text) > 500:
        return False
    if re.match(r'^[\s\-—·•*#_、，。！？；：""''【】《》（）\[\]{}]+$', text):
        return False
    if re.match(r'^[├└│─┃┗┏┓┛━\s]+', text):
        return False
    if re.match(r'^\|.*\|$', text):
        return False
    filler = ['我们来看看', '你说得对', '点击这里', '更多内容', '欢迎关注',
              '关注我', '点赞收藏', '关注转发']
    for f in filler:
        if f in text and len(text) < 30:
            return False
    signals = [
        r'\*\*(.*?)\*\*', r'本质[上是]', r'核心', r'关键', r'最重要',
        r'公式[：:]', r'模板[：:]', r'步骤[一二三]', r'第[一二三四五]步',
        r'方法[：:]', r'不要', r'避免', r'绝对', r'必须', r'一定', r'务必',
        r'不是.*而是', r'本质上', r'定律', r'法则', r'效应', r'原理',
        r'^[-•·]\s+\*\*', r'^\d+[.、．]\s+\*\*',
        r'操作公式', r'核心理论', r'验证案例', r'注意事项',
    ]
    for s in signals:
        if re.search(s, text):
            return True
    if re.match(r'^\d+[.、．]\s', text):
        return True
    return False


def classify_type(text):
    if re.search(r'(定律|法则|原理|本质|核心|不是.*而是)', text):
        return 'principle'
    elif re.search(r'(步骤|方法|公式|模板|操作|如何|怎么|方式|策略)', text):
        return 'method'
    elif re.search(r'(%|\d+万|\d+亿|概率|频率|占比|统计)', text):
        return 'data'
    elif re.search(r'(不要|避免|错误|注意|陷阱|禁止|千万)', text):
        return 'pattern'
    else:
        return 'insight'


def extract_atoms(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        raw = f.read()
    relpath = os.path.relpath(filepath, RAW_ROOT)
    body = re.sub(r'^---\s*\n.*?\n---\s*\n', '', raw, flags=re.DOTALL)
    body = re.sub(r'\[\[([^\]]+)\]\]', r'\1', body)
    body = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', body)
    paras = re.split(r'\n\n+', body)
    atoms = []
    seen = set()
    aid = 0
    for para in paras:
        para = para.strip()
        if not para:
            continue
        bolds = re.findall(r'\*\*([^*]+)\*\*', para)
        for bp in bolds:
            bp = bp.strip()
            if 8 < len(bp) < 300 and bp not in seen:
                seen.add(bp)
                aid += 1
                atoms.append({"id": f"RAW_{aid:04d}", "knowledge": bp, "source": f"01-原始资料/{relpath}", "topics": [], "skills": [], "type": classify_type(bp), "confidence": "high"})
        sents = re.split(r'(?<=[。！？；\n])', para)
        for sent in sents:
            sent = re.sub(r'\s+', ' ', sent.strip())
            sent = re.sub(r'^[-*•·#]+\s*', '', sent)
            sent = re.sub(r'^>\s*', '', sent)
            if not sent or sent in seen or not is_high_quality(sent):
                continue
            seen.add(sent)
            aid += 1
            atoms.append({"id": f"RAW_{aid:04d}", "knowledge": sent[:300], "source": f"01-原始资料/{relpath}", "topics": [], "skills": [], "type": classify_type(sent), "confidence": "medium"})
    return atoms

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_atoms = []
    total_files = 0

    for root, dirs, files in os.walk(RAW_ROOT):
        # 跳过原始文章目录
        dirs[:] = [d for d in dirs if not should_skip(os.path.join(root, d))]

        for fname in files:
            if not fname.endswith('.md'):
                continue
            if not should_include(fname):
                continue

            fpath = os.path.join(root, fname)
            try:
                atoms = extract_atoms(fpath)
                if atoms:
                    all_atoms.extend(atoms)
                    total_files += 1
                    print(f"  {os.path.relpath(fpath, RAW_ROOT)[:80]}: {len(atoms)} atoms")
            except Exception as e:
                print(f"  [ERR] {fname}: {e}")

    # 写入
    outpath = os.path.join(OUTPUT_DIR, 'atoms_raw_analysis.jsonl')
    with open(outpath, 'w', encoding='utf-8') as f:
        for atom in all_atoms:
            f.write(json.dumps(atom, ensure_ascii=False) + '\n')

    print(f"\n{'='*50}")
    print(f"文件数: {total_files}")
    print(f"原子数: {len(all_atoms)}")
    print(f"输出: {outpath}")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
