# 操作系统调度算法

本仓库包含操作系统课程中常见的调度算法实现，包括进程调度算法和页面置换算法等。

## 项目结构

```
.
├── 操作系统调度算法/
│   ├── FIFO和LRU页面置换算法/
│   │   ├── FIFO_LRU_PageReplacement.cpp - C++实现的FIFO和LRU页面置换算法
│   │   └── FIFO_LRU_PageReplacement.py - Python实现的FIFO和LRU页面置换算法
│   └── ... (其他调度算法)
└── ... (其他操作系统相关实现)
```

## 已实现的算法

### 页面置换算法

- **FIFO (First-In-First-Out)**: 最先进入内存的页面最先被置换出去
- **LRU (Least Recently Used)**: 最近最少使用页面置换算法，置换最长时间未被引用的页面

## 如何运行

### Python版本

```bash
python 操作系统调度算法/FIFO和LRU页面置换算法/FIFO_LRU_PageReplacement.py
```

### C++版本

```bash
# 编译
g++ 操作系统调度算法/FIFO和LRU页面置换算法/FIFO_LRU_PageReplacement.cpp -o FIFO_LRU_PageReplacement

# 运行
./FIFO_LRU_PageReplacement
```

## 算法说明

### FIFO页面置换算法

FIFO（First-In-First-Out）页面置换算法是最简单的页面置换算法。该算法总是淘汰最先进入内存的页面，即选择在内存中驻留时间最长的页面予以淘汰。

### LRU页面置换算法

LRU（Least Recently Used）页面置换算法是一种常用的页面置换算法，选择最近最久未使用的页面予以淘汰。该算法赋予每个页面一个访问字段，用来记录上次页面被访问到现在所经历的时间t，当须淘汰一个页面时，选择现有页面中其t值最大的，即最近最少使用的页面予以淘汰。

## 贡献

欢迎提交Pull Request或Issue来完善本项目。

## 许可

MIT License
