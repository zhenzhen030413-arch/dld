# WEEK02 Day02

## 今天学习内容

- Python Function
- List
- Dictionary
- JSON
- try / except
- Agent
- Tool
- Tool Routing

## 我的理解

Agent：

Agent接收用户的问题，判断问题属于什么类型，再选择对应的工具处理，最后返回结构化结果。今天实现的是基于关键词判断的规则型Agent，还没有使用LLM。

Tool：

Tool是Agent能够调用的一项具体能力。在今天的项目中，`git_tool()`、`api_tool()`、`python_tool()`和`frontend_tool()`都是不同的工具函数，分别提供对应问题的检查建议。

JSON：

JSON是一种结构化数据格式，使用键和值保存信息。Python字典可以通过`json.dump()`写入JSON文件，也可以通过`json.load()`读取JSON文件。今天程序把Agent的分析结果保存到了`agent_result.json`。

## 今日项目

FDE Customer Issue Triage Agent v0.1

该程序接收客户问题，通过`detect_category()`判断问题类别，再从`TOOLS`工具注册表中选择对应的工具函数，最后把分析结果显示在终端并保存为JSON文件。

流程：

Customer Issue → Router → Tool → Result → JSON
                  用户问题
                     │
                     ▼
              ┌─────────────┐
              │ Agent Router│
              │ 判断问题类型 │
              └──────┬──────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
      Git Tool    API Tool   Python Tool 
          │          │          │
          └──────────┼──────────┘
                     ▼
                Tool Result
                     │
                     ▼
                Agent 
## Git Tool（Git 工具）

专门用来操作 Git 代码仓库的工具。

- 能干什么：查看代码提交记录、看代码改动 diff、创建 / 切换分支、提交代码、拉取仓库代码、查看仓库文件状态。
- 使用场景：用户问代码仓库相关问题，比如 “看这个项目最近改了什么”、“帮我提交代码”、“对比两个版本代码差异”，Router 就会路由到 Git Tool。
- 简单说：**让 AI 直接操作代码版本仓库**。
## 2. API Tool（接口工具）

用来调用外部网络 API 接口。

- 能干什么：向外部服务发 http 请求，拿第三方数据；调用其他系统接口，查询实时数据，提交数据到别的服务。
- 使用场景：需要联网拿外部信息，调用第三方服务，比如查天气、调用业务后端接口、获取公开网络数据。
- 简单说：**AI 通过网络，和别的软件 / 服务对话拿数据**。
## 3. Python Tool（Python 代码执行工具，类似 Code Interpreter）

可以运行 Python 代码片段的工具。

- 能干什么：数值计算、数据处理、数据分析、文件处理、写脚本、算法运算，处理复杂逻辑。
- 使用场景：做数学计算、数据统计、处理表格、需要写代码完成逻辑任务的时候。
- 简单说：**给 AI 一个可以跑 Python 代码的沙箱环境，靠代码算出结果**。

- `json.dumps()`：输出字符串（给 print 打印用）
- `json.dump()`：直接写入文件