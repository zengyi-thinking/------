# -*- coding: utf-8 -*-
import random  # 导入random模块，用于生成随机数
from collections import deque, OrderedDict  # 从collections模块导入deque和OrderedDict类

def generate_page_sequence(k, L):
    """生成随机页面访问序列"""
    return [random.randint(1, k) for _ in range(L)]

class FIFOReplacer:
    """FIFO 页面置换算法实现"""
    def __init__(self, m):
        self.m = m            # 内存块数
        self.queue = deque()  # 维护页面进入顺序
        self.pages = set()    # 快速判断页面是否存在
        self.page_faults = 0  # 缺页次数

    def simulate(self, seq):
        """模拟页面访问过程"""
        for page in seq:
            if page in self.pages:
                continue     # 页面已在内存，无缺页

            self.page_faults += 1
            if len(self.queue) >= self.m:
                # 内存已满，移除最早进入的页面
                removed = self.queue.popleft()
                self.pages.remove(removed)

            # 将新页面加入队列和集合
            self.queue.append(page)
            self.pages.add(page)
        return self.page_faults

class LRUReplacer:
    """LRU 页面置换算法实现"""
    def __init__(self, m):
        self.m = m                   # 内存块数
        self.cache = OrderedDict()   # 维护页面使用顺序
        self.page_faults = 0         # 缺页次数

    def simulate(self, seq):
        """模拟页面访问过程"""
        for page in seq:
            if page in self.cache:
                # 页面已在内存：移动到末尾表示最近使用
                self.cache.move_to_end(page)
                continue

            self.page_faults += 1
            if len(self.cache) >= self.m:
                # 内存已满，移除最久未使用的页面（第一个）
                self.cache.popitem(last=False)

            # 添加新页面到末尾
            self.cache[page] = None
        return self.page_faults

def main():
    # 参数配置（可修改）
    m = 3  # 内存块数
    k = 5  # 页面总数（ID范围1~k）
    L = 10 # 访问序列长度

    # 生成随机页面访问序列
    seq = generate_page_sequence(k, L)
    print("页面访问序列:", seq)

    # 运行FIFO算法
    fifo = FIFOReplacer(m)
    fifo_faults = fifo.simulate(seq)

    # 运行LRU算法
    lru = LRUReplacer(m)
    lru_faults = lru.simulate(seq)

    # 输出比较结果
    print("\n--- 比较结果 ---")
    print(f"FIFO缺页次数: {fifo_faults} (缺页率: {fifo_faults * 100 / L:.1f}%)")
    print(f"LRU 缺页次数: {lru_faults} (缺页率: {lru_faults * 100 / L:.1f}%)")

if __name__ == "__main__":
    main()