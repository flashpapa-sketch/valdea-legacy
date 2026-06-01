/**
 * tense-fix.mjs
 * FF風テンス統一 — 地の文の過去形を現在形に変換
 * 台詞「〜」内はスキップ
 *
 * 使用: node tools/tense-fix.mjs
 */

import { readFileSync, writeFileSync, copyFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SRC  = join(__dirname, '..', 'game.html');
const DEST = join(__dirname, '..', 'game.html');
const BAK  = join(__dirname, '..', 'game.html.bak');

// バックアップ
copyFileSync(SRC, BAK);
console.log('Backup: game.html.bak');

let html = readFileSync(SRC, 'utf8');

// ──────────────────────────────────────────────
// 地の文のみ変換（<p>タグ内、台詞「」外）
// ──────────────────────────────────────────────

/**
 * <p>...</p> 内の地の文を変換する
 * 「」内はそのまま保持
 */
function transformParagraph(text) {
  // 台詞部分「〜」を一時プレースホルダーに退避
  const dialogues = [];
  let t = text.replace(/「[^」]*」/g, (m) => {
    dialogues.push(m);
    return `\x00D${dialogues.length - 1}\x00`;
  });
  // 二重鉤括弧も退避
  t = t.replace(/『[^』]*』/g, (m) => {
    dialogues.push(m);
    return `\x00D${dialogues.length - 1}\x00`;
  });

  // ── 変換ルール（地の文のみ適用）──

  // 1. 〜していた → 〜している
  t = t.replace(/していた([。、」』\s])/g, 'している$1');

  // 2. 〜だった。→ 〜だ。
  t = t.replace(/だった。/g, 'だ。');

  // 3. 〜があった → 〜がある
  t = t.replace(/があった([。、\s])/g, 'がある$1');

  // 4. 〜を見た → 〜を見る
  t = t.replace(/を見た([。、\s])/g, 'を見る$1');

  // 5. 〜は言った → 〜は言う（台詞外の地の文ナレーション）
  t = t.replace(/は言った([。、\s])/g, 'は言う$1');

  // 6. 〜と言った → 〜と言う
  t = t.replace(/と言った([。、\s])/g, 'と言う$1');

  // 7. 〜歩き続けた → 〜歩き続ける
  t = t.replace(/歩き続けた([。、\s])/g, '歩き続ける$1');

  // 8. 〜踏み出した → 〜踏み出す
  t = t.replace(/踏み出した([。、\s])/g, '踏み出す$1');

  // 9. 〜立っていた → 〜立っている
  t = t.replace(/立っていた([。、\s])/g, '立っている$1');

  // 10. 〜向かった → 〜向かう（行動動詞）
  t = t.replace(/へ向かった([。、\s])/g, 'へ向かう$1');

  // 台詞を復元
  t = t.replace(/\x00D(\d+)\x00/g, (_, i) => dialogues[parseInt(i)]);

  return t;
}

// <p>...</p> タグ内のテキストに適用
// para-body 内の <p> のみターゲット
let count = 0;
html = html.replace(
  /(<div class="para-body">)([\s\S]*?)(<\/div>)/g,
  (_, open, inner, close) => {
    const transformed = inner.replace(
      /<p>([\s\S]*?)<\/p>/g,
      (pmatch, content) => {
        const fixed = transformParagraph(content);
        if (fixed !== content) count++;
        return `<p>${fixed}</p>`;
      }
    );
    return open + transformed + close;
  }
);

writeFileSync(DEST, html, 'utf8');
console.log(`完了: ${count} 箇所変換`);
console.log('出力: game.html');
