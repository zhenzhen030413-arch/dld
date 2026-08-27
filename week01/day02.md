# Week 1 Day 2：PowerShell 基础与 Git 闭环

## 1. 今日学习目标

- 理解 VS Code、终端、PowerShell、Git 和 GitHub 的区别。
- 理解当前目录、绝对路径和相对路径。
- 掌握常用的 PowerShell 文件操作命令。
- 理解 Git 从本地修改到 GitHub 合并的完整流程。

## 2. 基本概念

**VS Code：** 用于打开、查看和编辑电脑本地文件的软件。VS Code 不是 GitHub 在本地的保存形式；真正保存在电脑上的是本地项目文件夹，VS Code 只是打开并显示它。

**终端（Terminal）：** 用于输入命令并查看执行结果的窗口。VS Code 下方的 Terminal 就是一个终端窗口。

**PowerShell：** Windows 的命令行工具和脚本环境，负责理解并执行终端中输入的命令。

**Git：** 分布式版本控制工具，用于记录文件修改、创建版本、管理分支，以及与远程仓库同步。Git 不负责编辑或运行代码。

**GitHub：** 在线代码托管与协作平台，用于保存远程 Git 仓库，并提供 Pull Request、代码审查和团队协作等功能。

本地与远程的关系：

```text
GitHub 远程仓库
      ↑ git push
      ↓ git pull
电脑中的本地项目文件夹
      ↕
VS Code 查看和编辑
```

PowerShell 不是同步文件的唯一方式。也可以使用 VS Code 的“源代码管理”界面或 GitHub Desktop；无论使用哪种界面，底层真正执行版本管理和同步的都是 Git。

## 3. 路径概念

**当前目录：** 终端当前所在的文件夹。命令中的相对路径会从这里开始计算。

**绝对路径：** 从磁盘盘符开始，完整表示文件或文件夹位置的路径，例如：

```text
F:\FDE\dld\week01\day01.md
```

**相对路径：** 以当前目录为起点表示文件位置的路径。假设当前目录是 `F:\FDE\dld`，同一个文件可以写成：

```text
.\week01\day01.md
```

- `.` 表示当前目录。
- `..` 表示上一级目录。

`Get-Location` 只显示当前目录，不会切换目录，也不能直接告诉我们目标文件在哪里；`Set-Location` 才负责切换目录。

## 4. 今日使用的命令

| 命令 | 作用 |
|---|---|
| `Get-Location` | 显示终端当前所在的文件夹，简写为 `pwd` |
| `Get-ChildItem` | 显示指定文件夹中的文件和子文件夹，简写为 `ls` |
| `Set-Location 路径` | 切换当前目录，简写为 `cd` |
| `Get-PSDrive -PSProvider FileSystem` | 查看电脑中的文件系统磁盘 |
| `Test-Path 路径` | 检查指定文件或文件夹是否存在 |
| `Get-Content 文件路径 -Encoding UTF8` | 按 UTF-8 编码读取文件内容 |
| `git switch -c 分支名` | 创建新分支并立即切换到该分支 |
| `git status` | 查看当前分支以及文件的修改、暂存和提交状态 |

## 5. Git 完整工作流程

```text
修改并保存文件 → git add → git commit → git push
→ Pull Request → Merge → git switch main → git pull
```

1. **修改并保存文件：** 在 VS Code 中编辑本地文件，按 `Ctrl+S` 保存到电脑。
2. **git add：** 选择要放入本次提交的文件并加入暂存区。
3. **git commit：** 在本地 Git 仓库中创建一次版本快照，不会自动上传。
4. **git push：** 把本地提交上传到 GitHub 上的对应分支。
5. **Pull Request：** 提出把学习分支修改合并到 `main` 的申请。
6. **Merge：** 真正把学习分支的修改加入 GitHub 的 `main`。
7. **git switch main：** 把电脑上的工作分支切换回 `main`。
8. **git pull：** 把 GitHub 上更新后的 `main` 下载并同步到本地项目文件夹。

## 6. FDE 场景练习

### 问题

客户说：“项目文件已经放在电脑里，但运行程序时提示找不到文件。”

### 我的前三步检查方法

1. **先询问并确认目标信息。** 向客户确认文件的完整名称、扩展名、来源、最后一次使用位置，以及报错中显示的路径。如果这些信息都不知道，就无法进行准确搜索。
2. **确认环境并缩小搜索范围。** 使用 `Get-Location` 确认终端当前所在位置，再用 `Get-PSDrive -PSProvider FileSystem` 查看磁盘。根据客户提供的信息，从下载目录、桌面、项目目录或最可能的磁盘开始搜索，而不是一开始扫描整个 `C:\`。
3. **搜索、验证并对照程序使用的路径。** 使用 `Get-ChildItem` 递归查找文件，取得完整路径后用 `Test-Path` 验证；最后检查程序配置中的文件名、扩展名和路径是否与实际位置完全一致。

例如，客户说目标文件叫 `data.csv`，可能在 `F:\FDE` 中：

```powershell
Get-Location
Get-PSDrive -PSProvider FileSystem
Get-ChildItem -Path F:\FDE -Recurse -File -Filter "data.csv" -ErrorAction SilentlyContinue |
    Select-Object FullName
Test-Path "F:\FDE\实际找到的文件夹\data.csv"
```

各命令的作用：

- `Get-Location`：确认终端现在站在哪里，但不代表目标文件也在那里。
- `Get-PSDrive`：查看有哪些磁盘可以搜索。
- `Get-ChildItem -Recurse`：搜索指定文件夹及其所有下级文件夹。
- `-Filter "data.csv"`：只查找指定文件；如果只知道部分名称，可以使用 `"*data*"`。
- `Select-Object FullName`：显示搜索结果的完整路径。
- `Test-Path`：确认找到的完整路径确实存在。

找到文件后仍需检查：

- 程序使用的是相对路径还是绝对路径；
- 程序运行时的当前目录是否正确；
- 文件名、扩展名和大小写是否写对；
- 配置文件中的路径是否仍指向旧位置；
- 当前用户是否有读取文件的权限。

正确的排查逻辑是：

```text
询问目标信息 → 确认当前环境 → 缩小搜索范围
→ 搜索并获得完整路径 → Test-Path 验证
→ 对照程序实际使用的路径
```

## 7. 今日总结

今天我真正理解了：VS Code 负责查看和编辑本地文件，Git 负责版本管理和同步，GitHub 保存远程仓库，PowerShell 只是执行 Git 和其他命令的一种方式。

我还理解了：`Get-Location` 只能确认终端当前位置。客户不知道文件在哪里时，应先询问信息并缩小范围，再搜索目标文件，不能把当前目录误认为文件位置。
