#include <iostream>
#include <vector>
#include <queue>
#include <list>
#include <unordered_set>
#include <unordered_map>
#include <random>

using namespace std;

// 基类：页面置换器
class PageReplacer
{
protected:
    int m;                // 内存块数
    vector<int> page_seq; // 页面访问序列
public:
    PageReplacer(int mem_blocks, const vector<int> &seq)
        : m(mem_blocks), page_seq(seq) {}
    virtual int simulate() = 0; // 模拟算法并返回缺页次数
};

// FIFO算法实现
class FIFO_Replacer : public PageReplacer
{
private:
    queue<int> q;               // 队列维护页面进入顺序
    unordered_set<int> mem_set; // 快速判断页面是否在内存
public:
    FIFO_Replacer(int m, const vector<int> &seq) : PageReplacer(m, seq) {}

    int simulate() override
    {
        q = queue<int>(); // 清空队列
        mem_set.clear();
        int page_faults = 0;

        for (int page : page_seq)
        {
            if (mem_set.find(page) != mem_set.end())
            {
                // 页面已在内存，无需操作
                continue;
            }

            page_faults++; // 缺页
            if (q.size() == m)
            { // 内存已满，替换
                int victim = q.front();
                q.pop();
                mem_set.erase(victim);
            }
            // 加入新页面
            q.push(page);
            mem_set.insert(page);
        }
        return page_faults;
    }
};

// LRU算法实现
class LRU_Replacer : public PageReplacer
{
private:
    list<int> lru_list;                              // 链表维护最近使用顺序（头部最久未用）
    unordered_map<int, list<int>::iterator> mem_map; // 快速定位页面位置
public:
    LRU_Replacer(int m, const vector<int> &seq) : PageReplacer(m, seq) {}

    int simulate() override
    {
        lru_list.clear();
        mem_map.clear();
        int page_faults = 0;

        for (int page : page_seq)
        {
            if (mem_map.find(page) != mem_map.end())
            {
                // 页面已在内存：移动到链表尾部（表示最近使用）
                lru_list.erase(mem_map[page]);
                lru_list.push_back(page);
                mem_map[page] = prev(lru_list.end());
                continue;
            }

            page_faults++; // 缺页
            if (lru_list.size() == m)
            { // 内存已满，替换
                int victim = lru_list.front();
                lru_list.pop_front();
                mem_map.erase(victim);
            }
            // 加入新页面到尾部
            lru_list.push_back(page);
            mem_map[page] = prev(lru_list.end());
        }
        return page_faults;
    }
};

// 生成随机页面访问序列
vector<int> generate_page_sequence(int k, int L)
{
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> distr(1, k); // 页面ID范围1~k

    vector<int> seq;
    for (int i = 0; i < L; ++i)
    {
        seq.push_back(distr(gen));
    }
    return seq;
}

int main()
{
    // 参数配置
    int m = 3;  // 内存块数
    int k = 5;  // 页面总数（1~5）
    int L = 10; // 访问序列长度

    // 生成随机访问序列
    vector<int> seq = generate_page_sequence(k, L);
    cout << "页面访问序列：";
    for (int p : seq)
        cout << p << " ";
    cout << endl;

    // 创建模拟器
    FIFO_Replacer fifo(m, seq);
    LRU_Replacer lru(m, seq);

    // 运行模拟
    int fifo_faults = fifo.simulate();
    int lru_faults = lru.simulate();

    // 输出结果
    cout << "\n--- 比较结果 ---" << endl;
    cout << "FIFO缺页次数: " << fifo_faults
         << " (缺页率: " << (fifo_faults * 100.0 / L) << "%)" << endl;
    cout << "LRU 缺页次数: " << lru_faults
         << " (缺页率: " << (lru_faults * 100.0 / L) << "%)" << endl;

    return 0;
}