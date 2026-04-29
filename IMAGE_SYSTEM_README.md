# valdea legacy - 画像システム統合版

**ファイル:** valdea_with_images.html

---

## 📸 画像システムの特徴

提供されたコードを**完全に統合**しました：

### ✅ 実装済み機能

1. **20枚の画像マッピング**
   - 7つのカテゴリ（env, enemy, npc, event, death, tension, ending）
   - 各カテゴリに2-4枚の画像

2. **初回のみ表示**
   - localStorage使用
   - 同じパラグラフを再訪問しても画像は表示されない

3. **フェードインアニメーション**
   - 1.2秒かけてゆっくり表示
   - グレースケール＋セピア処理

4. **パラグラフ→カテゴリ自動判定**
   ```javascript
   パラグラフ 1-15   → env (環境)
   パラグラフ 16-30  → npc (NPC)
   パラグラフ 31-50  → event (イベント)
   パラグラフ 51-70  → enemy (戦闘)
   パラグラフ 71-85  → tension (緊張)
   パラグラフ 86-95  → death (死亡)
   パラグラフ 96-108 → ending (エンディング)
   ```

---

## 📁 必要な画像ファイル

`images/` フォルダに以下のファイルを配置してください：

### 環境（env）
- `env_ruins.png` - 廃墟
- `env_forest.png` - 森
- `env_cave.png` - 洞窟
- `env_gate.png` - 門

### 敵（enemy）
- `enemy_goblin.png` - ゴブリン
- `enemy_beast.png` - 獣
- `enemy_shadow.png` - 影
- `enemy_boss.png` - ボス

### NPC（npc）
- `npc_oldman.png` - 老人
- `npc_woman.png` - 女性
- `npc_hooded.png` - フード

### イベント（event）
- `event_symbol.png` - シンボル
- `event_ritual.png` - 儀式
- `event_collapse.png` - 崩壊
- `event_fire.png` - 炎

### 死亡（death）
- `death_body.png` - 遺体
- `death_bones.png` - 骨

### 緊張（tension）
- `tension_eyes.png` - 目
- `tension_hand.png` - 手

### エンディング（ending）
- `ending_throne.png` - 玉座

**合計: 20枚**

---

## 🎨 画像の推奨仕様

### サイズ
- 横幅: 600-800px
- 縦幅: 400-600px
- アスペクト比: 4:3 または 16:9

### 形式
- PNG または JPEG
- ファイルサイズ: 100KB以下（推奨）

### スタイル
- モノクロ推奨（自動でグレースケール処理されます）
- Fighting Fantasy / Sorcery! の挿絵風
- ペン画・銅版画風

---

## 🔧 カスタマイズ方法

### 画像を無効化する場合

画像なしで動作させたい場合、HTMLの以下の部分をコメントアウト：

```javascript
// 画像表示部分（154-162行目）
/*
if (!localStorage.getItem(imgKey)) {
  const img = getImage(paraId);
  html += `
    <div class="illustration">
      <img id="img_${paraId}" src="images/${img}" ...>
    </div>
  `;
  localStorage.setItem(imgKey, 'true');
}
*/
```

### カテゴリ分類を変更する場合

`getImageType()` 関数を編集：

```javascript
function getImageType(paraId) {
  const paraIndex = getParaIndex(paraId);
  
  // カスタム分類
  if (paraIndex <= 10) return "env";
  if (paraIndex <= 20) return "npc";
  // ...
}
```

---

## 🚀 使い方

### 1. 画像なしで動作確認

そのまま開けば動作します。
画像は `onerror` で非表示になります。

### 2. 画像を追加

`images/` フォルダを作成し、20枚の画像を配置。

### 3. 訪問履歴をリセット

ブラウザのコンソール（F12）で実行：
```javascript
localStorage.clear();
location.reload();
```

---

## 🎯 統合内容

提供されたコードの以下の要素を**完全に統合**：

✅ 画像マッピングシステム（imageMap）  
✅ カテゴリ判定ロジック（getImageType）  
✅ 画像取得（固定化）  
✅ 初回のみ表示（localStorage）  
✅ フェードインアニメーション  
✅ レスポンシブデザイン  

---

## 📊 現在の実装状況

| 要素 | 状態 |
|------|------|
| 画像システム | ✅ 完全実装 |
| パラグラフデータ | ⚠️ サンプル（15個） |
| 戦闘システム | ⚠️ 簡易版 |
| ステータス管理 | ⚠️ 訪問履歴のみ |
| マップ機能 | ❌ 未実装 |

---

## 🔄 完全版への拡張

全108パラグラフを実装する場合：

1. `game_PRODUCTION_READY.html` から全パラグラフを抽出
2. `gameData` オブジェクトに追加
3. 戦闘システムを統合
4. ステータス管理を追加

---

**作成日時:** 2026-04-30  
**ステータス:** ✅ 画像システム統合完了  
**次のステップ:** 画像ファイルの準備

