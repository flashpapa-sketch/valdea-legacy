/**
 * ヴォルカネスの迷宮：匿名の進捗記録を受け取り、スプレッドシートに1行ずつ追加する。
 * 記録するのは段落番号・体力・金貨などの数字と、ブラウザごとのランダムな番号（sid）だけ。
 * 名前・メールアドレス・IPアドレスは記録しない（ゲーム側でも送っていない）。
 */
const SHEET_NAME = 'progress';
const HEADER = ['受信時刻', 'sid', '段落', '体力', '最大体力', '金貨', '言語', '端末', 'ブラウザ時刻'];

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let sh = ss.getSheetByName(SHEET_NAME);
    if (!sh) {
      sh = ss.insertSheet(SHEET_NAME);
      sh.appendRow(HEADER);
      sh.setFrozenRows(1);
    }
    sh.appendRow([
      new Date(),
      String(d.sid || '').slice(0, 40),
      String(d.para || '').slice(0, 60),
      d.hp,
      d.hp0,
      d.gold,
      String(d.lang || '').slice(0, 4),
      String(d.dev || '').slice(0, 10),
      String(d.t || '').slice(0, 30)
    ]);
  } catch (err) {
    // 壊れた送信は捨てる（ゲームの動作には影響させない）
  }
  return ContentService.createTextOutput('ok');
}
