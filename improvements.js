/**
 * valdea legacy - 開発支援ツール（本番環境用）
 * 既存コードを壊さず、追加機能のみ提供
 */

// ========================================
// 1. 分岐マップの自動生成（開発支援）
// ========================================
function extractBranchMap() {
    const map = {};
    
    document.querySelectorAll('.para').forEach(p => {
        const id = p.id;
        const targets = [...p.querySelectorAll('[onclick]')]
            .map(btn => {
                const match = btn.getAttribute('onclick').match(/goto\('([^']+)'\)/);
                return match ? match[1] : null;
            })
            .filter(Boolean);
        
        map[id] = [...new Set(targets)]; // 重複除去
    });
    
    return map;
}

// ========================================
// 2. リンク整合性の完全検証
// ========================================
function validateAllLinks() {
    const allIds = new Set([...document.querySelectorAll('.para')].map(e => e.id));
    const branchMap = extractBranchMap();
    
    const errors = [];
    const warnings = [];
    
    Object.entries(branchMap).forEach(([from, targets]) => {
        targets.forEach(to => {
            if (!allIds.has(to)) {
                errors.push(`${from} → ${to}`);
            }
        });
    });
    
    // 孤立ノード検出
    const referenced = new Set();
    Object.values(branchMap).forEach(targets => {
        targets.forEach(t => referenced.add(t));
    });
    
    const unreferenced = [...allIds].filter(id => 
        !referenced.has(id) && id !== '一'
    );
    
    if (unreferenced.length > 0) {
        warnings.push(`未参照ノード: ${unreferenced.length}個`);
    }
    
    return {
        errors,
        warnings,
        totalNodes: allIds.size,
        totalLinks: Object.values(branchMap).flat().length
    };
}

// ========================================
// 3. 到達可能性シミュレーション
// ========================================
function simulateReachability(startNode = '一') {
    const branchMap = extractBranchMap();
    const visited = new Set();
    const stack = [startNode];
    
    while (stack.length > 0) {
        const current = stack.pop();
        if (visited.has(current)) continue;
        
        visited.add(current);
        
        const targets = branchMap[current] || [];
        targets.forEach(target => {
            if (!visited.has(target)) {
                stack.push(target);
            }
        });
    }
    
    const allIds = new Set([...document.querySelectorAll('.para')].map(e => e.id));
    const unreachable = [...allIds].filter(id => !visited.has(id));
    
    return {
        reachable: visited.size,
        unreachable: unreachable.length,
        unreachableNodes: unreachable
    };
}

// ========================================
// 4. 開発モード用デバッグコンソール
// ========================================
function enableDevMode() {
    const results = {
        linkValidation: validateAllLinks(),
        reachability: simulateReachability()
    };
    
    console.log('='*80);
    console.log('valdea legacy - Development Mode');
    console.log('='*80);
    
    console.log('\n📊 Statistics:');
    console.log(`  Total Nodes: ${results.linkValidation.totalNodes}`);
    console.log(`  Total Links: ${results.linkValidation.totalLinks}`);
    console.log(`  Reachable: ${results.reachability.reachable}`);
    console.log(`  Unreachable: ${results.reachability.unreachable}`);
    
    if (results.linkValidation.errors.length > 0) {
        console.error('\n❌ Link Errors:', results.linkValidation.errors);
    } else {
        console.log('\n✅ All links valid');
    }
    
    if (results.linkValidation.warnings.length > 0) {
        console.warn('\n⚠️  Warnings:', results.linkValidation.warnings);
    }
    
    if (results.reachability.unreachable > 0) {
        console.warn('\n⚠️  Unreachable nodes:', results.reachability.unreachableNodes);
    }
    
    return results;
}

// ========================================
// 5. 本番環境チェック（GitHub Pages対応）
// ========================================
function checkProductionReadiness() {
    const checks = {
        initialDisplay: document.querySelector('.para.active') !== null,
        gotoExists: typeof goto === 'function',
        localStorageWorks: typeof localStorage !== 'undefined',
        allParagraphsHaveIds: [...document.querySelectorAll('.para')].every(p => p.id)
    };
    
    const allPassed = Object.values(checks).every(v => v);
    
    console.log('\n🔍 Production Readiness Check:');
    Object.entries(checks).forEach(([key, value]) => {
        console.log(`  ${value ? '✅' : '❌'} ${key}`);
    });
    
    return allPassed;
}

// ========================================
// 6. 使用方法
// ========================================
console.log('💡 Development Tools Loaded');
console.log('   enableDevMode() - 開発モード有効化');
console.log('   validateAllLinks() - リンク検証');
console.log('   simulateReachability() - 到達可能性チェック');
console.log('   checkProductionReadiness() - 本番環境チェック');
