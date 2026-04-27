#!/usr/bin/env python3
"""
valdea legacy - HTML→JSON完全変換
Sorcery!スタイル適用
"""

import re
import json
from typing import Dict, List, Any

def extract_paragraph_html(content: str, para_id: str) -> str:
    """指定IDのパラグラフHTMLを抽出"""
    pattern = rf'<div class="para" id="{re.escape(para_id)}">.*?</div>\s*(?=<div class="para" id="|</body>)'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(0) if match else ""

def clean_text(html: str) -> str:
    """HTMLタグを削除してプレーンテキスト化"""
    # <p>タグを改行に
    text = re.sub(r'</p>\s*<p>', '\n\n', html)
    # 全HTMLタグ削除
    text = re.sub(r'<[^>]+>', '', text)
    # HTML entities
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&')
    # 連続空白を削除
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_choices(para_html: str) -> List[Dict[str, Any]]:
    """選択肢を解析してSorcery!スタイルで構造化"""
    choices = []
    choice_id = 1
    
    for btn_match in re.finditer(r'<button[^>]*onclick="([^"]*)"[^>]*>([^<]*)</button>', para_html):
        onclick = btn_match.group(1)
        label = btn_match.group(2).strip()
        
        # goto先を抽出
        target = None
        action_type = "unknown"
        
        if "goto('" in onclick:
            goto_match = re.search(r"goto\('([^']+)'\)", onclick)
            target = goto_match.group(1) if goto_match else None
            action_type = "goto"
        elif "payGoto(" in onclick:
            paygoto_match = re.search(r"payGoto\((\d+),'([^']+)'", onclick)
            if paygoto_match:
                cost = paygoto_match.group(1)
                target = paygoto_match.group(2)
                action_type = "pay_goto"
        elif "luckCheck(" in onclick:
            luck_match = re.search(r"luckCheck\('([^']+)','([^']+)'", onclick)
            if luck_match:
                target = luck_match.group(1)  # 成功先
                action_type = "luck_check"
        elif "startCombat(" in onclick:
            combat_match = re.search(r"startCombat\('[^']*',\s*\d+,\s*\d+,\s*\d+,\s*'([^']*)'", onclick)
            if combat_match:
                target = combat_match.group(1)
                action_type = "combat"
        
        # Sorcery!スタイルの選択肢分類
        choice_weight = classify_choice_weight(label, action_type)
        
        choices.append({
            "id": f"c{choice_id}",
            "label": label,
            "target": target,
            "type": action_type,
            "weight": choice_weight,
            "action": onclick
        })
        choice_id += 1
    
    return choices

def classify_choice_weight(label: str, action_type: str) -> str:
    """選択肢の性格を分類（Sorcery!スタイル）"""
    label_lower = label.lower()
    
    # 探索系
    if any(word in label for word in ['調べる', '確かめ', '見る', '探す', '調査']):
        return "exploration"
    # 戦闘系
    elif any(word in label for word in ['戦', '攻撃', '迎え撃', '立ち向か']):
        return "combat"
    # 慎重系
    elif any(word in label for word in ['様子', '待つ', '観察', '慎重']):
        return "cautious"
    # 大胆系
    elif any(word in label for word in ['急ぐ', '飛び込', '突進', '大胆']):
        return "bold"
    # 外交系
    elif any(word in label for word in ['話', '説得', '交渉', '聞く']):
        return "diplomatic"
    # 回避系
    elif any(word in label for word in ['逃げ', '退', '避け', '離れ']):
        return "retreat"
    # 購入系
    elif '金貨' in label or '買' in label:
        return "purchase"
    # スキップ系
    elif any(word in label for word in ['すぐ', 'まっすぐ', '情報は', '十分']):
        return "skip"
    # デフォルト
    else:
        return "neutral"

def convert_paragraph_to_json(content: str, para_id: str) -> Dict[str, Any]:
    """1つのパラグラフをJSON化"""
    para_html = extract_paragraph_html(content, para_id)
    if not para_html:
        return None
    
    # パラグラフ番号を抽出
    num_match = re.search(r'<span>([^<]+)</span>', para_html)
    number = num_match.group(1) if num_match else para_id
    
    # テキストを抽出
    text_match = re.search(r'<div class="para-body">(.*?)</div>', para_html, re.DOTALL)
    text_html = text_match.group(1) if text_match else ""
    
    # テキストを段落に分割
    paragraphs = []
    for p_match in re.finditer(r'<p>(.*?)</p>', text_html, re.DOTALL):
        para_text = clean_text(p_match.group(1))
        if para_text:
            paragraphs.append(para_text)
    
    # 選択肢を解析
    choices = parse_choices(para_html)
    
    # JSON構造を構築
    return {
        "id": para_id,
        "number": number,
        "text": paragraphs,
        "choices": choices,
        "meta": {
            "has_combat": any(c['type'] == 'combat' for c in choices),
            "has_luck_check": any(c['type'] == 'luck_check' for c in choices),
            "has_payment": any(c['type'] == 'pay_goto' for c in choices),
            "choice_count": len(choices)
        }
    }

def main():
    print("="*80)
    print("valdea legacy - 全パラグラフJSON変換")
    print("="*80)
    
    with open('game.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 全パラグラフIDを抽出
    all_ids = re.findall(r'<div class="para" id="([^"]+)">', content)
    
    print(f"\n全パラグラフ: {len(all_ids)}個")
    print("変換開始...\n")
    
    # 全パラグラフを変換
    paragraphs = {}
    for i, para_id in enumerate(all_ids, 1):
        para_json = convert_paragraph_to_json(content, para_id)
        if para_json:
            paragraphs[para_id] = para_json
            if i % 10 == 0:
                print(f"  {i}/{len(all_ids)} 完了")
    
    # JSON出力
    output = {
        "meta": {
            "version": "1.0.0",
            "style": "sorcery",
            "created": "2026-04-27",
            "total_paragraphs": len(paragraphs)
        },
        "paragraphs": paragraphs
    }
    
    with open('valdea_complete.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 変換完了: {len(paragraphs)}パラグラフ")
    print(f"出力: valdea_complete.json")
    
    # 統計情報
    total_choices = sum(len(p['choices']) for p in paragraphs.values())
    combat_paras = sum(1 for p in paragraphs.values() if p['meta']['has_combat'])
    
    print(f"\n【統計】")
    print(f"  総選択肢数: {total_choices}")
    print(f"  戦闘パラグラフ: {combat_paras}")
    print(f"  平均選択肢数: {total_choices/len(paragraphs):.1f}")

if __name__ == '__main__':
    main()
