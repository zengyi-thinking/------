import unittest
from bankers_algorithm import BankersAlgorithmUI  # 修改导入语句
import tkinter as tk  # 显式导入tkinter

class TestBankersAlgorithm(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = BankersAlgorithmUI(self.root)
        
    def tearDown(self):
        self.root.destroy()

    def test_check_safety(self):
        # 测试安全状态
        self.app.n_processes.set(5)
        self.app.n_resources.set(3)
        self.app.generate_matrices()
        
        # 设置分配矩阵
        alloc_data = [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2]
        ]
        for i in range(5):
            for j in range(3):
                self.app.alloc_entries[i][j].delete(0, tk.END)
                self.app.alloc_entries[i][j].insert(0, str(alloc_data[i][j]))
        
        # 设置最大需求矩阵
        max_data = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3]
        ]
        for i in range(5):
            for j in range(3):
                self.app.max_entries[i][j].delete(0, tk.END)
                self.app.max_entries[i][j].insert(0, str(max_data[i][j]))
        
        # 设置可用资源
        avail_data = [3, 3, 2]
        for j in range(3):
            self.app.avail_entries[j].delete(0, tk.END)
            self.app.avail_entries[j].insert(0, str(avail_data[j]))
        
        # 检查安全性
        self.app.check_safety()
        result = self.app.result_text.get(1.0, tk.END).strip()
        self.assertIn("系统处于安全状态", result)
        
    def test_handle_request(self):
        # 测试资源请求处理
        self.app.n_processes.set(5)
        self.app.n_resources.set(3)
        self.app.generate_matrices()
        
        # 设置分配矩阵（同上）
        alloc_data = [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2]
        ]
        for i in range(5):
            for j in range(3):
                self.app.alloc_entries[i][j].delete(0, tk.END)
                self.app.alloc_entries[i][j].insert(0, str(alloc_data[i][j]))
        
        # 设置最大需求矩阵（同上）
        max_data = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3]
        ]
        for i in range(5):
            for j in range(3):
                self.app.max_entries[i][j].delete(0, tk.END)
                self.app.max_entries[i][j].insert(0, str(max_data[i][j]))
        
        # 设置可用资源（同上）
        avail_data = [3, 3, 2]
        for j in range(3):
            self.app.avail_entries[j].delete(0, tk.END)
            self.app.avail_entries[j].insert(0, str(avail_data[j]))
        
        # 发送资源请求
        self.app.pid_entry.delete(0, tk.END)
        self.app.pid_entry.insert(0, "1")  # 进程号（从1开始）
        self.app.request_entry.delete(0, tk.END)
        self.app.request_entry.insert(0, "1 0 2")  # 请求资源
        
        # 处理请求
        self.app.handle_request()
        result = self.app.result_text.get(1.0, tk.END).strip()
        self.assertIn("请求被接受，系统处于安全状态", result)

if __name__ == "__main__":
    unittest.main()
