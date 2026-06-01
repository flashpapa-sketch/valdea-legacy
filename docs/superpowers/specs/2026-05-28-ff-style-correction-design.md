# FF風補正 設計仕様書
日付: 2026-05-28

## 目的
「観測者のいない記録 — valdea legacy —」をイアン・リビングストン＆スティーブ・ジャクソンのFighting Fantasy形式に準拠させる。精神値/XP/ローグライク要素は維持。

## 対象ファイル
`game.html` (単一ファイル、432KB、2934行)

## 変更①：「〜なら〇〇へ進め」インジェクション
**方式**: JavaScript（ランタイム）  
**関数**: `injectFFChoiceHints()`  
各 `.para` の `.para-body` 末尾に `.ff-hint` 段落を追加。`.choices` 内ボタンの onclick を解析して：
- `goto(N)` → `Xするなら **N** へ進め`
- `luckCheck(ok, ng)` → `🎲 **運試し**を行え——成功→**ok**、失敗→**ng**へ進め`
- `skillCheck(...)` → `🎲 **技術試験**を行え`
- `startCombat(name, sk, hp)` → `⚔ **name**（技術点sk・体力点hp）と戦え`

実行タイミング: `DOMContentLoaded` + `goto()` フック + `rebuild138()` フック

**CSS追加** (`.ff-hint`):
- font-size .78rem、color var(--dim)
- border-top 1px dashed #2a2620
- margin-top .8rem、padding-top .5rem

## 変更②：テンス統一（現在形）
**方式**: Node.js変換スクリプト  
対象: `<p>` タグ内の地の文（「」内の台詞は除外）  
変換パターン（確定リスト）:

| 変換前 | 変換後 |
|--------|--------|
| 〜た。 | 〜る。（文末動詞のみ） |
| があった | がある |
| だった。 | だ。 |
| していた | している |
| 〜を見た | 〜を見る |
| 〜と言った | 〜と言う |
| 〜は言った | 〜は言う |
| 歩き続けた | 歩き続ける |

台詞「〜」内はスキップ。  
スクリプト: `tools/tense-fix.mjs`

## 変更③：ルール指示インライン記述
変更①と同一関数内で処理。戦闘・運試し・技術試験ボタンに対して、段落本文内にFF風の指示テキストを追加（ボタン上部）。

## 実装順序
1. CSS追加（`<style>` ブロック末尾）
2. `injectFFChoiceHints()` JS関数追加（`</body>` 直前）
3. `goto()` と `rebuild138()` にフック追加
4. `tools/tense-fix.mjs` 作成・実行

## 非変更項目
- 精神値（MENTAL）システム
- XP/レベルシステム
- ローグライク引き継ぎ
- 音響エンジン（SND）
- セーブ/ロード
- マップ
