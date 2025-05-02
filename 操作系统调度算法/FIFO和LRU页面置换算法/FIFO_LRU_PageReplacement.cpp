#include <iostream>      // 包含标准输入输出流库，用于输入输出操作
#include <vector>        // 包含标准向量库，用于动态数组操作
#include <queue>         // 包含标准队列库，用于队列操作
#include <list>          // 包含标准列表库，用于双向链表操作
#include <unordered_set> // 包含标准无序集合库，用于哈希表实现的集合操作
#include <unordered_map> // 包含标准无序映射库，用于哈希表实现的键值对操作
#include <random>        // 包含标准随机数库，用于生成随机数
#include <iomanip>       // 包含标准参数化输入输出库，用于格式化输入输出
#include <locale>        // 包含标准本地化库，用于本地化设置和字符处理

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

        cout << "FIFO算法模拟过程：" << endl
             << flush;
        for (int i = 0; i < page_seq.size(); i++)
        {
            int page = page_seq[i];
            cout << "访问页面 " << page << ": " << flush;

            if (mem_set.find(page) != mem_set.end())
            {
                // 页面已在内存，无需操作
                cout << "命中" << endl
                     << flush;
                continue;
            }

            page_faults++; // 缺页
            cout << "缺页" << flush;

            if (q.size() == m)
            { // 内存已满，替换
                int victim = q.front();
                q.pop();
                mem_set.erase(victim);
                cout << "，替换页面 " << victim << flush;
            }
            // 加入新页面
            q.push(page);
            mem_set.insert(page);
            cout << endl
                 << flush;

            // 显示当前内存状态
            cout << "  当前内存状态: " << flush;
            queue<int> temp_q = q;
            while (!temp_q.empty())
            {
                cout << temp_q.front() << " " << flush;
                temp_q.pop();
            }
            cout << endl
                 << flush;
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

        cout << "LRU算法模拟过程：" << endl
             << flush;
        for (int i = 0; i < page_seq.size(); i++)
        {
            int page = page_seq[i];
            cout << "访问页面 " << page << ": " << flush;

            if (mem_map.find(page) != mem_map.end())
            {
                // 页面已在内存：移动到链表尾部（表示最近使用）
                cout << "命中，移至最近使用" << endl
                     << flush;
                lru_list.erase(mem_map[page]);
                lru_list.push_back(page);
                mem_map[page] = prev(lru_list.end());
                continue;
            }

            page_faults++; // 缺页
            cout << "缺页" << flush;

            if (lru_list.size() == m)
            { // 内存已满，替换
                int victim = lru_list.front();
                lru_list.pop_front();
                mem_map.erase(victim);
                cout << "，替换页面 " << victim << flush;
            }
            // 加入新页面到尾部
            lru_list.push_back(page);
            mem_map[page] = prev(lru_list.end());
            cout << endl
                 << flush;

            // 显示当前内存状态
            cout << "  当前内存状态: " << flush;
            for (int p : lru_list)
            {
                cout << p << " " << flush;
            }
            cout << endl
                 << flush;
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
    // 设置控制台输出
    ios_base::sync_with_stdio(false);

    // 同时输出到文件
    ofstream logFile("page_replacement_log.txt");
    if (!logFile)
    {
        cerr << "无法创建日志文件!" << endl;
    }

// 定义一个宏，同时输出到控制台和文件
#define LOG(x)            \
    do                    \
    {                     \
        cout << x;        \
        if (logFile)      \
            logFile << x; \
    } while (0)

    LOG("程序开始执行..." << endl
                          << flush);

    try
    {
        // 参数配置
        int m = 3, k = 5, L = 10; // 默认值，避免输入问题

        cout << "请输入内存块数(m): " << flush;
        cin >> m;
        cout << "输入的内存块数: " << m << endl
             << flush;

        cout << "请输入页面总数(k): " << flush;
        cin >> k;
        cout << "输入的页面总数: " << k << endl
             << flush;

        cout << "请输入访问序列长度(L): " << flush;
        cin >> L;
        cout << "输入的序列长度: " << L << endl
             << flush;

        // 生成随机访问序列
        cout << "正在生成随机访问序列..." << endl
             << flush;
        vector<int> seq = generate_page_sequence(k, L);
        cout << "页面访问序列：";
        for (int p : seq)
            cout << p << " ";
        cout << endl
             << endl
             << flush;

        // 创建模拟器
        cout << "创建模拟器..." << endl
             << flush;
        FIFO_Replacer fifo(m, seq);
        LRU_Replacer lru(m, seq);

        // 运行模拟
        cout << "\n=== FIFO算法模拟 ===" << endl
             << flush;
        int fifo_faults = fifo.simulate();

        cout << "\n=== LRU算法模拟 ===" << endl
             << flush;
        int lru_faults = lru.simulate();

        // 输出结果
        cout << "\n=== 比较结果 ===" << endl
             << flush;
        cout << "FIFO缺页次数: " << fifo_faults
             << " (缺页率: " << fixed << setprecision(2) << (fifo_faults * 100.0 / L) << "%)" << endl
             << flush;
        cout << "LRU 缺页次数: " << lru_faults
             << " (缺页率: " << fixed << setprecision(2) << (lru_faults * 100.0 / L) << "%)" << endl
             << flush;
    }
    catch (const exception &e)
    {
        cout << "程序发生异常: " << e.what() << endl
             << flush;
    }
    catch (...)
    {
        cout << "程序发生未知异常" << endl
             << flush;
    }

    // 防止程序立即退出
    cout << "\n按Enter键退出程序..." << flush;
    cin.ignore();
    cin.get();

    return 0;
}