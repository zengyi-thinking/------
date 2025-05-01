//编码格式打开：UTF-8with BOM
//测试样例输入：3
// J1 0900 60
// J2 0930 30
// J3 1000 15

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

// 定义作业类
class Job {
    String jobId; // 作业ID
    int submitTime; // 提交时间
    int runningTime; // 运行时间
    int startTime; // 开始时间
    int completeTime; // 完成时间
    int turnAroundTime; // 周转时间
    double weightTurnAroundTime; // 带权周转时间
    double responseRatio; // 响应比

    // 构造函数
    public Job(String jobId, int submitTime, int runningTime) {
        this.jobId = jobId;
        this.submitTime = submitTime;
        this.runningTime = runningTime;
    }

    // 计算响应比
    public void calculateResponseRatio(int currentTime) {
        int waitTime = currentTime - submitTime;
        if (runningTime > 0) {
            responseRatio = (double) (waitTime + runningTime) / runningTime;
        }
    }

    // 计算周转时间和带权周转时间
    public void calculateTurnAroundTime() {
        turnAroundTime = completeTime - submitTime;
        weightTurnAroundTime = (double) turnAroundTime / runningTime;
    }
}

// HRRN调度算法类
public class HRRN_Scheduler extends JFrame {
    private JTextArea inputArea; // 输入文本区域
    private JTextArea outputArea; // 输出文本区域
    private ArrayList<Job> jobs; // 作业列表

    // 构造函数
    public HRRN_Scheduler() {
        jobs = new ArrayList<>();
        setTitle("HRRN调度算法");
        setSize(600, 400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // 输入面板
        JPanel inputPanel = new JPanel();
        JLabel infoLabel = new JLabel("输入格式: K TJ1 YS1 ... TJK YSK");
        inputArea = new JTextArea(5, 50);
        outputArea = new JTextArea(10, 50);
        outputArea.setEditable(false);
        JScrollPane outputScroll = new JScrollPane(outputArea);
        JButton runButton = new JButton("运行调度");

        // 设置输入面板布局
        inputPanel.setLayout(new BorderLayout());
        inputPanel.add(infoLabel, BorderLayout.NORTH);
        inputPanel.add(new JScrollPane(inputArea), BorderLayout.CENTER);
        inputPanel.add(runButton, BorderLayout.SOUTH);

        // 添加组件到主窗口
        add(inputPanel, BorderLayout.NORTH);
        add(outputScroll, BorderLayout.CENTER);

        // 运行按钮事件监听
        runButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String input = inputArea.getText();
                processInput(input);
            }
        });
    }

    // 处理输入数据
    private void processInput(String input) {
        try {
            jobs.clear();
            String[] lines = input.trim().split("\\s*\\n\\s*");
            int K = Integer.parseInt(lines[0].trim());

            // 解析每一行作业数据
            for (int i = 1; i <= K; i++) {
                String[] parts = lines[i].trim().split("\\s+");
                String jobId = parts[0];
                String timeString = parts[1];
                int submitTime = convertToMinutes(timeString);
                int runningTime = Integer.parseInt(parts[2]);
                jobs.add(new Job(jobId, submitTime, runningTime));
            }
            runHRRNAlgorithm();
        } catch (Exception e) {
            outputArea.setText("输入格式错误！");
        }
    }

    // 将时间字符串转换为分钟
    private int convertToMinutes(String timeString) {
        int hour = Integer.parseInt(timeString.substring(0, 2));
        int minute = Integer.parseInt(timeString.substring(2, 4));
        return hour * 60 + minute;
    }

    // 运行HRRN调度算法
    private void runHRRNAlgorithm() {
        outputArea.setText("调度过程:\n");
        int currentTime = 0;
        ArrayList<Job> completedJobs = new ArrayList<>();

        // 循环直到所有作业完成
        while (!jobs.isEmpty()) {
            ArrayList<Job> arrivedJobs = new ArrayList<>();
            // 获取当前时间已到达的作业
            for (Job job : jobs) {
                if (job.submitTime <= currentTime) {
                    job.calculateResponseRatio(currentTime);
                    arrivedJobs.add(job);
                }
            }

            // 如果没有到达的作业，跳到下一个作业的提交时间
            if (arrivedJobs.isEmpty()) {
                int minSubmitTime = Integer.MAX_VALUE;
                for (Job job : jobs) {
                    if (job.submitTime < minSubmitTime) {
                        minSubmitTime = job.submitTime;
                    }
                }
                currentTime = minSubmitTime;
                continue;
            }

            // 按响应比排序
            Collections.sort(arrivedJobs, new Comparator<Job>() {
                @Override
                public int compare(Job j1, Job j2) {
                    return Double.compare(j2.responseRatio, j1.responseRatio);
                }
            });

            // 选择响应比最高的作业
            Job selectedJob = arrivedJobs.get(0);
            jobs.remove(selectedJob);
            selectedJob.startTime = currentTime;
            currentTime += selectedJob.runningTime;
            selectedJob.completeTime = currentTime;
            selectedJob.calculateTurnAroundTime();
            completedJobs.add(selectedJob);

            // 输出调度结果
            outputArea.append(String.format(
                    "调度次数: %d，作业ID: %s，提交时间: %d，开始时间: %d，运行时间: %d，完成时间: %d，周转时间: %d，带权周转时间: %.2f\n",
                    (outputArea.getLineCount() + 1), selectedJob.jobId,
                    selectedJob.submitTime, selectedJob.startTime,
                    selectedJob.runningTime, selectedJob.completeTime,
                    selectedJob.turnAroundTime, selectedJob.weightTurnAroundTime));
        }

        // 计算平均周转时间和平均带权周转时间
        double totalTurnAroundTime = 0;
        double totalWeightTurnAroundTime = 0;
        for (Job job : completedJobs) {
            totalTurnAroundTime += job.turnAroundTime;
            totalWeightTurnAroundTime += job.weightTurnAroundTime;
        }

        int jobCount = completedJobs.size();
        if (jobCount > 0) {
            outputArea.append(String.format(
                    "平均周转时间: %.2f，平均带权周转时间: %.2f\n",
                    totalTurnAroundTime / jobCount,
                    totalWeightTurnAroundTime / jobCount));
        }
    }

    // 主函数
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            HRRN_Scheduler window = new HRRN_Scheduler();
            window.setVisible(true);
        });
    }
}
