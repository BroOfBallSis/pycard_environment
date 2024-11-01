# 内存占用的调试
import psutil


def print_memory_info():
    # 获取当前进程
    process = psutil.Process()

    # 获取内存信息
    memory_info = process.memory_info()

    # 打印内存占用情况
    print("内存占用:")
    print(f"RSS: {memory_info.rss / 1024 / 1024:.2f} MB")  # 常驻集大小
    print(f"VMS: {memory_info.vms / 1024 / 1024:.2f} MB")  # 虚拟内存大小
    print(f"Shared: {memory_info.shared / 1024 / 1024:.2f} MB")  # 共享内存大小
    print(f"Text: {memory_info.text / 1024 / 1024:.2f} MB")  # 可执行代码大小
    print(f"Lib: {memory_info.lib / 1024 / 1024:.2f} MB")  # 库大小
    print(f"Data: {memory_info.data / 1024 / 1024:.2f} MB")  # 数据段大小
    print(f"Dirty: {memory_info.dirty / 1024 / 1024:.2f} MB")  # 脏页大小
