1. Function Calling 是什么？
function calling不是简单的调用函数，他是LLM输出结构化指令→本地程序执行函数→结果返回给LLM这一整个交互机制，它相当于告诉LLM，我有一套函数工具可以给你做出，工具调用指令
2.为什么说 LLM 并没有直接执行 Python 函数？
（1）能力本质不同：LLM其实只是阅读了本地程序的对话和tools的工具库，并基于用户问题做出相应的调用指令，并不是真的运行函数
（2）环境隔离：LLM运行在远程的服务器上
（3）只负责决策，决定权在本地
3.Tool Schema 和真正 Python 函数有什么区别？
只是阅读工具的json文件的参数

1.subprocess.run()让 Python 帮你打开终端执行一个程序。
subprocess.run(["git", "status"])近似等于你自己在终端输入：git status
2.return_code
result.returncode  0=程序正常执行
