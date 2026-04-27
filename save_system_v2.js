/**
 * valdea legacy - localStorage バージョン管理システム
 * Sorcery!スタイル セーブデータ管理
 */

// セーブデータバージョン
const SAVE_VERSION = "1.1.0";
const SAVE_KEY_PREFIX = "valdea_";

/**
 * セーブデータ構造（v1.1.0）
 */
const SaveDataSchema = {
  version: SAVE_VERSION,
  created: null,      // タイムスタンプ
  updated: null,      // 最終更新
  
  // ゲーム状態
  state: {
    current_para: "一",
    sk: 7,
    sk0: 7,
    hp: 14,
    hp0: 14,
    lk: 7,
    lk0: 7,
    gold: 3,
    xp: 0,
    
    // Sorcery!スタイル: 詳細なインベントリ
    inventory: [
      {id: "food", name: "食料", count: 3, type: "consumable"},
      {id: "food", name: "食料", count: 3, type: "consumable"},
      {id: "food", name: "食料", count: 3, type: "consumable"}
    ],
    
    // フラグシステム
    flags: {},
    
    // 関係値システム（Sorcery!の重要要素）
    relationships: {
      nack: 0,
      golm: 0,
      sira: 0
    },
    
    // 腐敗度（Sorcery!の闇堕ちシステム）
    corruption: 0,
    
    // 訪問履歴（Sorcery!スタイル）
    visited: [],
    
    // 選択履歴（プレイスタイル分析用）
    choice_history: [],
    
    // メタ情報
    meta: {
      playTime: 0,
      deaths: 0,
      combats_won: 0,
      combats_fled: 0
    }
  }
};

/**
 * マイグレーション関数
 */
function migrateStorageData(oldData) {
  const version = oldData.version || "1.0.0";
  
  console.log(`[Migration] セーブデータ v${version} → v${SAVE_VERSION}`);
  
  // v1.0.0 → v1.1.0
  if (version === "1.0.0") {
    return {
      version: "1.1.0",
      created: oldData.created || Date.now(),
      updated: Date.now(),
      state: {
        ...oldData,
        visited: oldData.hist || [],
        choice_history: [],
        meta: {
          playTime: oldData.playTime || 0,
          deaths: 0,
          combats_won: 0,
          combats_fled: 0
        }
      }
    };
  }
  
  return oldData;
}

/**
 * セーブ関数（バージョン管理付き）
 */
function saveGameV2(state) {
  try {
    const saveData = {
      version: SAVE_VERSION,
      created: state.created || Date.now(),
      updated: Date.now(),
      state: state
    };
    
    localStorage.setItem(SAVE_KEY_PREFIX + 'save', JSON.stringify(saveData));
    
    // バックアップ作成（最新3件）
    const backups = JSON.parse(localStorage.getItem(SAVE_KEY_PREFIX + 'backups') || '[]');
    backups.unshift(saveData);
    if (backups.length > 3) backups.pop();
    localStorage.setItem(SAVE_KEY_PREFIX + 'backups', JSON.stringify(backups));
    
    console.log(`[Save] v${SAVE_VERSION} セーブ完了`);
    return true;
  } catch (e) {
    console.error('[Save] エラー:', e);
    return false;
  }
}

/**
 * ロード関数（マイグレーション付き）
 */
function loadGameV2() {
  try {
    const raw = localStorage.getItem(SAVE_KEY_PREFIX + 'save');
    if (!raw) return null;
    
    let data = JSON.parse(raw);
    
    // バージョンチェック＆マイグレーション
    if (data.version !== SAVE_VERSION) {
      console.warn(`[Load] 古いバージョン検出: v${data.version}`);
      data = migrateStorageData(data);
      
      // マイグレーション後のデータを保存
      saveGameV2(data.state);
    }
    
    console.log(`[Load] v${SAVE_VERSION} ロード完了`);
    return data.state;
  } catch (e) {
    console.error('[Load] エラー:', e);
    return null;
  }
}

/**
 * バックアップから復元
 */
function restoreFromBackup(index = 0) {
  try {
    const backups = JSON.parse(localStorage.getItem(SAVE_KEY_PREFIX + 'backups') || '[]');
    if (!backups[index]) {
      console.error(`[Restore] バックアップ ${index} が見つかりません`);
      return false;
    }
    
    const backup = backups[index];
    localStorage.setItem(SAVE_KEY_PREFIX + 'save', JSON.stringify(backup));
    
    console.log(`[Restore] バックアップ ${index} から復元完了`);
    return true;
  } catch (e) {
    console.error('[Restore] エラー:', e);
    return false;
  }
}

/**
 * セーブデータの整合性チェック
 */
function validateSaveData(data) {
  const errors = [];
  
  if (!data.state) {
    errors.push("state が存在しません");
  }
  
  if (data.state.sk < 1 || data.state.sk > 20) {
    errors.push(`SK値が異常: ${data.state.sk}`);
  }
  
  if (data.state.hp < 0 || data.state.hp > 50) {
    errors.push(`HP値が異常: ${data.state.hp}`);
  }
  
  if (errors.length > 0) {
    console.error('[Validate] セーブデータ破損:', errors);
    return false;
  }
  
  return true;
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    saveGameV2,
    loadGameV2,
    restoreFromBackup,
    validateSaveData,
    SAVE_VERSION
  };
}
