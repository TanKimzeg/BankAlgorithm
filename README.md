# 银行家算法的Python实现

这是一个使用Python实现的银行家算法项目，用于模拟资源分配和安全性检查。银行家算法是一种用于避免死锁的资源分配算法。

## 项目结构

- `BankAlgorithm.py`: 包含银行家算法的主要实现代码。
- `README.md`: 项目说明文件。

## 功能

1. **添加进程**: 支持添加多个进程，每个进程有最大资源需求和已分配资源。
2. **请求资源**: 进程可以请求资源，系统会检查是否处于安全状态。
3. **释放资源**: 进程可以释放已分配的资源。
4. **安全性检查**: 系统会检查当前状态是否安全，并提供安全序列（如果存在）。

## 使用方法

### 示例代码

以下是一个使用银行家算法的示例：

```python
from BankAlgorithm import BankAlgorithm, Process

# 初始化银行家算法
bank = BankAlgorithm(3, [9, 3, 6])

# 添加进程
p1 = Process("P1", 3, [3, 2, 2], [1, 0, 0])
p2 = Process("P2", 3, [6, 1, 3], [5, 1, 1])
p3 = Process("P3", 3, [3, 1, 4], [2, 1, 1])
p4 = Process("P4", 3, [4, 2, 2], [0, 0, 2])

bank.add_process(p1)
bank.add_process(p2)
bank.add_process(p3)
bank.add_process(p4)

# 显示所有进程
bank.display_processes()

# 请求资源
if bank.request_resources("P2", [1, 0, 1]):
    print("Request for P2 granted.")
else:
    print("Request for P2 denied.")

# 检查系统安全状态
is_safe, safe_sequence = bank.check_safe_state()
if is_safe:
    print("System is in a safe state.")
    print(f"Safe sequence:\n{\n.join(str(p[1]) for p in list(safe_sequence))}")
else:
    print("System is not in a safe state.")
```

### 运行项目

1. 确保安装了Python 3.10或更高版本。
2. 在终端中运行以下命令：
   ```bash
   python BankAlgorithm.py
   ```

## 注意事项

- 所有资源数量必须为非负数。
- 请求的资源不能超过进程的需求或系统的可用资源。
- 如果系统处于不安全状态，请求将被拒绝。
