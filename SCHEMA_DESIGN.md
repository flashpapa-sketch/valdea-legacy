# valdea legacy - Sorcery!スタイル JSONスキーマ v1.0

## 設計思想（Sorcery!の DNA）

### 1. 探索の喜び
- 各パラグラフは「場所」であり「瞬間」
- 環境描写が世界観を作る
- 隠し要素・発見可能な情報

### 2. 選択の重み
- 各選択肢に意味がある
- 即座の結果 + 遅延された結果
- 取り返しのつかない選択

### 3. 装備とアイテム
- アイテムが状況を変える
- 装備の選択が戦略性を生む
- 消費アイテムの管理

### 4. キャラクターとの出会い
- 記憶に残るNPC
- 関係値システム
- 再登場と因果

---

## JSONスキーマ構造

```json
{
  "meta": {
    "version": "1.0.0",
    "total_paragraphs": 108,
    "total_combats": 28,
    "endings": 7,
    "created": "2026-04-27",
    "style": "sorcery"
  },
  
  "world": {
    "locations": {
      "doran": "辺境交易街ドーラン",
      "zar_karam": "黄金時代の遺跡ザル＝カラム",
      "wilderness": "ヴァルデアの荒野"
    },
    "factions": {
      "merchant_guild": "ドーラン商人組合",
      "dark_merchant": "闇の商会",
      "ancients": "黄金時代の賢者たち"
    }
  },
  
  "paragraphs": {
    "一": {
      "id": "一",
      "number": "一",
      "title": "荒野の果て",
      "location": "wilderness",
      "atmosphere": "wind_sand_desolate",
      
      "text": {
        "main": [
          "ヴァルデアの荒野に、風が砂埃を巻き上げている。",
          "あなたはその風に背を向けながら、地平線に浮かぶ街の輪郭を見た。",
          "ドーラン。辺境の交易街だ。荒野の吹き溜まりだ。"
        ],
        "observation": [
          "左手の甲が熱い。紋章だ。",
          "生まれた時からそこにある古代の刻印が、ザル＝カラムに近づくにつれて熱を増している。"
        ],
        "immediate": [
          "ドーランの街門が見えてくる。",
          "門番が二人、槍を構えて立っている。",
          "あなたは歩き続ける。"
        ]
      },
      
      "choices": [
        {
          "id": "c1_1",
          "label": "街門の掲示板を確かめてから入る",
          "target": "二",
          "type": "exploration",
          "weight": "information_gathering",
          "flavor": "情報は武器だ。何が起きているかを知るべきだ。"
        },
        {
          "id": "c1_2",
          "label": "まっすぐ酒場へ向かう",
          "target": "四十七",
          "type": "direct",
          "weight": "action_oriented",
          "flavor": "時間を無駄にできない。噂は酒場で聞ける。"
        },
        {
          "id": "c1_3",
          "label": "路地に人影を見た",
          "target": "六",
          "type": "investigation",
          "weight": "cautious_observant",
          "flavor": "何かが動いた。見逃すべきではない。"
        },
        {
          "id": "c1_4",
          "label": "すでに情報は十分だ",
          "target": "百三十八",
          "type": "skip",
          "weight": "experienced_prepared",
          "flavor": "準備は済んでいる。ザル＝カラムへ向かう時だ。",
          "requirement": "meta_knowledge"
        }
      ],
      
      "state": {
        "flags_set": [],
        "flags_required": [],
        "items_gained": [],
        "items_consumed": [],
        "stat_changes": {}
      },
      
      "meta": {
        "first_visit": true,
        "replayability": "low",
        "sorcery_style": {
          "atmosphere": "opening_vista",
          "tone": "mysterious_foreboding",
          "pacing": "slow_deliberate"
        }
      }
    }
  }
}
```

---

## 選択肢の「重み」システム（Sorcery!の核心）

### weight（選択の性格）
- `exploration` - 探索・調査
- `direct` - 直接行動
- `cautious` - 慎重・観察
- `bold` - 大胆・リスク
- `diplomatic` - 外交・説得
- `aggressive` - 攻撃的・強硬
- `retreat` - 退却・回避
- `skip` - スキップ（メタ選択）

### consequence（結果の種類）
- `immediate` - 即座の結果
- `delayed` - 遅延された結果
- `permanent` - 取り返しがつかない
- `reversible` - 後で修正可能

---

## Sorcery!スタイルの文体ルール

1. **現在形・二人称**
   - ❌ 「あなたは歩いた」
   - ✅ 「あなたは歩き続ける」

2. **環境描写を冒頭に**
   - ❌ 「街に着いた。風が吹いている」
   - ✅ 「風が砂埃を巻き上げている。街の輪郭が見える」

3. **選択肢に「なぜ」を込める**
   - ❌ 「酒場へ行く」
   - ✅ 「酒場へ向かう（情報収集のため）」

4. **運と技術のバランス**
   - 選択 → スキル → 運試し → 結果
   - プレイヤーの判断が最重要

---

## 次のステップ

Phase 2で3つのサンプルパラグラフを完全JSON化し、
スキーマの妥当性を検証します。
