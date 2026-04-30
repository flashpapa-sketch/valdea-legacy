# valdea legacy - Professional QA v3.0

## 📋 概要

本ディレクトリには、プロフェッショナルQA v3.0の完全自動化ツールが含まれています。

---

## 🛠️ ツール一覧

### 1. qa_professional_v3.py
**8項目完全対応のQA自動化スクリプト**

✅ 1. 構文・実行完全検証
✅ 2. ブラウザ挙動・永続性テスト
✅ 3. 状態遷移・フラグ整合性
✅ 4. リンク・分岐の完全性
✅ 5. 戦闘・数値バランス検証
✅ 6. UI/UX・アクセシビリティ
✅ 7. テキスト・演出品質
✅ 8. パフォーマンス・最適化

**使い方:**
```bash
python qa/qa_professional_v3.py game-minimal.html
```

**出力:**
- コンソール: QA結果レポート
- ファイル: `*_qa_report.json`

---

### 2. branch_map_visualizer.py
**分岐マップ自動可視化ツール（バグ0保証）**

**機能:**
- 全シーン抽出
- 全遷移抽出
- リンク切れ検出
- 到達不可能シーン検出
- 行き止まり検出

**使い方:**
```bash
python qa/branch_map_visualizer.py game-minimal.html qa/reports
```

**出力:**
- `branch_map.mermaid.md` - Mermaid形式
- `branch_map.dot` - Graphviz形式
- `branch_map.html` - インタラクティブHTML

---

## 🚀 GitHub Actions統合

`.github/workflows/qa.yml` により、以下が自動実行されます：

**トリガー:**
- `main` / `develop` ブランチへのpush
- Pull Request作成時

**実行内容:**
1. ✅ プロフェッショナルQA v3.0実行
2. ✅ 分岐マップ生成
3. ✅ QAレポートアップロード
4. ✅ PR にコメント投稿
5. ✅ QA失敗時はブロック
6. ✅ QA成功時は自動デプロイ

---

## 📊 QA結果の見方

### ✅ RELEASE APPROVED
**すべての項目をパス。即座にリリース可能です。**

### ❌ RELEASE BLOCKED
**エラーが検出されました。修正が必要です。**

---

## 🔧 ローカルでのQA実行

```bash
# すべてのHTMLファイルをテスト
for file in *.html; do
  python qa/qa_professional_v3.py "$file"
done

# 分岐マップ生成
python qa/branch_map_visualizer.py game.html qa/reports
```

---

## 📝 最終リリース判定基準

以下の1つでも該当する場合、リリース不可：

❌ 詰みルートが1箇所でもある
❌ 数値バグ（HPマイナス等）が発生する
❌ UIで迷子になる
❌ 判断の介在しない運ゲーに終始

---

**valdea legacy - Professional QA v3.0**  
*Complete automated testing for zero-bug guarantee*
