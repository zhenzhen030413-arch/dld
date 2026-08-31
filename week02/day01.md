# Week 2 Day 1：文件读写、JSON配置与诊断报告

## 1. 今日完成内容
理解了json文件的作用以及如何将json文件转化为py的内部字典逻辑

## 2. 核心概念

代码文件和配置文件的区别：
代码文件里面写 Python 程序逻辑，可以运行、可以执行。
配置文件里的例如config.json只有数据，没有可执行逻辑，不会运行

列表是什么：
列表是容器，可以存放一大堆数据，顺序保存，可以放多个元素，用方括号 `[]`。
比如results就是各个result字典的列表
字典是什么：
是键-值对的容器，用大括号{}表示
student = {
    "name": "FDE",
    "age": 22,
    "gender": "male"
}
with open的作用：

安全打开文件，离开自动关闭文件，不用手动输入.close（）
 r和w的区别：
r是只读模式，w是可以编辑

encoding="utf-8"的作用：
防止乱码

json.load的作用：
把json文件转化为py字典
json.dump的作用：
把py字典转化为json文件
## 3. 数据流

1.程序使用`json.load()`读取`config.json`，并转换成`config`字典
2.程序从config字典中取得文件输入名，输出名等    
3.程序读取'customer_paths.txt',把每个非空行转换成`raw_paths`列表中的一个字符串
4.`for`循环逐个检查`raw_paths`中的路径，每次生成一个`result`字典。
5.所有`result`字典加入`results`列表，程序再生成统计信息和完整的`report`字典。
6.程序使用`json.dump()`把`report`字典写入`report.json`文件。

## 4. 调试记录

config的数据类型和内容：

`config`的数据类型是字典（dict），内容包括项目名称、输入文件名、输出文件名、是否记录文件大小和操作人员：

`{"project_name": "FDE 客户路径巡检", "input_file": "customer_paths.txt", "output_file": "report.json", "include_file_size": True, "operator": "Dingzhen"}`

raw_paths的数据类型和内容：

`raw_paths`的数据类型是列表（list），其中包含4个需要检查的路径字符串：

`["../../week01/day01.md", "../../week01/day04/batch_path_checker.py", "../../week01", "../../week01/not_found.csv"]`

result的数据类型和内容：

`result`的数据类型是字典（dict），表示一个路径的检查结果。例如：

`{"input_path": "../../week01/day01.md", "absolute_path": "F:\\FDE\\dld\\week01\\day01.md", "exists": True, "type": "file", "suffix": ".md", "size_bytes": 1008}`

report的数据结构：

`report`是一个嵌套字典（dict），包含项目名称、输入文件路径、汇总字典、全部检查结果列表和操作人员。`summary`是字典，`results`是由4个result字典组成的列表。

## 5. 错误测试

| 测试 | 实际输出 | 是否通过 |
|---|---|---|
| 正常配置 | | |
| JSON格式错误 | | |
| 输入文件不存在 | | |
| 关闭文件大小 | | |
| 增加输入路径 | | |
| 恢复验证 | | |

## 6. 独立修改

增加的配置字段：

修改的Python位置：

为什么以后改名字不需要修改代码：因为config已经将信息变量摘出去了

## 7. FDE场景理解

客户需要改变输入文件时，为什么不应该直接修改Python代码：

配置文件损坏时，程序应该如何提示客户：

## 8. 路线复盘

当前能够独立完成：

仍然需要提示：

今天最不理解的代码：

是否达到今天验收要求：

下一步需要加强：

Agent衔接情况：

积累
load：文件 → Python
dump：Python → 文件
result = {}   # 一个路径的诊断字典
results = []  # 保存所有诊断字典的列表
result 是一个普通变量，保存的是一个 Python 字典 dict。它用来记录“一个路径”的全部检查结果
变量名 = {
    "键": 值,
    "键": 值
}
json.load(file)：JSON文件 → Python字典。
JSON配置：控制输入文件、输出文件、项目名称等参数。
BASE_DIR：当前 Python 文件所在文件夹。
config_path、input_path：函数接收的路径参数。
相对路径：用 BASE_DIR / target 拼成完整路径。
result：单个路径的检查结果字典。
results：保存多个 result 的列表。
for循环：逐个检查路径，并把结果加入列表。
report：包含汇总信息和全部检查结果的嵌套字典。
save_report(output_path, report)：把 report 写入 report.json。
json.dump()：Python字典 → JSON文件。
数据流：配置 → 输入路径 → 逐项检查 → 汇总 → 输出报告。
断点调试：观察 config、raw_paths、result、report 的变化。
F5：继续到下一断点；F10：执行当前行。
灰色代码建议：Tab接受，Esc忽略。
编辑撤销：Ctrl+Z；恢复：Ctrl+Y。