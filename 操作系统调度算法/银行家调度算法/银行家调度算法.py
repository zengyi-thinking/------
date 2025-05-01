# 示例测试数据：
# 进程数: 2
# 资源种类: 3
#
# 分配矩阵（Allocation Matrix）:
# | 0 | 1 | 0 |
# | 2 | 0 | 0 |
#
# 最大需求矩阵（Maximum Demand Matrix）:
# | 7 | 5 | 3 |
# | 3 | 2 | 2 |
#
# 可用资源（Available Resources）:
# | 3 | 3 | 2 |

import tkinter as tk
from tkinter import ttk, messagebox

class BankersAlgorithmUI:
    def __init__(self, root):
        self.root = root
        self.root.title("银行家算法模拟程序")
        
        # 初始化变量
        self.n_processes = tk.IntVar(value=3)  # 进程数
        self.n_resources = tk.IntVar(value=3)  # 资源种类数
        self.avail_entries = []  # 可用资源输入框列表
        self.alloc_entries = []  # 分配矩阵输入框列表
        self.max_entries = []  # 最大需求矩阵输入框列表
        
        # 创建控件
        self.create_widgets()
        
    def create_widgets(self):
        # 控制面板
        control_frame = ttk.LabelFrame(self.root, text="控制面板")
        control_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        ttk.Label(control_frame, text="进程数:").grid(row=0, column=0)
        ttk.Spinbox(control_frame, from_=1, to=10, textvariable=self.n_processes, width=5).grid(row=0, column=1)
        
        ttk.Label(control_frame, text="资源种类:").grid(row=0, column=2)
        ttk.Spinbox(control_frame, from_=1, to=10, textvariable=self.n_resources, width=5).grid(row=0, column=3)
        
        ttk.Button(control_frame, text="生成矩阵", command=self.generate_matrices).grid(row=0, column=4, padx=5)

        # 矩阵面板
        self.matrix_frame = ttk.Frame(self.root)
        self.matrix_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        # 结果面板
        result_frame = ttk.LabelFrame(self.root, text="结果")
        result_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        self.result_text = tk.Text(result_frame, height=8, width=60)
        self.result_text.pack(padx=5, pady=5)
        
        # 请求面板
        request_frame = ttk.LabelFrame(self.root, text="资源请求")
        request_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        
        ttk.Label(request_frame, text="进程号:").grid(row=0, column=0)
        self.pid_entry = ttk.Entry(request_frame, width=5)
        self.pid_entry.grid(row=0, column=1)
        
        ttk.Label(request_frame, text="请求资源:").grid(row=0, column=2)
        self.request_entry = ttk.Entry(request_frame, width=20)
        self.request_entry.grid(row=0, column=3)
        
        ttk.Button(request_frame, text="处理请求", command=self.handle_request).grid(row=0, column=4)

    def generate_matrices(self):
        # 清除原有控件
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        
        n = self.n_processes.get()
        m = self.n_resources.get()
        
        # 分配矩阵
        alloc_frame = ttk.LabelFrame(self.matrix_frame, text="分配矩阵")
        alloc_frame.grid(row=0, column=0, padx=5, pady=5)
        
        self.alloc_entries = []
        for i in range(n):
            row = []
            for j in range(m):
                e = ttk.Entry(alloc_frame, width=5)
                e.grid(row=i, column=j, padx=2, pady=2)
                row.append(e)
            self.alloc_entries.append(row)
        
        # 最大需求矩阵
        max_frame = ttk.LabelFrame(self.matrix_frame, text="最大需求矩阵")
        max_frame.grid(row=0, column=1, padx=5, pady=5)
        
        self.max_entries = []
        for i in range(n):
            row = []
            for j in range(m):
                e = ttk.Entry(max_frame, width=5)
                e.grid(row=i, column=j, padx=2, pady=2)
                row.append(e)
            self.max_entries.append(row)
        
        # 可用资源
        avail_frame = ttk.LabelFrame(self.matrix_frame, text="可用资源")
        avail_frame.grid(row=0, column=2, padx=5, pady=5)
        
        self.avail_entries = []
        for j in range(m):
            e = ttk.Entry(avail_frame, width=5)
            e.grid(row=0, column=j, padx=2, pady=2)
            self.avail_entries.append(e)
        
        # 全局检查按钮
        ttk.Button(self.matrix_frame, text="全局检查", command=self.check_safety).grid(row=1, column=1, pady=5)

    def get_matrix_data(self):
        try:
            n = self.n_processes.get()
            m = self.n_resources.get()
            
            # 获取分配矩阵
            alloc = []
            for i in range(n):
                row = []
                for j in range(m):
                    row.append(int(self.alloc_entries[i][j].get()))
                alloc.append(row)
            
            # 获取最大需求矩阵
            max_demand = []
            for i in range(n):
                row = []
                for j in range(m):
                    row.append(int(self.max_entries[i][j].get()))
                max_demand.append(row)
            
            # 获取可用资源
            available = [int(e.get()) for e in self.avail_entries]
            
            return alloc, max_demand, available
        
        except ValueError:
            messagebox.showerror("错误", "无效的输入")
            return None, None, None

    def check_safety(self):
        # 获取分配矩阵、最大需求矩阵和可用资源矩阵
        alloc, max_demand, available = self.get_matrix_data()
        if alloc is None:
            return
        
        # 验证矩阵维度一致性
        n = len(alloc)  # 获取分配矩阵的行数，即进程数
        m = len(available)  # 获取可用资源矩阵的列数，即资源种类数
        if any(len(row) != m for row in alloc) or any(len(row) != m for row in max_demand):
            messagebox.showerror("错误", "矩阵维度不一致")
            return
        
        # 计算需求矩阵
        need = [[max_demand[i][j] - alloc[i][j] for j in range(m)] for i in range(n)]
        
        work = available.copy()
        finish = [False]*n
        safe_seq = []
        
        while True:
            found = False
            for i in range(n):
                if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                    # 分配资源
                    work = [work[j] + alloc[i][j] for j in range(m)]
                    finish[i] = True
                    safe_seq.append(i)
                    found = True
                    break
            if not found:
                break
    
        self.result_text.delete(1.0, tk.END)
        if all(finish):
            self.result_text.insert(tk.END, "系统处于安全状态\n")
            self.result_text.insert(tk.END, "安全序列: " + " -> ".join(f"P{p+1}" for p in safe_seq))
        else:
            self.result_text.insert(tk.END, "系统处于不安全状态")

    def handle_request(self):
        try:
            pid = int(self.pid_entry.get()) - 1  # 转换为0-based索引
            request = list(map(int, self.request_entry.get().split()))
            
            alloc, max_demand, available = self.get_matrix_data()
            if alloc is None:
                return
            
            # 验证请求
            if not (0 <= pid < len(alloc)):
                messagebox.showerror("错误", "无效的进程号")
                return
            
            if len(request) != len(available):
                messagebox.showerror("错误", "请求资源数量不匹配")
                return
            
            # 验证矩阵维度一致性
            n = len(alloc)
            m = len(available)
            if any(len(row) != m for row in alloc) or any(len(row) != m for row in max_demand):
                messagebox.showerror("错误", "矩阵维度不一致")
                return
            
            # 检查1：请求是否小于等于需求
            need = [max_demand[pid][j] - alloc[pid][j] for j in range(len(available))]
            if any(request[j] > need[j] for j in range(len(request))):
                messagebox.showerror("错误", "请求资源超过需求")
                return
                
            # 检查2：请求是否小于等于可用资源
            if any(request[j] > available[j] for j in range(len(request))):
                messagebox.showerror("错误", "请求资源超过可用资源")
                return
                
            # 模拟分配
            new_available = [available[j] - request[j] for j in range(len(available))]
            new_alloc = [row.copy() for row in alloc]
            new_alloc[pid] = [new_alloc[pid][j] + request[j] for j in range(len(request))]
            
            # 执行安全性检查
            need = [[max_demand[i][j] - new_alloc[i][j] for j in range(len(available))] for i in range(len(alloc))]
            work = new_available.copy()
            finish = [False]*len(alloc)
            safe_seq = []
            
            while True:
                found = False
                for i in range(len(alloc)):
                    if not finish[i] and all(need[i][j] <= work[j] for j in range(len(work))):
                        work = [work[j] + new_alloc[i][j] for j in range(len(work))]
                        finish[i] = True
                        safe_seq.append(i)
                        found = True
                        break
                if not found:
                    break
            
            self.result_text.delete(1.0, tk.END)
            if all(finish):
                self.result_text.insert(tk.END, "请求被接受，系统处于安全状态\n")
                self.result_text.insert(tk.END, "安全序列: " + " -> ".join(f"P{p+1}" for p in safe_seq))
            else:
                self.result_text.insert(tk.END, "请求被拒绝，系统处于不安全状态")
                
        except ValueError:
            messagebox.showerror("错误", "无效的输入格式")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankersAlgorithmUI(root)
    root.mainloop()