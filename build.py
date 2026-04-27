#!/usr/bin/env python3
"""
valdea legacy - JSONビルドシステム
Sorcery!スタイル HTML生成 + リンク検証
"""

import json
import re
from typing import Dict, List, Set

class ValeaBuilder:
    def __init__(self, json_path: str, template_path: str):
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        with open(template_path, 'r', encoding='utf-8') as f:
            self.template = f.read()
        
        self.paragraphs = self.data['paragraphs']
        self.errors = []
        self.warnings = []
    
    def validate_links(self) -> bool:
        """リンク整合性を完全検証"""
        print("\n" + "="*80)
        print("リンク検証")
        print("="*80)
        
        all_ids = set(self.paragraphs.keys())
        referenced_ids = set()
        
        # 全選択肢のリンク先を収集
        for para_id, para in self.paragraphs.items():
            for choice in para.get('choices', []):
                target = choice.get('target')
                if target:
                    referenced_ids.add(target)
                    
                    # 存在チェック
                    if target not in all_ids:
                        self.errors.append(
                            f"❌ ◆{para_id} の選択肢 '{choice['label']}' "
                            f"が存在しないパラグラフ ◆{target} を参照"
                        )
        
        # 孤立パラグラフチェック（◆一以外で参照されていない）
        unreferenced = all_ids - referenced_ids - {'一'}
        if unreferenced:
            for para_id in sorted(unreferenced):
                self.warnings.append(
                    f"⚠️  ◆{para_id} はどこからも参照されていません（孤立）"
                )
        
        # 結果表示
        print(f"\n定義済みパラグラフ: {len(all_ids)}個")
        print(f"参照されているパラグラフ: {len(referenced_ids)}個")
        
        if self.errors:
            print(f"\n❌ エラー: {len(self.errors)}件")
            for err in self.errors[:10]:
                print(f"  {err}")
        else:
            print(f"\n✅ リンクエラー: 0件")
        
        if self.warnings:
            print(f"\n⚠️  警告: {len(self.warnings)}件")
            for warn in self.warnings[:5]:
                print(f"  {warn}")
        
        return len(self.errors) == 0
    
    def build_paragraph_html(self, para_id: str, para: Dict) -> str:
        """1つのパラグラフのHTML生成"""
        # テキスト部分
        text_html = []
        for text in para.get('text', []):
            text_html.append(f'<p>{text}</p>')
        
        # 選択肢部分
        choices_html = []
        for choice in para.get('choices', []):
            label = choice['label']
            action = choice['action']
            
            # Sorcery!スタイル: 選択肢の性格をクラスで表現
            weight = choice.get('weight', 'neutral')
            choice_class = f'choice-btn choice-{weight}'
            
            choices_html.append(
                f'<button class="{choice_class}" onclick="{action}">{label}</button>'
            )
        
        # パラグラフHTML組み立て
        return f'''<div class="para" id="{para_id}">
  <div class="para-num">◆ <span>{para['number']}</span></div>
  <div class="para-body">
    {''.join(text_html)}
  </div>
  <div class="choices">
    {''.join(choices_html)}
  </div>
</div>'''
    
    def build_all_paragraphs(self) -> str:
        """全パラグラフのHTML生成"""
        print("\n" + "="*80)
        print("HTML生成")
        print("="*80)
        
        html_parts = []
        for para_id in sorted(self.paragraphs.keys()):
            para = self.paragraphs[para_id]
            html_parts.append(self.build_paragraph_html(para_id, para))
        
        print(f"\n✅ {len(html_parts)}パラグラフのHTML生成完了")
        return '\n\n'.join(html_parts)
    
    def inject_into_template(self, paragraphs_html: str) -> str:
        """テンプレートにパラグラフHTMLを注入"""
        # テンプレート内の<!-- PARAGRAPHS -->マーカーを置換
        if '<!-- PARAGRAPHS -->' in self.template:
            return self.template.replace('<!-- PARAGRAPHS -->', paragraphs_html)
        else:
            # マーカーがない場合、既存のパラグラフセクションを置換
            pattern = r'<div class="para" id="一">.*?</body>'
            return re.sub(pattern, paragraphs_html + '\n</body>', 
                         self.template, flags=re.DOTALL)
    
    def build(self, output_path: str) -> bool:
        """完全ビルド実行"""
        print("="*80)
        print("valdea legacy - ビルド開始")
        print("="*80)
        
        # リンク検証
        if not self.validate_links():
            print("\n❌ ビルド失敗: リンクエラーを修正してください")
            return False
        
        # HTML生成
        paragraphs_html = self.build_all_paragraphs()
        
        # テンプレート注入
        final_html = self.inject_into_template(paragraphs_html)
        
        # 出力
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        print(f"\n✅ ビルド完了: {output_path}")
        print(f"   ファイルサイズ: {len(final_html)/1024:.1f} KB")
        
        return True

def main():
    builder = ValeaBuilder('valdea_complete.json', 'game.html')
    success = builder.build('game_rebuilt.html')
    
    if success:
        print("\n" + "="*80)
        print("✅ ビルド成功")
        print("="*80)
    else:
        print("\n" + "="*80)
        print("❌ ビルド失敗")
        print("="*80)

if __name__ == '__main__':
    main()
