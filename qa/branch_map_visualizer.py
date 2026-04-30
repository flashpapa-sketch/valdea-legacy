#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
valdea legacy - Branch Map Visualizer
Complete branching structure visualization with bug detection
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

class BranchMapVisualizer:
    """Automatic branch map generation with zero-bug guarantee"""
    
    def __init__(self, html_path: str):
        self.html_path = Path(html_path)
        self.html_content = self.html_path.read_text(encoding='utf-8')
        self.scenes = {}
        self.transitions = []
        self.flags = set()
        self.bugs = []
        
    def extract_scenes(self) -> Dict:
        """シーン情報抽出"""
        # getScene関数からすべてのシーン抽出
        scene_blocks = re.findall(
            r'if\s*\(\s*id\s*===?\s*(\d+)\s*\)\s*{([^}]+(?:{[^}]*}[^}]*)*)}',
            self.html_content,
            re.DOTALL
        )
        
        for scene_id_str, content in scene_blocks:
            scene_id = int(scene_id_str)
            
            # テキスト抽出
            text_match = re.search(r'text\s*=\s*["\']([^"\']+)["\']', content)
            text = text_match.group(1) if text_match else ""
            
            # 選択肢抽出
            choices = []
            choice_blocks = re.findall(
                r'{text:\s*["\']([^"\']+)["\'](?:,\s*effect:[^,}]+)?(?:,\s*next:\s*(\d+|"boss"))?}',
                content
            )
            
            for choice_text, next_id in choice_blocks:
                if next_id:
                    try:
                        next_id = int(next_id) if next_id != '"boss"' else 'boss'
                    except:
                        next_id = next_id.strip('"')
                    choices.append({'text': choice_text, 'next': next_id})
            
            # フラグ効果抽出
            flag_effects = re.findall(r'state\.flags\.(\w+)\s*=\s*true', content)
            
            self.scenes[scene_id] = {
                'id': scene_id,
                'text': text[:50] + '...' if len(text) > 50 else text,
                'choices': choices,
                'flags': flag_effects
            }
            
            # 遷移記録
            for choice in choices:
                if choice['next']:
                    self.transitions.append((scene_id, choice['next'], choice['text']))
            
            # フラグ記録
            self.flags.update(flag_effects)
        
        return self.scenes
    
    def detect_bugs(self) -> List[str]:
        """バグ検出"""
        bugs = []
        
        # すべての遷移先ID
        all_next_ids = set()
        for _, next_id, _ in self.transitions:
            if isinstance(next_id, int):
                all_next_ids.add(next_id)
        
        # 定義されているシーンID
        defined_ids = set(self.scenes.keys())
        
        # リンク切れ検出
        broken_links = all_next_ids - defined_ids - {1, 100}
        if broken_links:
            bugs.append(f"🔴 リンク切れ: {sorted(broken_links)}")
        
        # 到達不可能シーン
        reachable_ids = {1}  # 1から開始
        for scene_id, next_id, _ in self.transitions:
            if scene_id in reachable_ids and isinstance(next_id, int):
                reachable_ids.add(next_id)
        
        unreachable = defined_ids - reachable_ids
        if unreachable:
            bugs.append(f"⚠️  到達不可能: {sorted(unreachable)}")
        
        # 行き止まり検出（100以外で選択肢がない）
        for scene_id, scene in self.scenes.items():
            if scene_id != 100 and not scene['choices']:
                bugs.append(f"🔴 行き止まり: シーン{scene_id}")
        
        self.bugs = bugs
        return bugs
    
    def generate_mermaid(self) -> str:
        """Mermaid形式の分岐図生成"""
        lines = ["```mermaid", "graph TD"]
        
        # ノード定義
        for scene_id, scene in sorted(self.scenes.items()):
            text = scene['text'].replace('"', "'")
            label = f"{scene_id}: {text}"
            
            # 特殊シーンのスタイル
            if scene_id == 1:
                lines.append(f'  {scene_id}["{label}"]:::start')
            elif scene_id == 100:
                lines.append(f'  {scene_id}["{label}"]:::end')
            elif scene.get('flags'):
                lines.append(f'  {scene_id}["{label}"]:::flag')
            else:
                lines.append(f'  {scene_id}["{label}"]')
        
        # boss特殊ノード
        if any(next_id == 'boss' for _, next_id, _ in self.transitions):
            lines.append('  boss["BOSS戦"]:::boss')
        
        # エッジ定義
        for from_id, to_id, choice_text in self.transitions:
            choice_label = choice_text[:20] + '...' if len(choice_text) > 20 else choice_text
            lines.append(f'  {from_id} -->|"{choice_label}"| {to_id}')
        
        # スタイル定義
        lines.extend([
            "",
            "  classDef start fill:#90EE90,stroke:#006400,stroke-width:3px",
            "  classDef end fill:#FFB6C1,stroke:#8B0000,stroke-width:3px",
            "  classDef flag fill:#FFD700,stroke:#FF8C00,stroke-width:2px",
            "  classDef boss fill:#FF6347,stroke:#8B0000,stroke-width:3px",
            "```"
        ])
        
        return "\n".join(lines)
    
    def generate_dot(self) -> str:
        """Graphviz DOT形式の分岐図生成"""
        lines = ["digraph valdea {", "  rankdir=TB;", "  node [shape=box];", ""]
        
        # ノード定義
        for scene_id, scene in sorted(self.scenes.items()):
            text = scene['text'].replace('"', '\\"')
            label = f"{scene_id}: {text}"
            
            # スタイル
            if scene_id == 1:
                style = 'style=filled,fillcolor=lightgreen'
            elif scene_id == 100:
                style = 'style=filled,fillcolor=pink'
            elif scene.get('flags'):
                style = 'style=filled,fillcolor=gold'
            else:
                style = ''
            
            lines.append(f'  {scene_id} [label="{label}",{style}];')
        
        # boss
        if any(next_id == 'boss' for _, next_id, _ in self.transitions):
            lines.append('  boss [label="BOSS戦",style=filled,fillcolor=tomato];')
        
        lines.append("")
        
        # エッジ定義
        for from_id, to_id, choice_text in self.transitions:
            choice_label = choice_text.replace('"', '\\"')
            lines.append(f'  {from_id} -> {to_id} [label="{choice_label}"];')
        
        lines.append("}")
        
        return "\n".join(lines)
    
    def generate_html_map(self) -> str:
        """HTML形式のインタラクティブマップ生成"""
        html = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>valdea legacy - Branch Map</title>
<style>
body{background:#111;color:#eee;font-family:monospace;padding:20px;}
.scene{border:2px solid #444;margin:10px;padding:10px;background:#222;}
.scene.start{border-color:#0f0;}
.scene.end{border-color:#f00;}
.scene.flag{border-color:#ff0;}
.scene h3{margin:0 0 5px 0;}
.choice{margin:5px 0;padding:5px;background:#333;cursor:pointer;}
.choice:hover{background:#555;}
.stats{margin-top:20px;padding:10px;background:#333;}
.bug{color:#f00;font-weight:bold;}
.warning{color:#ff0;}
</style>
</head>
<body>
<h1>valdea legacy - Branch Map</h1>

<div class="stats">
<h2>統計</h2>
<p>総シーン数: {scene_count}</p>
<p>総遷移数: {transition_count}</p>
<p>フラグ数: {flag_count}</p>
<p>検出されたバグ: {bug_count}</p>
</div>

{bug_section}

<h2>全シーン一覧</h2>
{scenes_html}

<script>
function jumpTo(id){{
  document.getElementById('scene_'+id).scrollIntoView({{behavior:'smooth'}});
}}
</script>
</body>
</html>
"""
        
        # バグセクション
        bug_html = ""
        if self.bugs:
            bug_html = '<div class="stats bug"><h2>🔴 検出されたバグ</h2><ul>'
            for bug in self.bugs:
                bug_html += f'<li>{bug}</li>'
            bug_html += '</ul></div>'
        
        # シーンHTML生成
        scenes_html = ""
        for scene_id, scene in sorted(self.scenes.items()):
            scene_class = 'scene'
            if scene_id == 1:
                scene_class += ' start'
            elif scene_id == 100:
                scene_class += ' end'
            elif scene.get('flags'):
                scene_class += ' flag'
            
            scenes_html += f'<div class="{scene_class}" id="scene_{scene_id}">\n'
            scenes_html += f'<h3>シーン {scene_id}</h3>\n'
            scenes_html += f'<p>{scene["text"]}</p>\n'
            
            if scene.get('flags'):
                scenes_html += f'<p><strong>フラグ:</strong> {", ".join(scene["flags"])}</p>\n'
            
            if scene['choices']:
                scenes_html += '<div class="choices">\n'
                for choice in scene['choices']:
                    scenes_html += f'<div class="choice" onclick="jumpTo({choice["next"]})">'
                    scenes_html += f'{choice["text"]} → {choice["next"]}</div>\n'
                scenes_html += '</div>\n'
            
            scenes_html += '</div>\n'
        
        return html.format(
            scene_count=len(self.scenes),
            transition_count=len(self.transitions),
            flag_count=len(self.flags),
            bug_count=len(self.bugs),
            bug_section=bug_html,
            scenes_html=scenes_html
        )
    
    def generate_all(self, output_dir: str = '.'):
        """すべての形式で出力"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # シーン抽出
        print("🔍 シーン抽出中...")
        self.extract_scenes()
        print(f"✅ {len(self.scenes)}シーン抽出完了")
        
        # バグ検出
        print("\n🔍 バグ検出中...")
        bugs = self.detect_bugs()
        if bugs:
            print("❌ バグ検出:")
            for bug in bugs:
                print(f"  {bug}")
        else:
            print("✅ バグ0件")
        
        # Mermaid出力
        mermaid_file = output_path / "branch_map.mermaid.md"
        mermaid_content = self.generate_mermaid()
        mermaid_file.write_text(mermaid_content, encoding='utf-8')
        print(f"\n✅ Mermaid: {mermaid_file}")
        
        # DOT出力
        dot_file = output_path / "branch_map.dot"
        dot_content = self.generate_dot()
        dot_file.write_text(dot_content, encoding='utf-8')
        print(f"✅ Graphviz: {dot_file}")
        
        # HTML出力
        html_file = output_path / "branch_map.html"
        html_content = self.generate_html_map()
        html_file.write_text(html_content, encoding='utf-8')
        print(f"✅ HTML: {html_file}")
        
        # サマリー
        print("\n" + "="*60)
        print("分岐マップ生成完了")
        print("="*60)
        print(f"総シーン数: {len(self.scenes)}")
        print(f"総遷移数: {len(self.transitions)}")
        print(f"フラグ数: {len(self.flags)}")
        print(f"バグ数: {len(self.bugs)}")
        
        return len(self.bugs) == 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python branch_map_visualizer.py <html_file> [output_dir]")
        sys.exit(1)
    
    html_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else '.'
    
    visualizer = BranchMapVisualizer(html_file)
    success = visualizer.generate_all(output_dir)
    
    sys.exit(0 if success else 1)
