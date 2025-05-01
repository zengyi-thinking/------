// DOM元素
document.addEventListener('DOMContentLoaded', function() {
    // 标签页切换
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            
            // 移除所有活动类
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));
            
            // 添加活动类到当前标签
            btn.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // 单资源类型相关元素
    const processCountSingle = document.getElementById('process-count-single');
    const generateSingleTable = document.getElementById('generate-single-table');
    const singleTableBody = document.getElementById('single-table-body');
    const checkSingleBtn = document.getElementById('check-single');
    const singleResult = document.getElementById('single-result').querySelector('.result-content');
    const totalResources = document.getElementById('total-resources');
    const availableResources = document.getElementById('available-resources');

    // 多资源类型相关元素
    const processCount = document.getElementById('process-count');
    const resourceCount = document.getElementById('resource-count');
    const generateTablesBtn = document.getElementById('generate-tables');
    const allocationMatrix = document.getElementById('allocation-matrix');
    const maxMatrix = document.getElementById('max-matrix');
    const availableResourcesContainer = document.getElementById('available-resources-container');
    const checkSafetyBtn = document.getElementById('check-safety');
    const multiResult = document.getElementById('multi-result').querySelector('.result-content');
    const requestProcess = document.getElementById('request-process');
    const requestResourcesContainer = document.getElementById('request-resources-container');
    const checkRequestBtn = document.getElementById('check-request');

    // 生成单资源类型表格
    generateSingleTable.addEventListener('click', () => {
        const count = parseInt(processCountSingle.value);
        if (count < 1 || count > 10) {
            alert('进程数量必须在1到10之间');
            return;
        }

        singleTableBody.innerHTML = '';
        for (let i = 0; i < count; i++) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>P${i}</td>
                <td><input type="number" class="allocation-single" min="0" value="0"></td>
                <td><input type="number" class="max-single" min="0" value="0"></td>
                <td class="need-single">0</td>
            `;
            singleTableBody.appendChild(row);
        }

        // 添加事件监听器来计算需求
        const allocationInputs = document.querySelectorAll('.allocation-single');
        const maxInputs = document.querySelectorAll('.max-single');
        const needCells = document.querySelectorAll('.need-single');

        function updateNeed() {
            for (let i = 0; i < count; i++) {
                const allocation = parseInt(allocationInputs[i].value) || 0;
                const max = parseInt(maxInputs[i].value) || 0;
                needCells[i].textContent = Math.max(0, max - allocation);
            }
        }

        allocationInputs.forEach(input => input.addEventListener('input', updateNeed));
        maxInputs.forEach(input => input.addEventListener('input', updateNeed));
    });

    // 检查单资源类型安全性
    checkSingleBtn.addEventListener('click', () => {
        const total = parseInt(totalResources.value) || 0;
        const available = parseInt(availableResources.value) || 0;
        const allocationInputs = document.querySelectorAll('.allocation-single');
        const maxInputs = document.querySelectorAll('.max-single');
        
        if (allocationInputs.length === 0) {
            alert('请先生成表格');
            return;
        }

        // 获取数据
        const n = allocationInputs.length;
        const allocation = [];
        const max = [];
        const need = [];
        
        let totalAllocated = 0;
        
        for (let i = 0; i < n; i++) {
            const a = parseInt(allocationInputs[i].value) || 0;
            const m = parseInt(maxInputs[i].value) || 0;
            
            allocation.push(a);
            max.push(m);
            need.push(Math.max(0, m - a));
            
            totalAllocated += a;
        }
        
        // 验证数据
        if (totalAllocated + available > total) {
            singleResult.innerHTML = `
                <p class="unsafe">错误: 已分配资源(${totalAllocated}) + 可用资源(${available}) 超过总资源(${total})</p>
            `;
            return;
        }
        
        // 安全性检查
        const result = checkSafetySingleResource(allocation, need, available, n);
        
        if (result.safe) {
            singleResult.innerHTML = `
                <p class="safe">系统处于安全状态</p>
                <div class="sequence">安全序列: ${result.sequence.map(i => 'P' + i).join(' → ')}</div>
            `;
        } else {
            singleResult.innerHTML = `
                <p class="unsafe">系统处于不安全状态</p>
            `;
        }
    });

    // 生成多资源类型表格
    generateTablesBtn.addEventListener('click', () => {
        const p = parseInt(processCount.value);
        const r = parseInt(resourceCount.value);
        
        if (p < 1 || p > 10 || r < 1 || r > 10) {
            alert('进程数量和资源类型数必须在1到10之间');
            return;
        }
        
        // 生成分配矩阵
        allocationMatrix.innerHTML = '';
        allocationMatrix.style.gridTemplateColumns = `repeat(${r}, 1fr)`;
        
        // 添加列标题
        for (let j = 0; j < r; j++) {
            const header = document.createElement('div');
            header.textContent = `R${j}`;
            header.style.fontWeight = 'bold';
            allocationMatrix.appendChild(header);
        }
        
        // 添加输入框
        for (let i = 0; i < p; i++) {
            for (let j = 0; j < r; j++) {
                const input = document.createElement('input');
                input.type = 'number';
                input.min = 0;
                input.value = 0;
                input.classList.add('allocation-input');
                input.dataset.row = i;
                input.dataset.col = j;
                allocationMatrix.appendChild(input);
            }
        }
        
        // 生成最大需求矩阵
        maxMatrix.innerHTML = '';
        maxMatrix.style.gridTemplateColumns = `repeat(${r}, 1fr)`;
        
        // 添加列标题
        for (let j = 0; j < r; j++) {
            const header = document.createElement('div');
            header.textContent = `R${j}`;
            header.style.fontWeight = 'bold';
            maxMatrix.appendChild(header);
        }
        
        // 添加输入框
        for (let i = 0; i < p; i++) {
            for (let j = 0; j < r; j++) {
                const input = document.createElement('input');
                input.type = 'number';
                input.min = 0;
                input.value = 0;
                input.classList.add('max-input');
                input.dataset.row = i;
                input.dataset.col = j;
                maxMatrix.appendChild(input);
            }
        }
        
        // 生成可用资源输入
        availableResourcesContainer.innerHTML = '';
        for (let j = 0; j < r; j++) {
            const container = document.createElement('div');
            container.classList.add('input-group');
            
            const label = document.createElement('label');
            label.textContent = `R${j}:`;
            
            const input = document.createElement('input');
            input.type = 'number';
            input.min = 0;
            input.value = 0;
            input.classList.add('available-input');
            
            container.appendChild(label);
            container.appendChild(input);
            availableResourcesContainer.appendChild(container);
        }
        
        // 生成请求资源输入
        requestResourcesContainer.innerHTML = '';
        for (let j = 0; j < r; j++) {
            const container = document.createElement('div');
            container.classList.add('input-group');
            
            const label = document.createElement('label');
            label.textContent = `R${j}:`;
            
            const input = document.createElement('input');
            input.type = 'number';
            input.min = 0;
            input.value = 0;
            input.classList.add('request-input');
            
            container.appendChild(label);
            container.appendChild(input);
            requestResourcesContainer.appendChild(container);
        }
        
        // 更新请求进程ID的最大值
        requestProcess.max = p - 1;
        if (parseInt(requestProcess.value) >= p) {
            requestProcess.value = 0;
        }
    });

    // 检查多资源类型安全性
    checkSafetyBtn.addEventListener('click', () => {
        const p = parseInt(processCount.value);
        const r = parseInt(resourceCount.value);
        
        // 获取分配矩阵
        const allocation = Array(p).fill().map(() => Array(r).fill(0));
        const allocationInputs = document.querySelectorAll('.allocation-input');
        
        allocationInputs.forEach(input => {
            const i = parseInt(input.dataset.row);
            const j = parseInt(input.dataset.col);
            allocation[i][j] = parseInt(input.value) || 0;
        });
        
        // 获取最大需求矩阵
        const max = Array(p).fill().map(() => Array(r).fill(0));
        const maxInputs = document.querySelectorAll('.max-input');
        
        maxInputs.forEach(input => {
            const i = parseInt(input.dataset.row);
            const j = parseInt(input.dataset.col);
            max[i][j] = parseInt(input.value) || 0;
        });
        
        // 获取可用资源
        const available = Array(r).fill(0);
        const availableInputs = document.querySelectorAll('.available-input');
        
        availableInputs.forEach((input, j) => {
            available[j] = parseInt(input.value) || 0;
        });
        
        // 计算需求矩阵
        const need = Array(p).fill().map((_, i) => 
            Array(r).fill().map((_, j) => Math.max(0, max[i][j] - allocation[i][j]))
        );
        
        // 安全性检查
        const result = checkSafetyMultiResource(allocation, max, need, available, p, r);
        
        if (result.safe) {
            multiResult.innerHTML = `
                <p class="safe">系统处于安全状态</p>
                <div class="sequence">安全序列: ${result.sequence.map(i => 'P' + i).join(' → ')}</div>
            `;
        } else {
            multiResult.innerHTML = `
                <p class="unsafe">系统处于不安全状态</p>
            `;
        }
    });

    // 检查资源请求
    checkRequestBtn.addEventListener('click', () => {
        const p = parseInt(processCount.value);
        const r = parseInt(resourceCount.value);
        const processId = parseInt(requestProcess.value);
        
        if (processId < 0 || processId >= p) {
            alert('进程ID无效');
            return;
        }
        
        // 获取分配矩阵
        const allocation = Array(p).fill().map(() => Array(r).fill(0));
        const allocationInputs = document.querySelectorAll('.allocation-input');
        
        allocationInputs.forEach(input => {
            const i = parseInt(input.dataset.row);
            const j = parseInt(input.dataset.col);
            allocation[i][j] = parseInt(input.value) || 0;
        });
        
        // 获取最大需求矩阵
        const max = Array(p).fill().map(() => Array(r).fill(0));
        const maxInputs = document.querySelectorAll('.max-input');
        
        maxInputs.forEach(input => {
            const i = parseInt(input.dataset.row);
            const j = parseInt(input.dataset.col);
            max[i][j] = parseInt(input.value) || 0;
        });
        
        // 获取可用资源
        const available = Array(r).fill(0);
        const availableInputs = document.querySelectorAll('.available-input');
        
        availableInputs.forEach((input, j) => {
            available[j] = parseInt(input.value) || 0;
        });
        
        // 获取请求资源
        const request = Array(r).fill(0);
        const requestInputs = document.querySelectorAll('.request-input');
        
        requestInputs.forEach((input, j) => {
            request[j] = parseInt(input.value) || 0;
        });
        
        // 计算需求矩阵
        const need = Array(p).fill().map((_, i) => 
            Array(r).fill().map((_, j) => Math.max(0, max[i][j] - allocation[i][j]))
        );
        
        // 检查请求是否超过需求
        for (let j = 0; j < r; j++) {
            if (request[j] > need[processId][j]) {
                multiResult.innerHTML = `
                    <p class="unsafe">错误: 请求资源超过了进程P${processId}的最大需求</p>
                `;
                return;
            }
        }
        
        // 检查请求是否超过可用资源
        for (let j = 0; j < r; j++) {
            if (request[j] > available[j]) {
                multiResult.innerHTML = `
                    <p class="unsafe">错误: 请求资源超过了系统可用资源</p>
                `;
                return;
            }
        }
        
        // 尝试分配资源
        const tempAllocation = JSON.parse(JSON.stringify(allocation));
        const tempAvailable = JSON.parse(JSON.stringify(available));
        const tempNeed = JSON.parse(JSON.stringify(need));
        
        for (let j = 0; j < r; j++) {
            tempAvailable[j] -= request[j];
            tempAllocation[processId][j] += request[j];
            tempNeed[processId][j] -= request[j];
        }
        
        // 安全性检查
        const result = checkSafetyMultiResource(tempAllocation, max, tempNeed, tempAvailable, p, r);
        
        if (result.safe) {
            multiResult.innerHTML = `
                <p class="safe">请求可以被满足</p>
                <div class="sequence">安全序列: ${result.sequence.map(i => 'P' + i).join(' → ')}</div>
            `;
        } else {
            multiResult.innerHTML = `
                <p class="unsafe">请求不能被满足，会导致不安全状态</p>
            `;
        }
    });

    // 初始化生成表格
    generateSingleTable.click();
    generateTablesBtn.click();
});

// 单资源类型安全性检查算法
function checkSafetySingleResource(allocation, need, available, n) {
    const work = available;
    const finish = Array(n).fill(false);
    const safeSequence = [];
    
    let count = 0;
    while (count < n) {
        let found = false;
        
        for (let i = 0; i < n; i++) {
            if (!finish[i] && need[i] <= work) {
                work += allocation[i];
                finish[i] = true;
                safeSequence.push(i);
                found = true;
                count++;
                break;
            }
        }
        
        if (!found) {
            break;
        }
    }
    
    return {
        safe: count === n,
        sequence: safeSequence
    };
}

// 多资源类型安全性检查算法
function checkSafetyMultiResource(allocation, max, need, available, p, r) {
    const work = [...available];
    const finish = Array(p).fill(false);
    const safeSequence = [];
    
    let count = 0;
    while (count < p) {
        let found = false;
        
        for (let i = 0; i < p; i++) {
            if (!finish[i]) {
                let canAllocate = true;
                
                for (let j = 0; j < r; j++) {
                    if (need[i][j] > work[j]) {
                        canAllocate = false;
                        break;
                    }
                }
                
                if (canAllocate) {
                    for (let j = 0; j < r; j++) {
                        work[j] += allocation[i][j];
                    }
                    
                    finish[i] = true;
                    safeSequence.push(i);
                    found = true;
                    count++;
                    break;
                }
            }
        }
        
        if (!found) {
            break;
        }
    }
    
    return {
        safe: count === p,
        sequence: safeSequence
    };
}
