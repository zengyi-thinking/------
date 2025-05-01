function bankers_algorithm
    % 示例测试数据
    n_processes = 2; % 进程数
    n_resources = 3; % 资源种类数
    
    % 分配矩阵
    allocation = [0 1 0; 2 0 0];
    
    % 最大需求矩阵
    max_demand = [7 5 3; 3 2 2];
    
    % 可用资源
    available = [3 3 2];
    
    % 显示初始数据
    disp('初始数据:');
    disp(['进程数: ', num2str(n_processes)]);
    disp(['资源种类: ', num2str(n_resources)]);
    disp('分配矩阵:');
    disp(allocation);
    disp('最大需求矩阵:');
    disp(max_demand);
    disp('可用资源:');
    disp(available);
    
    % 检查安全性
    [is_safe, safe_sequence] = check_safety(allocation, max_demand, available);
    if is_safe
        disp('系统处于安全状态');
        disp(['安全序列: ', strjoin(safe_sequence, ' -> ')]);
    else
        disp('系统处于不安全状态');
    end
    
    % 处理资源请求
    pid = 1; % 请求资源的进程号 (1-based index)
    request = [1 0 2]; % 请求的资源数量
    
    % 处理请求
    [request_accepted, new_safe_sequence] = handle_request(allocation, max_demand, available, pid, request);
    if request_accepted
        disp(['请求被接受，系统处于安全状态']);
        disp(['新的安全序列: ', strjoin(new_safe_sequence, ' -> ')]);
    else
        disp('请求被拒绝，系统处于不安全状态');
    end
end

function [is_safe, safe_sequence] = check_safety(allocation, max_demand, available)
    n_processes = size(allocation, 1);
    n_resources = size(allocation, 2);
    
    % 计算需求矩阵
    need = max_demand - allocation;
    
    work = available;
    finish = false(1, n_processes);
    safe_sequence = {};
    
    while true
        found = false;
        for i = 1:n_processes
            if ~finish(i) && all(need(i, :) <= work)
                % 分配资源
                work = work + allocation(i, :);
                finish(i) = true;
                safe_sequence{end+1} = sprintf('P%d', i);
                found = true;
                break;
            end
        end
        if ~found
            break;
        end
    end
    
    is_safe = all(finish);
end

function [request_accepted, new_safe_sequence] = handle_request(allocation, max_demand, available, pid, request)
    n_processes = size(allocation, 1);
    n_resources = size(allocation, 2);
    
    % 验证请求
    if pid < 1 || pid > n_processes
        error('无效的进程号');
    end
    
    if length(request) ~= n_resources
        error('请求资源数量不匹配');
    end
    
    % 计算需求矩阵
    need = max_demand - allocation;
    
    % 检查1：请求是否小于等于需求
    if any(request > need(pid, :))
        error('请求资源超过需求');
    end
    
    % 检查2：请求是否小于等于可用资源
    if any(request > available)
        error('请求资源超过可用资源');
    end
    
    % 模拟分配
    new_available = available - request;
    new_allocation = allocation;
    new_allocation(pid, :) = new_allocation(pid, :) + request;
    
    % 执行安全性检查
    [is_safe, new_safe_sequence] = check_safety(new_allocation, max_demand, new_available);
    
    request_accepted = is_safe;
end