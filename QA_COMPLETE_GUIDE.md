# valdea legacy - Professional QA v3.0 Complete Guide
# プロフェッショナルQA v3.0 完全ガイド

---

## 🎯 Overview / 概要

**Professional QA v3.0** provides complete automated testing for valdea legacy.

**プロフェッショナルQA v3.0**は、valdea legacyの完全自動テストを提供します。

---

## 📦 Package Contents / パッケージ内容

```
valdea-legacy-FINAL/
├── game.html                        # Main game (フル版ゲーム)
├── game-minimal.html                # Minimal version (ミニマル版)
├── index.html                       # Top page (トップページ)
├── guide.html                       # Play guide (遊び方ガイド)
├── README.md                        # Repository info (リポジトリ情報)
├── .gitignore                       # Git exclusions (Git除外設定)
│
├── .github/workflows/
│   └── qa.yml                       # GitHub Actions workflow
│
└── qa/                              # QA automation tools
    ├── README.md                    # QA documentation
    ├── qa_professional_v3.py        # Main QA script (8項目対応)
    ├── branch_map_visualizer.py     # Branch map generator
    └── reports/                     # Generated reports
```

---

## 🚀 Quick Start / クイックスタート

### Local QA Execution / ローカルQA実行

```bash
# Test a single file / 単一ファイルをテスト
python qa/qa_professional_v3.py game-minimal.html

# Generate branch map / 分岐マップ生成
python qa/branch_map_visualizer.py game-minimal.html qa/reports

# Test all HTML files / すべてのHTMLをテスト
for file in *.html; do
  python qa/qa_professional_v3.py "$file"
done
```

---

## ✅ QA Test Items / QA検証項目

### 1. Syntax & Execution / 構文・実行完全検証
- ✅ HTML/CSS/JS syntax validation
- ✅ Console error detection (0 errors required)
- ✅ Unused code detection
- ✅ Null/undefined safety checks

### 2. Browser Behavior / ブラウザ挙動・永続性
- ✅ Save/load functionality
- ✅ F5 reload resistance
- ✅ Browser back button support
- ✅ Session persistence

### 3. State Management / 状態遷移・フラグ整合性
- ✅ Game state management
- ✅ Flag consistency
- ✅ State transition validation

### 4. Links & Branches / リンク・分岐の完全性
- ✅ Broken link detection
- ✅ Unreachable scene detection
- ✅ Dead-end detection
- ✅ Transition safety (safeNext validation)

### 5. Combat Balance / 戦闘・数値バランス
- ✅ Combat system validation
- ✅ HP underflow prevention
- ✅ Damage calculation checks

### 6. UI/UX & Accessibility / UI/UX・アクセシビリティ
- ✅ Language tag validation
- ✅ Charset declaration
- ✅ Viewport meta tag
- ✅ Responsive design check

### 7. Text Quality / テキスト・演出品質
- ✅ Text formatting functions
- ✅ Style consistency (e.g., Jackson style)
- ✅ Warning messages

### 8. Performance / パフォーマンス・最適化
- ✅ File size analysis
- ✅ Base64 image count
- ✅ Optimization recommendations

---

## 📊 Understanding QA Results / QA結果の見方

### ✅ RELEASE APPROVED / リリース許可

**All tests passed. Ready for immediate release.**

**すべてのテストをパス。即座にリリース可能です。**

Example output / 出力例:
```
【最終判定】✅ RELEASE APPROVED
```

---

### ❌ RELEASE BLOCKED / リリースブロック

**Errors detected. Fixes required before release.**

**エラーが検出されました。修正が必要です。**

Example output / 出力例:
```
【最終判定】❌ RELEASE BLOCKED

❌ エラー: 1
  ❌ 4.1 リンク切れ: [41, 42, 46, 47]
```

---

## 🔄 GitHub Actions Integration / GitHub Actions統合

### Automatic Triggers / 自動トリガー

The QA workflow runs automatically on:

QAワークフローは以下で自動実行されます:

- ✅ Push to `main` or `develop` branch
- ✅ Pull Request creation
- ✅ Any `.html`, `.js`, or `.css` file changes

### Workflow Steps / ワークフローステップ

1. **Checkout code** / コードチェックアウト
2. **Run QA v3.0** / QA v3.0実行
3. **Generate branch maps** / 分岐マップ生成
4. **Upload reports** / レポートアップロード
5. **Comment on PR** / PRにコメント
6. **Block if failed** / 失敗時はブロック
7. **Deploy if passed** / 成功時は自動デプロイ

---

## 📈 Branch Map Visualization / 分岐マップ可視化

### Output Formats / 出力形式

1. **Mermaid** (`branch_map.mermaid.md`)
   - GitHub native support
   - Markdown-embeddable
   - Interactive on GitHub

2. **Graphviz DOT** (`branch_map.dot`)
   - Professional diagrams
   - Requires Graphviz
   ```bash
   dot -Tpng branch_map.dot -o branch_map.png
   ```

3. **Interactive HTML** (`branch_map.html`)
   - Click to jump between scenes
   - Bug highlighting
   - Statistics display

---

## 🐛 Bug Detection / バグ検出

### Automatic Detection / 自動検出項目

✅ **Broken Links** / リンク切れ
- Detects transitions to undefined scenes
- Example: `next: 999` when scene 999 doesn't exist

✅ **Unreachable Scenes** / 到達不可能シーン
- Detects scenes with no incoming transitions
- Example: Scene 50 defined but never referenced

✅ **Dead Ends** / 行き止まり
- Detects scenes with no choices (except ending)
- Example: Scene 75 has no `choices` array

---

## 🎯 Release Criteria / 最終リリース判定基準

**BLOCK release if ANY of these are true:**

**以下の1つでも該当する場合、リリース不可:**

❌ **Dead-end route exists** / 詰みルートが存在
❌ **Numerical bugs** (e.g., negative HP) / 数値バグ（HPマイナス等）
❌ **Player gets lost** / UIで迷子になる
❌ **Pure luck-based gameplay** / 判断の介在しない運ゲー

---

## 🔧 Advanced Usage / 高度な使い方

### Custom QA Configuration / カスタムQA設定

Edit `qa_professional_v3.py` to customize:

`qa_professional_v3.py`を編集してカスタマイズ:

```python
# Modify thresholds
results['size_rating'] = 'good' if file_size < 100 * 1024 else 'heavy'

# Add custom checks
def check_custom(self):
    # Your custom validation
    pass
```

---

### CI/CD Integration / CI/CD統合

**GitHub Actions** (included) / 含まれています

**Other CI/CD:**
```yaml
# GitLab CI example
test:
  script:
    - python qa/qa_professional_v3.py game.html
  artifacts:
    paths:
      - "*_qa_report.json"
```

---

## 📝 QA Report Format / QAレポート形式

### JSON Output / JSON出力

```json
{
  "syntax": {
    "html_balance": true,
    "js_balance": true,
    "console_clean": true,
    "null_safety": true
  },
  "links": {
    "broken_links": [],
    "total_scenes": 100,
    "total_transitions": 200
  },
  "final_verdict": "APPROVED"
}
```

---

## 🚀 Deployment Workflow / デプロイワークフロー

```
1. Developer pushes code
   ↓
2. GitHub Actions triggers QA
   ↓
3. QA runs all 8 test categories
   ↓
4. Branch map generated
   ↓
5. If APPROVED → Auto-deploy to GitHub Pages
   If BLOCKED → Notify developer
```

---

## 📚 Additional Resources / 追加リソース

- **QA Documentation:** `qa/README.md`
- **GitHub Actions:** `.github/workflows/qa.yml`
- **Branch Maps:** `qa/reports/`
- **Main README:** `README.md`

---

## ✅ Best Practices / ベストプラクティス

### Before Commit / コミット前

```bash
# Run QA locally
python qa/qa_professional_v3.py game.html

# Check for errors
if [ $? -eq 0 ]; then
  echo "✅ QA PASSED"
  git commit -m "Update game"
else
  echo "❌ QA FAILED - Fix errors first"
fi
```

### Regular Testing / 定期テスト

- ✅ Run QA after every major change
- ✅ Generate branch maps weekly
- ✅ Review unreachable scenes monthly

---

## 🎉 Success Metrics / 成功指標

**Zero-bug release achieved when:**

**バグゼロリリース達成条件:**

✅ All 8 QA categories pass
✅ No broken links detected
✅ No unreachable scenes
✅ No dead ends (except endings)
✅ All numerical checks pass
✅ Performance within acceptable range

---

**valdea legacy - Professional QA v3.0**  
*Complete automated testing for zero-bug guarantee*  
*完全自動化テストによるバグゼロ保証*

---

**Version:** v3.0 COMPLETE  
**Last Updated:** 2026-04-30  
**Status:** ✅ PRODUCTION READY
