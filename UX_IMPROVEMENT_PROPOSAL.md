# valdea legacy - Sorcery!スタイル UX改善提案書

## 現状の課題

### 1. 逃げルートの過剰使用
- **問題:** ◆百三十八への遷移が24箇所
- **影響:** 選択の重みが薄れる、分岐の意味が消失
- **Sorcery!との違い:** Sorcery!では「進む/戻る」の選択に常に意味がある

### 2. 選択肢の文言が平板
- **問題:** 「酒場へ向かう」「神殿へ向かう」など、動詞のみ
- **Sorcery!との違い:** 「なぜそうするのか」が込められている

### 3. 環境描写の不足
- **問題:** パラグラフが「何が起きたか」のみ
- **Sorcery!との違い:** 「どんな場所か」「何が見えるか」が先

---

## Sorcery!スタイル改善案

### 改善1: 逃げルート24箇所の個別化

#### ❌ 現状（全て同じ）
```
どのパラグラフからも:
「すでに情報は十分だ」→ ◆百三十八
```

#### ✅ Sorcery!スタイル

**パターンA: 情報収集済み**
```
◆二（掲示板）から:
「掲示板の情報で十分だ。今すぐ出発する」→ ◆百三十八
→ フラグ: board_checked

◆十四（マグダの話）から:
「星の間の情報を得た。もう行くべきだ」→ ◆百三十八
→ フラグ: star_room_info
```

**パターンB: 時間的緊急性**
```
◆四十七（酒場）から:
「時間がない。一刻も早くザル＝カラムへ」→ ◆百三十八
→ 効果: 夜間出発、ランダムイベント発生率UP

◆六十一（神殿）から:
「夜明けを待たずに出る」→ ◆百三十八
→ 効果: 体力-2、でも先行者より早く到着
```

**パターンC: 経験者プレイ**
```
◆一から直接:
「この街は何度も来た。手順は分かっている」→ ◆百三十八
→ 条件: プレイ回数2回以上
→ 効果: 金貨+5（時短ボーナス）、でも仲間0人
```

**結果:**
- 24箇所 → 3-4パターンに集約
- 各選択に「なぜ」と「結果」
- リプレイ時の選択肢増加

---

### 改善2: 選択肢の文言改善（Sorcery!スタイル）

#### ❌ 現状
```
<button>酒場へ向かう</button>
<button>神殿へ向かう</button>
<button>武器屋の看板が見えた</button>
```

#### ✅ Sorcery!スタイル
```
<button class="choice-exploration">
  酒場「錆びた剣亭」で噂を集める
  <span class="choice-hint">情報収集・仲間との出会い</span>
</button>

<button class="choice-cautious">
  神殿で古代の記録を調べる
  <span class="choice-hint">ザル＝カラムの真実・準備</span>
</button>

<button class="choice-purchase">
  武器屋「鉄の爪」で装備を整える
  <span class="choice-hint">戦闘力UP・職人の助言</span>
</button>
```

**CSS追加:**
```css
.choice-hint {
  display: block;
  font-size: 0.7rem;
  color: var(--dim);
  margin-top: 0.3rem;
  font-style: italic;
}

.choice-exploration { border-left: 3px solid #8ab48a; }
.choice-cautious { border-left: 3px solid #c4c47a; }
.choice-purchase { border-left: 3px solid #b8860b; }
```

**効果:**
- プレイヤーが選択の意味を理解
- 視覚的に選択肢の性格が分かる
- Sorcery!の「なぜそうするのか」を表現

---

### 改善3: 環境描写の強化

#### ❌ 現状（◆四十七 酒場）
```
「錆びた剣亭」はドーランで唯一まともな酒場だ。
扉を押し開けると、煙草の煙と獣脂の臭いが鼻をつく。
```

#### ✅ Sorcery!スタイル
```
[冒頭に環境を配置]
煙草の煙が酒場の天井に渦を巻いている。
獣脂のランプが薄暗い光を投げかけ、
奥のカウンターでは小柄な女将が杯を拭いている。

[次に行動を配置]
「錆びた剣亭」。ドーランで唯一まともな酒場だ。
あなたは扉を押し開ける。

[最後に選択の文脈]
テーブルに複数の人影がある。
冒険者風の者、地元の商人、そしてフードを深く被った者が一人。
全員がこちらをちらりと見て、視線を外した。
```

**構造:**
1. 環境描写（五感）
2. 行動
3. 選択の文脈

**効果:**
- 場所の雰囲気が伝わる
- プレイヤーが「そこにいる」感覚
- Sorcery!の世界観構築手法

---

### 改善4: 選択の「重み」可視化

#### 新規UI要素
```html
<div class="choice-weight-indicator">
  <div class="weight-bar" data-weight="high"></div>
  <span class="weight-label">取り返しがつかない選択</span>
</div>

<button class="choice-btn choice-permanent">
  ロサを見捨てて先へ進む
</button>
```

**CSS:**
```css
.weight-bar[data-weight="high"] {
  background: linear-gradient(90deg, #d32f2f, #f44336);
}

.weight-bar[data-weight="medium"] {
  background: linear-gradient(90deg, #ffa726, #ffb74d);
}

.choice-permanent {
  border: 2px solid #d32f2f;
  background: rgba(211, 47, 47, 0.1);
}
```

**効果:**
- 重要な選択が視覚的に分かる
- Sorcery!の「後悔する選択」の表現
- プレイヤーが慎重に考える

---

### 改善5: リプレイ価値の向上

#### 新規システム: プレイスタイル分析
```javascript
const PlayStyle = {
  explorer: 0,    // 探索重視
  warrior: 0,     // 戦闘重視
  diplomat: 0,    // 外交重視
  cautious: 0,    // 慎重プレイ
  bold: 0         // 大胆プレイ
};

// 選択肢に応じてスタイルポイント加算
function recordChoice(choiceType) {
  switch(choiceType) {
    case 'exploration': PlayStyle.explorer++; break;
    case 'combat': PlayStyle.warrior++; break;
    case 'diplomatic': PlayStyle.diplomat++; break;
    // ...
  }
  
  // 一定ポイントで隠しイベント解放
  if (PlayStyle.explorer >= 10) {
    unlockSecret('explorer_path');
  }
}
```

**効果:**
- プレイスタイルに応じた分岐
- リプレイで異なる体験
- Sorcery!の「遊び方の自由」

---

## 実装優先度

### 優先度: 高（即効性あり）
1. **選択肢の文言改善** - 既存テキストの修正のみ
2. **環境描写の強化** - パラグラフ冒頭の追記

### 優先度: 中（構造変更必要）
3. **逃げルート24箇所の個別化** - ロジック変更
4. **選択の重み可視化** - CSS追加

### 優先度: 低（大規模実装）
5. **プレイスタイル分析システム** - 新規機能

---

## まとめ

**Sorcery!の本質:**
> 「選択に意味があり、世界が生きている」

**改善の方向性:**
1. ✅ 選択肢に「なぜ」を込める
2. ✅ 環境描写で世界観を作る
3. ✅ 取り返しのつかない選択を明示
4. ✅ リプレイで異なる体験を提供

これらを段階的に実装することで、
valdea legacyは真の「Sorcery!スタイル」になります。
