#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文AI味检测脚本 (lint_ai_zh.py)
检测中文文本中的AI写作特征，输出AI味评分和问题诊断。

用法:
    python lint_ai_zh.py <file>           # 检测文件
    python lint_ai_zh.py --text "文本"     # 直接检测文本
    echo "文本" | python lint_ai_zh.py -   # 从stdin读取
"""

import re
import sys
import json
import argparse
from collections import defaultdict
from typing import List, Dict, Tuple, Any


# ============================================================
# AI特征模式库
# ============================================================

AI_PATTERNS = {
    # --- A. 结构套路类 ---
    "排比三连": {
        "patterns": [
            r'[^，。；！？]{2,8}是[^，。；！？]{2,10}的[^，。；！？]{2,6}[，,][^，。；！？]{2,8}是[^，。；！？]{2,10}的[^，。；！？]{2,6}[，,][^，。；！？]{2,8}是[^，。；！？]{2,10}的',
            r'[^，。；！？]{2,6}[、，][^，。；！？]{2,6}[、，][^，。；！？]{2,6}[，。]',  # 三词并列
        ],
        "weight": 10,
        "category": "结构套路",
        "hint": "避免工整的三连排比，打破对称结构",
    },
    "首先其次最后": {
        "patterns": [
            r'首先[^。]*其次[^。]*最后',
            r'第一[^。]*第二[^。]*第三',
            r'一方面[^。]*另一方面[^。]*此外',
        ],
        "weight": 8,
        "category": "结构套路",
        "hint": "避免八股式分点，用自然的逻辑连接",
    },
    "不仅而且递进": {
        "patterns": [
            r'不仅[^，。]{2,15}[，,]而且[^，。]{2,15}',
            r'不但[^，。]{2,15}[，,]而且[^，。]{2,15}[，,]更',
        ],
        "weight": 6,
        "category": "结构套路",
        "hint": "不要机械递进，只说最重要的点",
    },
    "不是而是": {
        "patterns": [
            r'不是[^，。]{2,20}[，,]而是',
            r'并非[^，。]{2,20}[，,]而是',
        ],
        "weight": 7,
        "category": "结构套路",
        "hint": "直接说是什么，不要先否定再肯定",
    },
    "对称句式": {
        "patterns": [
            r'[^，。；]{4,12}[是为][^，。；]{2,8}[，,][^，。；]{4,12}[是为][^，。；]{2,8}',
        ],
        "weight": 5,
        "category": "结构套路",
        "hint": "打破对称，长短句交替",
    },

    # --- B. 过渡词类 ---
    "值得注意的是": {
        "patterns": [r'值得注意的是', r'需要指出的是', r'不容忽视的是', r'需要强调的是'],
        "weight": 5,
        "category": "过渡词",
        "hint": "直接说内容，去掉这个前缀",
    },
    "总而言之": {
        "patterns": [r'总而言之', r'综上所述', r'归纳而言', r'由此可见', r'总的来说'],
        "weight": 5,
        "category": "过渡词",
        "hint": "直接给结论，不用套话开头",
    },
    "不可否认": {
        "patterns": [r'不可否认', r'毋庸置疑', r'毫无疑问', r'显然[,，]'],
        "weight": 4,
        "category": "过渡词",
        "hint": "直接说事实，不做铺垫",
    },
    "与此同时": {
        "patterns": [r'与此同时', r'在此基础上', r'另一方面[,，]'],
        "weight": 3,
        "category": "过渡词",
        "hint": "用'同时'或直接接下一句",
    },
    "然而转折": {
        "patterns": [r'然而[,，]', r'尽管如此[,，]', r'话虽如此[,，]'],
        "weight": 3,
        "category": "过渡词",
        "hint": "口语用'但/不过'，'然而'过于书面",
    },

    # --- C. 形容词/黑话类 ---
    "互联网黑话": {
        "patterns": [
            r'赋能', r'抓手', r'闭环', r'生态(?!环境)', r'链路', r'打法',
            r'颗粒度', r'对齐', r'拉齐', r'跑通', r'沉淀(?!于)', r'迭代',
            r'心智', r'组合拳', r'护城河', r'底层逻辑', r'顶层设计',
            r'全链路', r'全方位', r'多维度', r'立体化', r'赋能.*升级',
        ],
        "weight": 8,
        "category": "词汇选择",
        "hint": "用大白话替换互联网黑话",
    },
    "空洞形容词": {
        "patterns": [
            r'具有重要意义', r'产生深远影响', r'发挥积极作用', r'取得显著成效',
            r'重大意义', r'深远意义', r'积极影响', r'显著提升', r'重大突破',
            r'重要引擎', r'核心驱动力', r'关键支撑', r'坚实基础', r'有力保障',
        ],
        "weight": 6,
        "category": "词汇选择",
        "hint": "用具体数据/案例代替空洞形容词",
    },
    "程度副词堆砌": {
        "patterns": [
            r'深刻(?:理解|认识|体会|把握|变革)',
            r'全面(?:落实|推进|提升|发展|加强)',
            r'深入(?:推进|分析|研究|开展|探讨)',
            r'充分(?:认识|发挥|利用|体现|调动)',
            r'有效(?:提升|解决|促进|保障|实施)',
            r'大力(?:发展|推进|支持|加强|推广)',
        ],
        "weight": 4,
        "category": "词汇选择",
        "hint": "删掉程度副词，用动词本身说话",
    },

    # --- D. 语气/腔调类 ---
    "翻译腔": {
        "patterns": [
            r'作为一(?:个|名|位)[^，。]{2,10}[，,]',
            r'有着[^，。]{2,10}的(?:特点|特征|优势|作用)',
            r'基于[^，。]{2,15}的基础上',
            r'对于[^，。]{2,15}来说',
            r'进行了[^，。]{2,10}的(?:讨论|分析|研究|探索)',
            r'致力于[^，。]{2,20}[，。]',
            r'...的存在',
        ],
        "weight": 6,
        "category": "语气腔调",
        "hint": "回归中文表达，动词优先，少用弱动词",
    },
    "官腔": {
        "patterns": [
            r'为[^，。]{2,10}奠定了坚实基础',
            r'为[^，。]{2,10}提供了有力保障',
            r'取得了阶段性成果',
            r'呈现出良好(?:态势|势头|局面)',
            r'不断提升|持续改善|稳步推进|扎实推进',
            r'贯彻落实|统一思想|提高认识',
        ],
        "weight": 7,
        "category": "语气腔调",
        "hint": "用具体结果代替官话套话",
    },
    "升华金句": {
        "patterns": [
            r'每一个[^，。]{2,10}的背后[^，。]',
            r'终将[^，。]{2,15}必将',
            r'[^，。]是一种[^，。]{2,8}[，。]',
            r'让我们一起[^，。]{2,15}',
            r'未来可期|道阻且长|行则将至',
        ],
        "weight": 5,
        "category": "语气腔调",
        "hint": "删掉强行升华的金句，平实收尾",
    },
    "说教口吻": {
        "patterns": [
            r'我们(?:应该|应当|必须|需要|要学会|要懂得)[^，。]{2,20}',
        ],
        "weight": 4,
        "category": "语气腔调",
        "hint": "换成分享经验的口吻，不要居高临下",
    },

    # --- E. 开头/结尾类 ---
    "时代背景开头": {
        "patterns": [
            r'^(?:在)?(?:当今|如今|当下|现在)(?:这个)?(?:时代|社会|背景下)',
            r'^随着[^，。]{2,20}的(?:快速|迅猛|飞速|不断|持续)?(?:发展|进步|崛起|普及)',
            r'^近年来[,，]',
            r'^在[^，。]{2,15}的大背景下',
        ],
        "weight": 8,
        "category": "开头结尾",
        "hint": "用具体场景/数据/问题直接切入，不要宏大叙事开头",
    },
    "展望未来结尾": {
        "patterns": [
            r'展望未来[^，。]',
            r'相信在不久的将来',
            r'未来[^，。]{2,10}必将',
            r'让我们拭目以待',
            r'[^，。]一定会越来越好',
        ],
        "weight": 6,
        "category": "开头结尾",
        "hint": "结尾用具体建议或有回味的细节，不要空喊未来",
    },
    "双刃剑隐喻": {
        "patterns": [
            r'一把双刃剑',
            r'既是机遇也是挑战',
            r'既有(?:其)?优势也有(?:其)?弊端',
            r'有利(?:也)?有弊',
        ],
        "weight": 4,
        "category": "内容空洞",
        "hint": "直接说利弊是什么，不要用烂大街比喻",
    },
    "被动语态": {
        "patterns": [
            r'被广泛(?:应用于|认为是|称为|使用)',
            r'被誉?为[^，。]{2,15}',
            r'被称(?:为|作)[^，。]{2,15}',
        ],
        "weight": 3,
        "category": "词汇选择",
        "hint": "换成主动语态",
    },
    "大跨度概括": {
        "patterns": [
            r'从[^，。]{2,8}到[^，。]{2,8}[，,]从[^，。]{2,8}到[^，。]{2,8}',
            r'渗透到[^，。]{2,10}的方方面面',
            r'无处不在|随处可见',
        ],
        "weight": 4,
        "category": "内容空洞",
        "hint": "缩小范围，写具体场景，不要面面俱到",
    },
    "过度平衡": {
        "patterns": [
            r'在看到[^，。]{2,10}的同时[^，。]也要(?:注意|看到|关注)',
            r'既要[^，。]{2,10}[，,]又要[^，。]{2,10}[，,]还要',
        ],
        "weight": 4,
        "category": "内容空洞",
        "hint": "给出明确立场，不要两头讨好",
    },
}

# 句子分割
SENTENCE_SPLIT = re.compile(r'[。！？；\n]+')


def detect_ai_features(text: str) -> Tuple[int, List[Dict], Dict[str, int]]:
    """检测文本中的AI特征，返回(score, hits, category_counts)"""
    hits = []
    category_counts = defaultdict(int)
    total_weight = 0

    # 按句子检测
    sentences = [s.strip() for s in SENTENCE_SPLIT.split(text) if s.strip()]

    for sent_idx, sentence in enumerate(sentences):
        for feature_name, feature_info in AI_PATTERNS.items():
            for pattern in feature_info["patterns"]:
                try:
                    matches = re.finditer(pattern, sentence)
                    for match in matches:
                        hit = {
                            "feature": feature_name,
                            "category": feature_info["category"],
                            "weight": feature_info["weight"],
                            "hint": feature_info["hint"],
                            "sentence_idx": sent_idx,
                            "sentence": sentence[:80] + ("..." if len(sentence) > 80 else ""),
                            "matched": match.group(0)[:40],
                            "position": match.start(),
                        }
                        hits.append(hit)
                        category_counts[feature_info["category"]] += 1
                        total_weight += feature_info["weight"]
                        break  # 同一句子同一特征只记一次
                except re.error:
                    continue

    # 计算排比密度加分
    parallel_count = sum(1 for h in hits if h["feature"] in ("排比三连", "对称句式"))
    if parallel_count >= 2:
        total_weight += 15

    # 检查开头
    first_100 = text[:100]
    for feature_name, feature_info in AI_PATTERNS.items():
        if "开头" in feature_info.get("category", ""):
            for pattern in feature_info["patterns"]:
                try:
                    if re.search(pattern, first_100):
                        total_weight += 5
                        break
                except re.error:
                    continue

    # 口语化表达扣分
    colloquial = len(re.findall(r'其实|真的|挺|蛮|有点|怎么说|你知道|对吧|嘛|呗|啦', text))
    total_weight = max(0, total_weight - colloquial * 2)

    # 归一化到0-100
    score = min(100, total_weight * 2)

    return score, hits, dict(category_counts)


def get_rating(score: int) -> str:
    if score <= 20:
        return "自然"
    elif score <= 40:
        return "轻微AI味"
    elif score <= 60:
        return "中等AI味"
    elif score <= 80:
        return "浓重AI味"
    else:
        return "典型AI"


def format_report(text: str, score: int, hits: List[Dict], category_counts: Dict[str, int]) -> str:
    """格式化检测报告"""
    lines = []
    lines.append("=" * 60)
    lines.append("中文AI味检测报告")
    lines.append("=" * 60)
    lines.append("")

    # 评分
    rating = get_rating(score)
    lines.append(f"AI味评分: {score}/100  ({rating})")
    lines.append("")

    # 评分条
    bar_len = 40
    filled = int(bar_len * score / 100)
    bar = "█" * filled + "░" * (bar_len - filled)
    lines.append(f"[{bar}]")
    lines.append("")

    # 问题分类统计
    if category_counts:
        lines.append("问题分类统计:")
        for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
            lines.append(f"  - {cat}: {count}处")
        lines.append("")

    # 详细问题列表
    if hits:
        lines.append("-" * 60)
        lines.append(f"发现 {len(hits)} 处AI写作特征:")
        lines.append("-" * 60)

        # 去重并按权重排序
        seen = set()
        unique_hits = []
        for h in hits:
            key = (h["feature"], h["sentence_idx"])
            if key not in seen:
                seen.add(key)
                unique_hits.append(h)

        unique_hits.sort(key=lambda x: -x["weight"])

        for i, hit in enumerate(unique_hits, 1):
            lines.append("")
            lines.append(f"[{i}] {hit['feature']} (权重:{hit['weight']})")
            lines.append(f"    分类: {hit['category']}")
            lines.append(f"    问题句: {hit['sentence']}")
            lines.append(f"    匹配: ...{hit['matched']}...")
            lines.append(f"    建议: {hit['hint']}")

    lines.append("")
    lines.append("=" * 60)
    lines.append("改写建议:")
    lines.append("  1. 打破工整排比和对称结构，长短句交替")
    lines.append("  2. 删掉'值得注意的是/综上所述/总而言之'等过渡套话")
    lines.append("  3. 用具体数据和案例代替'深远影响/重要意义'等空洞形容词")
    lines.append("  4. 避免'不仅...而且...更...'机械递进，只说最重点")
    lines.append("  5. 替换'赋能/抓手/闭环/生态'等互联网黑话为大白话")
    lines.append("  6. 去掉'随着...发展'式开头，用具体场景切入")
    lines.append("  7. 删掉结尾升华金句，平实收尾")
    lines.append("  8. 加入具体数字、人名、案例、个人经历")
    lines.append("=" * 60)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="中文AI味检测工具")
    parser.add_argument("file", nargs="?", help="要检测的文本文件路径")
    parser.add_argument("--text", "-t", help="直接检测提供的文本")
    parser.add_argument("--json", "-j", action="store_true", help="以JSON格式输出")
    args = parser.parse_args()

    # 读取文本
    if args.text:
        text = args.text
    elif args.file and args.file != "-":
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("错误: 没有输入文本", file=sys.stderr)
        sys.exit(1)

    # 检测
    score, hits, category_counts = detect_ai_features(text)

    if args.json:
        result = {
            "score": score,
            "rating": get_rating(score),
            "hit_count": len(hits),
            "categories": category_counts,
            "hits": [
                {
                    "feature": h["feature"],
                    "category": h["category"],
                    "weight": h["weight"],
                    "hint": h["hint"],
                    "sentence": h["sentence"],
                    "matched": h["matched"],
                }
                for h in hits
            ],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_report(text, score, hits, category_counts))


if __name__ == "__main__":
    main()
