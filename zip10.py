import os  
import zipfile  
import threading  
from queue import Queue  
from tqdm import tqdm  
import shutil  
import time  
  
# 定义线程数量和文件队列  
NUM_THREADS = 4  
file_queue = Queue()  
lock = threading.Lock()  
  
# 用于存储已完成压缩的文件名  
completed_files = []  
  
def zip_file_with_progress(file_path, filename):  
    zip_filename = f"{os.path.splitext(filename)[0]}.zip"  
    zip_path = os.path.join(os.path.dirname(file_path), zip_filename)  
      
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:  
        with open(file_path, 'rb') as f:  
            # 假设我们不需要进度条，为简洁起见这里省略  
            for data in iter(lambda: f.read(1024 * 1024), b''):  
                zipf.writestr(filename, data)  
      
    # 标记文件已完成压缩  
    with lock:  
        completed_files.append(filename)  
        print(f"文件 {filename} 压缩完成，已保存为 {zip_filename}")  
  
def worker():  
    while True:  
        file_path = file_queue.get()  
        if file_path is None:  
            file_queue.task_done()  
            break  
        filename = os.path.basename(file_path)  
        zip_file_with_progress(file_path, filename)  
        file_queue.task_done()  
  
def print_completed_files():  
    while True:  
        time.sleep(1)  # 每秒检查一次  
        with lock:  
            if completed_files and not file_queue.empty():  
                continue  # 队列中还有文件，继续等待  
            if completed_files:  
                print("\n压缩完成列表:")  
                for filename in completed_files:  
                    print(f"文件 {filename} 压缩完成")  
                print()  
            if file_queue.empty() and not any(t.is_alive() for t in threading.enumerate() if t != threading.current_thread()):  
                # 所有文件都已处理且所有线程都已结束  
                break  
  
def main(directory):  
    total, used, free = shutil.disk_usage(directory)  
    print(f"开始压缩文件在 {directory} 目录，剩余空间: {free / (1024.0 ** 3):.2f} GB")  
      
    for filename in os.listdir(directory):  
        file_path = os.path.join(directory, filename)  
        if os.path.isfile(file_path) and not filename.endswith('.zip'):  
            file_queue.put(file_path)  
      
    threads = []  
    for _ in range(NUM_THREADS):  
        t = threading.Thread(target=worker)  
        t.start()  
        threads.append(t)  
      
    # 启动一个单独的线程来打印完成文件列表  
    print_completed_files_thread = threading.Thread(target=print_completed_files)  
    print_completed_files_thread.start()  
      
    # 等待队列中的所有任务都被处理完毕以及所有工作线程结束  
    file_queue.join()  
    for t in threads:  
        t.join()  
      
    # 停止打印完成文件列表的线程  
    for _ in range(NUM_THREADS):  
        file_queue.put(None)  
    print_completed_files_thread.join()  
      
    print("\n所有文件压缩完成\n")  
    total, used, free = shutil.disk_usage(directory)  
    print(f"压缩后剩余空间: {free / (1024.0 ** 3):.2f} GB")  
  
# 使用main函数  
if __name__ == "__main__":  
    directory_to_compress = "/storage/emulated/0/指令/1/"  # 替换为你要压缩的目录路径  
    main(directory_to_compress)