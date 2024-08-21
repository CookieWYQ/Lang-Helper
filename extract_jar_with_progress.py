__all__ = ['extract_jar_with_progress', 'extract_jar_with_progress_window', 'compress_folder_to_jar_with_progress_window',
           'compress_folder_to_jar_with_progress']


def extract_jar_with_progress(file_path: str, output_path: str, callback_progress: callable = None):
    import zipfile
    import os
    if not os.path.isfile(file_path):
        raise ValueError("Invalid file path")
    if not zipfile.is_zipfile(file_path):
        raise ValueError("Invalid JAR file")
    if callback_progress is None:
        raise ValueError("Callback function is required")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        # 获取文件列表
        files = zip_ref.namelist()
        total_files = len(files)

        for _ in range(len(files)):
            zip_ref.extract(files[_], output_path)
            callback_progress(i=_, all_=total_files)


def extract_jar_with_progress_window(file_path: str, output_path: str):
    import tkinter as tk
    from tkinter import ttk
    from math import floor
    import zipfile
    import os

    if not os.path.isfile(file_path):
        raise ValueError("Invalid file path")
    if not zipfile.is_zipfile(file_path):
        raise ValueError("Invalid JAR file")
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    show_progress_window_ = tk.Tk()
    show_progress_window_.title("进度")
    show_progress_window_.geometry("300x100")
    show_progress_window_.resizable(False, False)
    show_progress_window_.protocol("WM_DELETE_WINDOW", lambda: None)

    bar = ttk.Progressbar(show_progress_window_, orient=tk.HORIZONTAL, length=250, mode='determinate')
    bar.place(x=10, y=10)

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        # 获取文件列表
        files = zip_ref.namelist()
        total_files = len(files)

        for _ in range(len(files)):
            zip_ref.extract(files[_], output_path)
            bar['value'] = floor(_ / total_files * 10000) / 100
            show_progress_window_.update()
    show_progress_window_.destroy()


def compress_folder_to_jar_with_progress(folder_path: str, output_path: str, callback_progress: callable = None):
    import zipfile
    import os
    import os.path
    if not os.path.isdir(folder_path):
        raise ValueError("Invalid folder path")

    if os.path.exists(output_path):
        raise ValueError("Output file already exists")

    if callback_progress is None:
        raise ValueError("Callback function is required")

    # 获取文件夹内所有文件和目录
    def get_files_in_folder(folder):
        for root, dirs, files_ in os.walk(folder):
            for file in files_:
                yield os.path.join(root, file)

    # 创建 ZIP 文件
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        files = list(get_files_in_folder(folder_path))
        total_files = len(files)

        for i, file_path in enumerate(files):
            arcname = os.path.relpath(file_path, folder_path)
            zip_ref.write(file_path, arcname)

        callback_progress(i=total_files, all_=total_files)


def compress_folder_to_jar_with_progress_window(folder_path: str, output_path: str):
    import tkinter as tk
    from tkinter import ttk
    from math import floor
    import zipfile
    import os
    import os.path
    if not os.path.isdir(folder_path):
        raise ValueError("Invalid folder path")

    if os.path.exists(output_path):
        raise ValueError("Output file already exists")

    show_progress_window = tk.Tk()
    show_progress_window.title("进度")
    show_progress_window.geometry("300x100")
    show_progress_window.resizable(False, False)
    show_progress_window.protocol("WM_DELETE_WINDOW", lambda: None)

    bar = ttk.Progressbar(show_progress_window, orient=tk.HORIZONTAL, length=250, mode='determinate')
    bar.place(x=10, y=10)

    # 获取文件夹内所有文件和目录
    def get_files_in_folder(folder):
        for root, dirs, files_ in os.walk(folder):
            for file in files_:
                yield os.path.join(root, file)

    # 创建 ZIP 文件
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        files = list(get_files_in_folder(folder_path))
        total_files = len(files)

        for i, file_path in enumerate(files):
            arcname = os.path.relpath(file_path, folder_path)
            zip_ref.write(file_path, arcname)
            bar['value'] = floor(i / total_files * 10000) / 100
            show_progress_window.update()

    show_progress_window.destroy()


if __name__ == '__main__':
    # 指定要解压的jar文件路径
    jar_file = '[林业] forestry-1.16.5-6.0.14.jar'
    # 指定输出目录
    output_dir = 'a'


    def show_progress(i, all_):
        print(f'正在解压文件：{i}/{all_} {i * 100 / all_:.2f}%', end='\r')


    # 调用函数
    extract_jar_with_progress(jar_file, output_dir, show_progress)
