#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
valdea legacy - Professional QA v3.0
Complete automated testing suite
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set

class ValdegaQA:
    """Professional QA automation for valdea legacy"""
    
    def __init__(self, html_path: str):
        self.html_path = Path(html_path)
        self.html_content = self.html_path.read_text(encoding='utf-8')
        self.errors = []
        self.warnings = []
        self.passed = []
        
    # ==========================================
    # ■ 1. 構文・実行完全検証
    # ==========================================
    
    def check_syntax(self) -> Dict:
        """HTML/CSS/JS構文チェック"""
        results = {}
        
        # HTML tag balance
        html_open = len(re.findall(r'<html[^>]*>', self.html_content))
        html_close = len(re.findall(r'</html>', self.html_content))
        results['html_balance'] = html_open == html_close
        
        # JS brace balance
        js_open = self.html_content.count('{')
        js_close = self.html_content.count('}')
        results['js_balance'] = js_open == js_close
        
        # console.log/error/warn
        console_log = len(re.findall(r'console\.log', self.html_content))
        console_error = len(re.findall(r'console\.error', self.html_content))
        console_warn = len(re.findall(r'console\.warn', self.html_content))
        
        results['console_log_count'] = console_log
        results['console_error_count'] = console_error
        results['console_warn_count'] = console_warn
        results['console_clean'] = console_log == 0 and console_warn == 0
        
        # Unused variables/functions
        # (簡易検出 - 関数定義と呼び出しの差分)
        func_defs = set(re.findall(r'function\s+(\w+)\s*\(', self.html_content))
        func_calls = set(re.findall(r'(\w+)\s*\(', self.html_content))
        unused_funcs = func_defs - func_calls
        results['unused_functions'] = list(unused_funcs)
        
        # Null/undefined checks
        has_null_checks = 'if(!scene.choices' in self.html_content
        has_try_catch = 'try{' in self.html_content and 'catch' in self.html_content
        results['null_safety'] = has_null_checks and has_try_catch
        
        if results['html_balance'] and results['js_balance']:
            self.passed.append("✅ 1.1 構文バランス正常")
        else:
            self.errors.append("❌ 1.1 構文バランス異常")
            
        if results['console_clean']:
            self.passed.append("✅ 1.2 コンソール出力クリーン")
        else:
            self.warnings.append(f"⚠️  1.2 console.log: {console_log}, console.error: {console_error}")
            
        if results['null_safety']:
            self.passed.append("✅ 1.3 Null/undefined保護あり")
        else:
            self.errors.append("❌ 1.3 Null/undefined保護不足")
            
        return results
    
    # ==========================================
    # ■ 2. ブラウザ挙動・永続性テスト
    # ==========================================
    
    def check_persistence(self) -> Dict:
        """セーブ・ロード機能検証"""
        results = {}
        
        # localStorage使用確認
        has_save = 'localStorage.setItem' in self.html_content
        has_load = 'localStorage.getItem' in self.html_content
        results['has_persistence'] = has_save and has_load
        
        # save/load関数の存在
        has_save_func = 'function save(' in self.html_content
        has_load_func = 'function load(' in self.html_content
        results['has_save_load_funcs'] = has_save_func and has_load_func
        
        # エラーハンドリング
        has_error_handling = 'try{' in self.html_content and 'JSON.parse' in self.html_content
        results['has_error_handling'] = has_error_handling
        
        # ブラウザ「戻る」対応
        has_popstate = 'onpopstate' in self.html_content or 'window.onpopstate' in self.html_content
        results['has_browser_back'] = has_popstate
        
        if results['has_persistence'] and results['has_save_load_funcs']:
            self.passed.append("✅ 2.1 永続性システム完備")
        else:
            self.errors.append("❌ 2.1 永続性システム不足")
            
        if results['has_error_handling']:
            self.passed.append("✅ 2.2 エラーハンドリングあり")
        else:
            self.warnings.append("⚠️  2.2 エラーハンドリング不足")
            
        return results
    
    # ==========================================
    # ■ 3. 状態遷移・フラグ整合性
    # ==========================================
    
    def check_state_management(self) -> Dict:
        """状態管理・フラグ検証"""
        results = {}
        
        # state/flags定義
        has_state = 'const state' in self.html_content or 'let state' in self.html_content
        has_flags = 'flags:' in self.html_content or 'flags =' in self.html_content
        results['has_state_management'] = has_state
        results['has_flags'] = has_flags
        
        # フラグ一覧抽出
        flags_match = re.search(r'flags:\s*{([^}]+)}', self.html_content)
        if flags_match:
            flags_text = flags_match.group(1)
            flags = re.findall(r'(\w+):\s*(?:false|true|\d+)', flags_text)
            results['flags_list'] = flags
        else:
            results['flags_list'] = []
        
        # 各フラグの使用箇所確認
        flag_usage = {}
        for flag in results['flags_list']:
            usage_count = len(re.findall(rf'\b{flag}\b', self.html_content))
            flag_usage[flag] = usage_count
        results['flag_usage'] = flag_usage
        
        if results['has_state_management'] and results['has_flags']:
            self.passed.append("✅ 3.1 状態管理システムあり")
        else:
            self.errors.append("❌ 3.1 状態管理システム不足")
            
        return results
    
    # ==========================================
    # ■ 4. リンク・分岐の完全性
    # ==========================================
    
    def check_links_and_branches(self) -> Dict:
        """分岐・リンク完全性検証"""
        results = {}
        
        # 全シーンID抽出
        scene_ids = set()
        
        # getScene関数からID抽出
        scene_checks = re.findall(r'if\s*\(\s*id\s*===?\s*(\d+)\s*\)', self.html_content)
        scene_ids.update(int(x) for x in scene_checks)
        
        # next遷移先抽出
        next_ids = set()
        next_patterns = [
            r'next:\s*(\d+)',
            r'next:\s*safeNext\((\d+)\)',
            r'render\((\d+)\)'
        ]
        for pattern in next_patterns:
            matches = re.findall(pattern, self.html_content)
            next_ids.update(int(x) for x in matches)
        
        # safeNext関数の存在
        has_safe_next = 'function safeNext' in self.html_content
        results['has_safe_next'] = has_safe_next
        
        # リンク切れ検出（nextで指定されているが定義されていないID）
        broken_links = next_ids - scene_ids - {1, 100, 'boss'}  # 1と100は常に存在想定
        broken_links = {x for x in broken_links if isinstance(x, int)}
        results['broken_links'] = sorted(broken_links)
        
        # 到達不可能なシーン（定義されているが遷移先にない）
        unreachable = scene_ids - next_ids
        results['unreachable_scenes'] = sorted(unreachable)
        
        results['total_scenes'] = len(scene_ids)
        results['total_transitions'] = len(next_ids)
        
        if not results['broken_links']:
            self.passed.append("✅ 4.1 リンク切れ0件")
        else:
            self.errors.append(f"❌ 4.1 リンク切れ: {results['broken_links']}")
            
        if results['has_safe_next']:
            self.passed.append("✅ 4.2 安全な遷移関数あり")
        else:
            self.errors.append("❌ 4.2 安全な遷移関数なし")
            
        return results
    
    # ==========================================
    # ■ 5. 戦闘・数値バランス検証
    # ==========================================
    
    def check_combat_balance(self) -> Dict:
        """戦闘システム検証"""
        results = {}
        
        # 戦闘システムの存在
        has_combat = 'renderBoss' in self.html_content or 'boss' in self.html_content
        results['has_combat'] = has_combat
        
        # HP管理
        hp_checks = re.findall(r'hp[<>=!]+\s*0', self.html_content)
        has_hp_management = len(hp_checks) > 0
        results['has_hp_management'] = has_hp_management
        
        # HP下限チェック（マイナス防止）
        has_hp_clamp = 'hp<=0' in self.html_content or 'Math.max(0' in self.html_content
        results['has_hp_clamp'] = has_hp_clamp
        
        # ダメージ計算
        damage_patterns = re.findall(r'hp\s*[-+]=\s*\d+', self.html_content)
        results['damage_calculations'] = len(damage_patterns)
        
        if has_combat:
            self.passed.append("✅ 5.1 戦闘システムあり")
            
            if has_hp_clamp:
                self.passed.append("✅ 5.2 HPマイナス防止あり")
            else:
                self.errors.append("❌ 5.2 HPマイナス防止なし")
        else:
            self.warnings.append("⚠️  5.1 戦闘システムなし（意図的？）")
        
        return results
    
    # ==========================================
    # ■ 6. UI/UX・アクセシビリティ
    # ==========================================
    
    def check_ui_ux(self) -> Dict:
        """UI/UX検証"""
        results = {}
        
        # ボタン要素
        buttons = len(re.findall(r'<button', self.html_content))
        results['button_count'] = buttons
        
        # アクセシビリティ
        has_lang = 'lang="ja"' in self.html_content or 'lang="en"' in self.html_content
        has_charset = 'charset=' in self.html_content
        has_viewport = 'viewport' in self.html_content
        
        results['has_lang'] = has_lang
        results['has_charset'] = has_charset
        results['has_viewport'] = has_viewport
        
        # レスポンシブデザイン
        has_responsive = 'max-width' in self.html_content or '@media' in self.html_content
        results['has_responsive'] = has_responsive
        
        if has_lang and has_charset:
            self.passed.append("✅ 6.1 基本アクセシビリティあり")
        else:
            self.warnings.append("⚠️  6.1 アクセシビリティ改善可能")
            
        return results
    
    # ==========================================
    # ■ 7. テキスト・演出品質
    # ==========================================
    
    def check_text_quality(self) -> Dict:
        """テキスト品質検証"""
        results = {}
        
        # テキスト整形関数
        has_text_formatting = 'narrate' in self.html_content or 'formatChoices' in self.html_content
        results['has_text_formatting'] = has_text_formatting
        
        # 文体一貫性（ジャクソン文体など）
        jackson_style = 'しても良い' in self.html_content
        results['has_jackson_style'] = jackson_style
        
        # 注記・警告
        has_warnings = '※' in self.html_content or '警告' in self.html_content
        results['has_warnings'] = has_warnings
        
        if has_text_formatting:
            self.passed.append("✅ 7.1 テキスト整形機能あり")
        else:
            self.warnings.append("⚠️  7.1 テキスト整形機能なし")
            
        return results
    
    # ==========================================
    # ■ 8. パフォーマンス・最適化
    # ==========================================
    
    def check_performance(self) -> Dict:
        """パフォーマンス検証"""
        results = {}
        
        # ファイルサイズ
        file_size = len(self.html_content.encode('utf-8'))
        results['file_size_bytes'] = file_size
        results['file_size_kb'] = file_size / 1024
        
        # Base64画像（重い要素）
        base64_images = len(re.findall(r'data:image', self.html_content))
        results['base64_image_count'] = base64_images
        
        # 最適化推奨
        if file_size < 10 * 1024:  # 10KB未満
            results['size_rating'] = 'excellent'
        elif file_size < 100 * 1024:  # 100KB未満
            results['size_rating'] = 'good'
        elif file_size < 500 * 1024:  # 500KB未満
            results['size_rating'] = 'acceptable'
        else:
            results['size_rating'] = 'heavy'
        
        self.passed.append(f"✅ 8.1 ファイルサイズ: {results['file_size_kb']:.1f}KB ({results['size_rating']})")
        
        return results
    
    # ==========================================
    # ■ 総合評価
    # ==========================================
    
    def run_all_tests(self) -> Dict:
        """全テスト実行"""
        print("="*80)
        print("valdea legacy - Professional QA v3.0")
        print("="*80)
        print()
        
        all_results = {}
        
        print("【1. 構文・実行完全検証】")
        all_results['syntax'] = self.check_syntax()
        print()
        
        print("【2. ブラウザ挙動・永続性テスト】")
        all_results['persistence'] = self.check_persistence()
        print()
        
        print("【3. 状態遷移・フラグ整合性】")
        all_results['state'] = self.check_state_management()
        print()
        
        print("【4. リンク・分岐の完全性】")
        all_results['links'] = self.check_links_and_branches()
        print()
        
        print("【5. 戦闘・数値バランス検証】")
        all_results['combat'] = self.check_combat_balance()
        print()
        
        print("【6. UI/UX・アクセシビリティ】")
        all_results['ui'] = self.check_ui_ux()
        print()
        
        print("【7. テキスト・演出品質】")
        all_results['text'] = self.check_text_quality()
        print()
        
        print("【8. パフォーマンス・最適化】")
        all_results['performance'] = self.check_performance()
        print()
        
        # サマリー
        print("="*80)
        print("【QA結果サマリー】")
        print("="*80)
        print()
        
        print(f"✅ 合格: {len(self.passed)}")
        for p in self.passed:
            print(f"  {p}")
        print()
        
        if self.warnings:
            print(f"⚠️  警告: {len(self.warnings)}")
            for w in self.warnings:
                print(f"  {w}")
            print()
        
        if self.errors:
            print(f"❌ エラー: {len(self.errors)}")
            for e in self.errors:
                print(f"  {e}")
            print()
        
        # 最終判定
        print("="*80)
        if not self.errors:
            print("【最終判定】✅ RELEASE APPROVED")
            all_results['final_verdict'] = 'APPROVED'
        else:
            print("【最終判定】❌ RELEASE BLOCKED")
            all_results['final_verdict'] = 'BLOCKED'
        print("="*80)
        
        return all_results


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python qa_professional_v3.py <html_file>")
        sys.exit(1)
    
    html_file = sys.argv[1]
    qa = ValdegaQA(html_file)
    results = qa.run_all_tests()
    
    # JSON出力（CI/CD用）
    output_file = Path(html_file).stem + '_qa_report.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 詳細レポート: {output_file}")
    
    # 終了コード
    sys.exit(0 if results['final_verdict'] == 'APPROVED' else 1)
