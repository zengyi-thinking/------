
class BankersAlgorithmUI:
    def __init__(self, root):
        self.root = root
        self.root.title("银行家算法模拟程序")
        
        # 初始化变量
        self.n_processes = tk.IntVar(value=3)  # 进程数
        self.n_resources = tk.IntVar(value=3)  # 资源种类数
        self.avail_entries = []
        self.alloc_entries = []
        self.max_entries = []
        
        # 创建控件
        self.create_widgets()
        