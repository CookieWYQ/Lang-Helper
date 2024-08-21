import json
import os
import sys
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
from tkinter import simpledialog
import functools
import threading

from transfromAPIWithSogou import translate_with_check
from LangOperation import *
from JsonLangOperation import *
from tool import *

try:
    from PyDeepLX import PyDeepLX
except ImportError:
    os.system(f'pip3 install PyDeepLX')
    from PyDeepLX import PyDeepLX

try:
    import pyperclip
except ImportError:
    os.system(f'pip3 install pyperclip')
    import pyperclip

try:
    import langdetect
except ImportError:
    os.system(f'pip3 install langdetect')
    import langdetect

win = tk.Tk()
win.title("LangOperation GUI By CallMeACookieWYQ")
win.geometry("500x500")
if os.path.exists('tb.ico'):
    win.iconbitmap('tb.ico')

config: dict[str, str | bool | dict[str, str] | int] = {}

SOUGO = "sogou"
DEEPL = "deepl"
GOOGLE = "google"
BAIDU = "baidu"
TENCENT = "tencent"

stop_event: threading.Event = threading.Event()
show_progress_window: tk.Toplevel

main_lang_path: str = "fy_ok/zh_cn.lang"
contrast_lang_path: str = "fy_ok/en_us.lang"
main_lang: LangOperation | JsonLangOperation
contrast_lang: LangOperation | JsonLangOperation

file_path: str = "./file/"
file_type: str = "*.jar"
keys_list: list[str] = []

USE_NUM_KEY: bool = False
color_num_key: dict[str, str] = {"1": "white",
                                 "2": "red",
                                 "3": "green",
                                 "4": "blue",
                                 "5": "yellow",
                                 "6": "purple",
                                 "7": "orange",
                                 "8": "pink",
                                 "9": "gray",
                                 "0": "light green"
                                 }

copy_key: str = 'c'
USE_COPY_TIP: bool = True

top_find_key: str = 'r'

all_find_mark_key: str = 'q'
all_find_mark_color: str = 'light yellow'

USE_BUTTON_KEY: bool = True
button_key: dict[str, str] = {"5": "white",
                              "4": "red"}

USE_MOUSE_WHEEL: bool = True

USE_KEY_TO_TURN_and_DOWN: bool = True
KEY_TO_TURN_and_DOWN: dict[str, str] = {"KEY_TO_DOWN": "s", "KEY_TO_UP": "w"}

reload_key: str = 'l'
USE_RELOAD_TIP: bool = True

save_key: str = 's'
USE_SAVE_TIP: bool = True

labels: dict[str, tk.Label] = {}
page: int = 0
input_vars: dict[str, tk.StringVar] = {}
inputs: dict[str, tk.Entry] = {}
lens_key: list[int] = []
states: dict[str, str] = {}

ALLOW_RELOAD_LANG: bool = True

show_order: list[str] = []

show_num: int = 0

interval: int = 40

USE_SAVE_TIP_WHEN_SETTING_CLOSE: bool = True
USE_SAVE_TIP_WHEN_MAIN_CLOSE: bool = True

translate_api: str = SOUGO


def deepl_translate_with_check(text: str, sourceLang: str = "auto", targetLang: str = "zh"):
    try:
        return PyDeepLX.translate(text, sourceLang, targetLang)
    except PyDeepLX.TooManyRequestsException:
        messagebox.showerror("翻译失败",
                             "翻译失败，请稍后再试！\n(你在短时间内发送了大量的翻译请求，导致你的翻译请求被限制了(IP被暂时封禁)")


def init():
    global config, \
        file_path, keys_list, USE_NUM_KEY, color_num_key, \
        copy_key, USE_COPY_TIP, top_find_key, all_find_mark_key, \
        all_find_mark_color, USE_BUTTON_KEY, button_key, USE_MOUSE_WHEEL, \
        USE_KEY_TO_TURN_and_DOWN, KEY_TO_TURN_and_DOWN, reload_key, \
        USE_RELOAD_TIP, file_path, file_type, keys_list, save_key, USE_SAVE_TIP, main_lang_path, \
        contrast_lang_path, main_lang, contrast_lang, input_vars, inputs, lens_key, states, show_order, \
        interval, show_order, show_num, USE_SAVE_TIP_WHEN_SETTING_CLOSE, USE_SAVE_TIP_WHEN_MAIN_CLOSE, translate_api

    if not os.path.exists('config/config.json'):
        messagebox.showerror("文件路径", "配置文件不存在！")
        sys.exit()

    with open('config/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    if not os.path.exists(config["main_lang_path"]):
        messagebox.showerror("文件路径", "主语言文件不存在！")
        sys.exit()

    if not os.path.exists(config["contrast_lang_path"]):
        messagebox.showerror("文件路径", "对比语言文件不存在！")
        sys.exit()

    main_lang_path = config["main_lang_path"]
    contrast_lang_path = config["contrast_lang_path"]

    if json_or_lang_path(main_lang_path) and json_or_lang_path(contrast_lang_path):
        main_lang = JsonLangOperation(main_lang_path)
        contrast_lang = JsonLangOperation(contrast_lang_path)
    elif not (json_or_lang_path(main_lang_path) or json_or_lang_path(contrast_lang_path)):
        main_lang = LangOperation(main_lang_path)
        contrast_lang = LangOperation(contrast_lang_path)
    else:
        messagebox.showerror("文件路径", "主语言文件或对比语言文件格式错误！")
        sys.exit()

    keys_list = list(main_lang.read_lang().keys())
    lens_key = [len(k) for k in main_lang.read_lang().keys()]

    if ALLOW_RELOAD_LANG:
        main_lang_path = config["main_lang_path"]
        contrast_lang_path = config["contrast_lang_path"]
        if json_or_lang_path(main_lang_path) and json_or_lang_path(contrast_lang_path):
            main_lang = JsonLangOperation(main_lang_path)
            contrast_lang = JsonLangOperation(contrast_lang_path)
        elif not json_or_lang_path(main_lang_path) and not json_or_lang_path(contrast_lang_path):
            main_lang = LangOperation(main_lang_path)
            contrast_lang = LangOperation(contrast_lang_path)
        else:
            messagebox.showerror("文件路径", "主语言文件或对比语言文件格式错误！")
            sys.exit()

    USE_NUM_KEY = config["USE_NUM_KEY"]
    color_num_key = config["color_num_key"]

    USE_COPY_TIP = config["USE_COPY_TIP"]

    USE_BUTTON_KEY = config["USE_BUTTON_KEY"]
    button_key = config["button_key"]

    USE_MOUSE_WHEEL = config["USE_MOUSE_WHEEL"]

    KEY_TO_TURN_and_DOWN = config["KEY_TO_TURN_and_DOWN"]

    copy_key = config["copy_key"]

    all_find_mark_key = config["all_find_mark_key"]
    all_find_mark_color = config["all_find_mark_color"]

    USE_RELOAD_TIP = config["USE_RELOAD_TIP"]
    reload_key = config["reload_key"]

    save_key = config["save_key"]
    USE_SAVE_TIP = config["USE_SAVE_TIP"]

    interval = config["interval"]

    show_num = win.winfo_height() // interval

    USE_SAVE_TIP_WHEN_SETTING_CLOSE = config["USE_SAVE_TIP_WHEN_SETTING_CLOSE"]
    USE_SAVE_TIP_WHEN_MAIN_CLOSE = config["USE_SAVE_TIP_WHEN_MAIN_CLOSE"]

    translate_api = config["translate_api"]

    for _ in labels:
        labels[_].destroy()
        inputs[_].destroy()
        input_vars[_].set('')

    labels.clear()
    inputs.clear()
    input_vars.clear()
    show_order.clear()

    for k_, v_ in main_lang.read_lang().items():
        t_v = tk.StringVar()
        t_v.set(v_)
        t_l = ttk.Label(win, text=k_)
        t_i = ttk.Entry(win, textvariable=t_v, width=50)
        input_vars[k_] = t_v
        inputs[k_] = t_i
        labels[k_] = t_l
        show_order.append(k_)

    for t in range(len(labels.values())):
        labels[list(labels.keys())[t]].place(x=5, y=t * interval)

    for t in range(len(inputs.values())):
        inputs[list(inputs.keys())[t]].place(x=lens_key[t] * 9 + 10, y=t * interval)


init()


def release_focus():
    # 强制根窗口获得焦点，这将导致所有子组件失去焦点
    win.focus_force()


def save():
    if USE_SAVE_TIP:
        messagebox.showinfo("保存", "成功保存！")
    main_lang.save_lang()


def change_label_and_input():
    for _ in range(len(keys_list)):
        if _ < page:
            labels[keys_list[_]].place_forget()
            inputs[keys_list[_]].place_forget()
        else:
            labels[keys_list[_]].place(x=5, y=(_ - page) * interval)
            inputs[keys_list[_]].place(x=lens_key[_] * 9 + 10, y=(_ - page) * interval)


def on_press(event=None):
    global page
    if USE_NUM_KEY:
        if event.keysym == "1":
            states[keys_list[page]] = color_num_key["1"]
        elif event.keysym == "2":
            states[keys_list[page]] = color_num_key["2"]
        elif event.keysym == "3":
            states[keys_list[page]] = color_num_key["3"]
        elif event.keysym == "4":
            states[keys_list[page]] = color_num_key["4"]
        elif event.keysym == "5":
            states[keys_list[page]] = color_num_key["5"]
        elif event.keysym == "6":
            states[keys_list[page]] = color_num_key["6"]
        elif event.keysym == "7":
            states[keys_list[page]] = color_num_key["7"]
        elif event.keysym == "8":
            states[keys_list[page]] = color_num_key["8"]
        elif event.keysym == "9":
            states[keys_list[page]] = color_num_key["9"]
        elif event.keysym == "0":
            states[keys_list[page]] = color_num_key["0"]

    if event.keysym == copy_key:
        try:
            pyperclip.copy(os.path.basename(keys_list[page].replace('\\', '/')))
        except RuntimeError:
            messagebox.showerror("复制", "复制失败！")
        else:
            if USE_COPY_TIP:
                messagebox.showinfo("复制", "成功复制！")
    elif event.keysym == top_find_key:
        text = simpledialog.askstring("to", "Input text you want to find...")
        for _ in range(len(keys_list)):
            if text in keys_list[_]:
                page = _
                change_label_and_input()
                break
    elif event.keysym == all_find_mark_key:
        text = simpledialog.askstring("change", "Input text you want to find...")
        for _ in range(len(keys_list)):
            if text in keys_list[_]:
                states[keys_list[_]] = all_find_mark_color

    if USE_KEY_TO_TURN_and_DOWN:

        if event.keysym == KEY_TO_TURN_and_DOWN["KEY_TO_UP"]:
            if page > -1:
                page -= 1
            if page <= -1:
                page = len(keys_list) - 1
        elif event.keysym == KEY_TO_TURN_and_DOWN["KEY_TO_DOWN"]:
            if page < len(keys_list):
                page += 1
            if page >= len(keys_list):
                page = 0
        # print(page)
        change_label_and_input()

    if event.keysym == reload_key:
        init()
        if USE_RELOAD_TIP:
            messagebox.showinfo("重载", "成功重载！")

    if event.keysym == save_key:
        save()


win.bind('<KeyPress>', on_press)


def on_button(event=None):
    if event.num == 5:
        states[keys_list[page]] = button_key["5"]
    elif event.num == 4:
        states[keys_list[page]] = button_key["4"]


win.bind('<Button>', on_button)


def on_wheel(event=None):
    global page
    if USE_MOUSE_WHEEL:
        if event.delta > 0:
            if page > -1:
                page -= 1
            if page <= -1:
                page = len(keys_list) - 1
        else:
            if page < len(keys_list):
                page += 1
            if page >= len(keys_list):
                page = 0
        change_label_and_input()


win.bind('<MouseWheel>', on_wheel)


def show_menu(event):
    # 显示右键菜单
    right_click_menu.post(event.x_root, event.y_root)


def add_item():
    global ALLOW_RELOAD_LANG

    key__ = simpledialog.askstring("键", "请输入您要添加的键：")
    if key__ in keys_list:
        messagebox.showerror("键", "键已存在！")
        return
    if key__ is None:
        messagebox.showerror("键", "输入为空！")
        return

    value__ = simpledialog.askstring("值", "请输入您要添加的值：")
    if value__ is None:
        messagebox.showerror("值", "输入为空！")
        return

    main_lang.change_lang(key__, value__)
    main_lang.save_lang()
    ALLOW_RELOAD_LANG = False
    init()
    ALLOW_RELOAD_LANG = True
    messagebox.showinfo("添加", "成功添加！")


def complete_missing_parts():
    global ALLOW_RELOAD_LANG
    main_lang.complete_lang_by_obj(contrast_lang)
    main_lang.save_lang()
    ALLOW_RELOAD_LANG = False
    init()
    ALLOW_RELOAD_LANG = True
    messagebox.showinfo("补全", "成功补全！")


def remove_item():
    global ALLOW_RELOAD_LANG

    key__ = simpledialog.askstring("键", "请输入您要删除的键：")
    if key__ not in keys_list:
        messagebox.showerror("键", "没有找到该键！")
        return
    if key__ is None:
        messagebox.showerror("键", "输入为空！")
        return

    main_lang.remove_lang(key__)
    main_lang.save_lang()
    ALLOW_RELOAD_LANG = False
    init()
    ALLOW_RELOAD_LANG = True
    messagebox.showinfo("删除", "成功删除！")


def quit_win():
    if USE_SAVE_TIP_WHEN_MAIN_CLOSE:
        if messagebox.askyesno("保存", "是否保存？"):
            save()
    stop_event.set()
    win.destroy()


def reload_from_hard_drive():
    init()
    if USE_RELOAD_TIP:
        messagebox.showinfo("重载", "成功重载！")


def reload():
    global ALLOW_RELOAD_LANG
    ALLOW_RELOAD_LANG = False
    init()
    ALLOW_RELOAD_LANG = True
    if USE_RELOAD_TIP:
        messagebox.showinfo("重载", "成功重载！")


def ask_lang_path() -> str:
    return filedialog.askopenfilename(title="选择语言文件", filetypes=[("语言文件", "*.lang"), ("语言文件", "*.json"), ("所有文件", "*.*")])


def show_setting_window():
    global main_lang, contrast_lang, config

    def save_to_hard_drive():
        global config
        global main_lang, contrast_lang
        config["main_lang_path"] = main_lang_path_entry.get()
        config["contrast_lang_path"] = contrast_lang_path_entry.get()
        config["USE_NUM_KEY"] = if_USE_NUM_KEY_ckbtn_var.get()

        with open("config/config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("保存", "成功保存！更新这些配置需要重载或重启软件！")

    def ask_save_to_hard_drive():
        if USE_SAVE_TIP_WHEN_SETTING_CLOSE:
            if messagebox.askyesno("保存", "是否保存配置至硬盘？"):
                save_to_hard_drive()
        setting_window.destroy()

    setting_window = tk.Toplevel(win)
    setting_window.title("设置")
    setting_window.geometry("500x780")
    setting_window.resizable(False, False)
    setting_window.protocol("WM_DELETE_WINDOW", ask_save_to_hard_drive)

    def ask_main_lang_path():
        global main_lang_path
        fp = ask_lang_path()
        if fp:
            main_lang_path = fp
            main_lang_path_entry.delete(0, tk.END)
            main_lang_path_entry.insert(0, fp)
            messagebox.showinfo("路径", "成功选择路径！")
        else:
            messagebox.showerror("路径", "路径为空！")
            return

    main_lang_path_label = tk.Label(setting_window, text="主语言文件路径")
    main_lang_path_label.place(x=10, y=10)
    main_lang_path_entry = tk.Entry(setting_window, width=30, font=("Arial", 10), bd=1, relief="solid", bg="white",
                                    fg="black", insertbackground="black", selectbackground="lightblue",
                                    selectforeground="black", exportselection=True, selectborderwidth=1,
                                    highlightthickness=1, takefocus=True, disabledforeground="gray",
                                    disabledbackground="white",
                                    highlightcolor="white", highlightbackground="white")
    main_lang_path_entry.place(x=10, y=30)
    main_lang_path_entry.insert(0, main_lang.lang_path)
    main_lang_path_button = tk.Button(setting_window, text="选择", command=ask_main_lang_path, font=("Arial", 10),
                                      width=5, height=1, bg="lightgray", fg="black", relief="raised", bd=1,
                                      activebackground="lightblue", activeforeground="black", cursor="hand2",
                                      overrelief="raised", state="normal", highlightcolor="white",
                                      highlightbackground="white", highlightthickness=1)
    main_lang_path_button.place(x=240, y=30)

    def ask_contrast_lang_path():
        global contrast_lang
        fp = ask_lang_path()
        if fp:
            contrast_lang = fp
            contrast_lang_path_entry.delete(0, tk.END)
            contrast_lang_path_entry.insert(0, fp)
            messagebox.showinfo("路径", "成功选择路径！")
        else:
            messagebox.showerror("路径", "路径为空！")
            return

    contrast_lang_path_label = tk.Label(setting_window, text="对比语言文件路径")
    contrast_lang_path_label.place(x=10, y=60)
    contrast_lang_path_entry = tk.Entry(setting_window, width=30, font=("Arial", 10), bd=1, relief="solid", bg="white",
                                        fg="black", insertbackground="black", selectbackground="lightblue",
                                        selectforeground="black", exportselection=True, selectborderwidth=1,
                                        highlightthickness=1, takefocus=True, disabledforeground="gray",
                                        disabledbackground="white",
                                        highlightcolor="white", highlightbackground="white")
    contrast_lang_path_entry.place(x=10, y=80)
    contrast_lang_path_entry.insert(0, contrast_lang.lang_path)
    contrast_lang_path_button = tk.Button(setting_window, text="选择", command=ask_contrast_lang_path,
                                          font=("Arial", 10),
                                          width=5, height=1, bg="lightgray", fg="black", relief="raised", bd=1,
                                          activebackground="lightblue", activeforeground="black", cursor="hand2",
                                          overrelief="raised", state="normal", highlightcolor="white",
                                          highlightbackground="white", highlightthickness=1)
    contrast_lang_path_button.place(x=240, y=80)

    """
    添加对数字键颜色的设置
    """

    def show_num_key_color_setting_window():
        num_key_color_setting_window = tk.Toplevel(setting_window)
        num_key_color_setting_window.title("数字键颜色设置")
        num_key_color_setting_window.geometry("400x400")
        num_key_color_setting_window.resizable(False, False)

        def change_color(num: int):
            color = colorchooser.askcolor(title="选择颜色")[1]
            if color is not None:
                config["color_num_key"][str(num)] = str(color)
                key_color_labels[num].config(text=f"{num}键颜色: {config['color_num_key'][str(num)]}",
                                             bg=config["color_num_key"][str(num)])
                key_color_labels[num].config(bg=config["color_num_key"][str(num)])
            else:
                messagebox.showerror("颜色", "颜色为空！")
                return

        key_color_labels: dict[int, tk.Label] = {}
        key_color_setting_buttons: dict[int, tk.Button] = {}

        for i in range(10):
            key_color_label = tk.Label(num_key_color_setting_window,
                                       text=f"{i}键颜色: {config['color_num_key'][str(i)]}",
                                       bg=config["color_num_key"][str(i)])
            key_color_label.place(x=10, y=10 + i * 30)
            key_color_button = tk.Button(num_key_color_setting_window, text="选择",
                                         bg=config["color_num_key"][str(i)],
                                         font=("Arial", 10), command=functools.partial(change_color, i),
                                         width=5, height=1, fg="black", relief="raised", bd=1,
                                         activebackground="lightblue", activeforeground="black", cursor="hand2",
                                         overrelief="raised", state="normal", highlightcolor="white",
                                         )
            key_color_button.place(x=240, y=10 + i * 30)
            key_color_labels[i] = key_color_label
            key_color_setting_buttons[i] = key_color_button

    show_num_key_color_setting_button = tk.Button(setting_window, text="数字键颜色设置",
                                                  command=show_num_key_color_setting_window,
                                                  font=("Arial", 10),
                                                  width=14, height=1, bg="lightgray", fg="black", relief="raised", bd=1,
                                                  activebackground="lightblue", activeforeground="black",
                                                  cursor="hand2",
                                                  overrelief="raised", highlightcolor="white",
                                                  highlightbackground="white", highlightthickness=1,
                                                  state="normal" if config["USE_NUM_KEY"] else "disabled",
                                                  )

    show_num_key_color_setting_button.place(x=130, y=110)

    if_USE_NUM_KEY_ckbtn_var = tk.BooleanVar()

    def if_USE_NUM_KEY__check():
        """
        更改是否能修改数字键对应的颜色
        """
        global config
        config["USE_COPY_TIP"] = if_USE_COPY_TIP_ckbtn_var.get()
        if if_USE_NUM_KEY_ckbtn_var.get():
            show_num_key_color_setting_button.config(state="normal")
        else:
            show_num_key_color_setting_button.config(state="disabled")

    if_USE_NUM_KEY_ckbtn = ttk.Checkbutton(setting_window, text="是否使用数字键", variable=if_USE_NUM_KEY_ckbtn_var,
                                           command=if_USE_NUM_KEY__check, style="Switch.TCheckbutton", onvalue=1,
                                           offvalue=0)
    if_USE_NUM_KEY_ckbtn.place(x=10, y=110)

    def ask_copy_key():
        k = simpledialog.askstring("复制热键", "请输入复制热键", parent=win)
        if k is not None and 0 < len(k) < 2:
            config["copy_key"] = k
            copy_key_show_label.config(text=f"当前复制热键：{k}")
        else:
            messagebox.showerror("错误", "热键错误！请输入一个字符！")

    copy_key_setting_button = tk.Button(setting_window, text="设置复制热键", command=ask_copy_key,
                                        font=("Arial", 10),
                                        width=10, height=1, bg="lightgray", fg="black", relief="raised", bd=1,
                                        activebackground="lightblue", activeforeground="black", cursor="hand2",
                                        overrelief="raised", state="normal", highlightcolor="white",
                                        highlightbackground="white", highlightthickness=1
                                        )

    copy_key_setting_button.place(x=10, y=170)

    copy_key_show_label = tk.Label(setting_window, text=f"当前复制热键：{config["copy_key"]}")
    copy_key_show_label.place(x=10, y=140)

    def if_USE_COPY_TIP__check():
        global config
        config["USE_COPY_TIP"] = if_USE_COPY_TIP_ckbtn_var.get()

    if_USE_COPY_TIP_ckbtn_var = tk.BooleanVar()
    if_USE_COPY_TIP_ckbtn_var.set(bool(config["USE_COPY_TIP"]))
    if_USE_COPY_TIP_ckbtn = ttk.Checkbutton(setting_window, text="是否使用复制提示", variable=if_USE_COPY_TIP_ckbtn_var,
                                            command=if_USE_COPY_TIP__check, style="Switch.TCheckbutton", onvalue=1,
                                            offvalue=0)
    if_USE_COPY_TIP_ckbtn.place(x=10, y=210)

    top_find_key_show_label = tk.Label(setting_window, text=f"当前置顶搜索热键：{config["top_find_key"]}")
    top_find_key_show_label.place(x=10, y=240)

    def ask_top_find_key():
        k = simpledialog.askstring("置顶搜索热键", "请输入置顶搜索热键", parent=win)
        if k is not None and 0 < len(k) < 2:
            config["top_find_key"] = k
            top_find_key_show_label.config(text=f"当前置顶搜索热键：{k}")
        else:
            messagebox.showerror("错误", "热键错误！请输入一个字符！")

    top_find_key_setting_button = tk.Button(setting_window, text="设置置顶搜索热键", command=ask_top_find_key,
                                            font=("Arial", 10),
                                            width=14, height=1, bg="lightgray", fg="black", relief="raised", bd=1,
                                            activebackground="lightblue", activeforeground="black", cursor="hand2",
                                            overrelief="raised", state="normal", highlightcolor="white",
                                            highlightbackground="white", highlightthickness=1
                                            )

    top_find_key_setting_button.place(x=10, y=270)

    all_find_mark_key_show_label = tk.Label(setting_window, text=f"当前全选搜索热键：{config["all_find_mark_key"]}")
    all_find_mark_key_show_label.place(x=10, y=300)

    def ask_all_find_mark_key():
        k = simpledialog.askstring("全局搜索匹配热键", "请输入全局搜索匹配热键", parent=win)
        if k is not None and 0 < len(k) < 2:
            config["all_find_mark_key"] = k
            all_find_mark_key_show_label.config(text=f"当前全局搜索匹配热键：{k}")
        else:
            messagebox.showerror("错误", "热键错误！请输入一个字符！")

    all_find_mark_key_setting_button = tk.Button(setting_window, text="设置全局搜索匹配热键",
                                                 command=ask_all_find_mark_key,
                                                 font=("Arial", 10),
                                                 width=16, height=1, bg="lightgray", fg="black", relief="raised", bd=1,
                                                 activebackground="lightblue", activeforeground="black", cursor="hand2",
                                                 overrelief="raised", state="normal", highlightcolor="white",
                                                 )

    all_find_mark_key_setting_button.place(x=10, y=330)

    all_find_mark_color_show_label = tk.Label(setting_window,
                                              text=f"当前全局搜索匹配颜色：{config["all_find_mark_color"]}")
    all_find_mark_color_show_label.place(x=10, y=360)

    def ask_all_find_mark_color():
        k = colorchooser.askcolor(title="选择全局搜索匹配颜色", parent=win, initialcolor=config["all_find_mark_color"])
        if k[1] is not None:
            config["all_find_mark_color"] = str(k[1])
            all_find_mark_color_show_label.config(text=f"当前全局搜索匹配颜色：{k[1]}")
        else:
            messagebox.showerror("错误", "选择错误！请选择一个颜色！")

    all_find_mark_color_setting_button = tk.Button(setting_window, text="设置全局搜索匹配颜色",
                                                   command=ask_all_find_mark_color,
                                                   font=("Arial", 10),
                                                   width=16, height=1, bg="lightgray", fg="black", relief="raised",
                                                   bd=1,
                                                   activebackground="lightblue", activeforeground="black",
                                                   cursor="hand2",
                                                   overrelief="raised", state="normal", highlightcolor="white",
                                                   )
    all_find_mark_color_setting_button.place(x=10, y=390)

    """
    添加对鼠标按键标记颜色的设置
    """

    def show_button_key_color_setting_window():
        button_key_setting_window = tk.Toplevel(setting_window)
        button_key_setting_window.title("鼠标键颜色设置")
        button_key_setting_window.geometry("150x150")
        button_key_setting_window.resizable(False, False)

        def change_color(num: int):
            color = colorchooser.askcolor(title="选择颜色")[1]
            if color is not None:
                config["button_key"][str(num)] = str(color)
                key_color_labels[num].config(text=f"{num}键颜色: {config['button_key'][str(num)]}",
                                             bg=config["button_key"][str(num)])
                key_color_labels[num].config(bg=config["button_key"][str(num)])
                key_color_setting_buttons[num].config(bg=config["button_key"][str(num)])
            else:
                messagebox.showerror("颜色", "颜色为空！")
                return

        key_color_labels: dict[int, tk.Label] = {}
        key_color_setting_buttons: dict[int, tk.Button] = {}

        mouse_key_5_color_label = tk.Label(button_key_setting_window,
                                           text=f"鼠标5键颜色:{config["color_num_key"]["5"]}",
                                           bg=config["color_num_key"]["5"], fg="black", font=("Arial", 10))
        mouse_key_5_color_label.place(x=10, y=10)
        key_color_labels[5] = mouse_key_5_color_label

        mouse_key_5_color_setting_button = tk.Button(button_key_setting_window, text="设置鼠标5键颜色",
                                                     command=lambda: change_color(5),
                                                     font=("Arial", 10),
                                                     width=16, height=1, fg="black", relief="raised",
                                                     bd=1,
                                                     bg=config["color_num_key"]['5'],
                                                     activebackground="lightblue", activeforeground="black",
                                                     )
        mouse_key_5_color_setting_button.place(x=10, y=40)
        key_color_setting_buttons[5] = mouse_key_5_color_setting_button

        mouse_key_6_color_label = tk.Label(button_key_setting_window,
                                           text=f"鼠标6键颜色:{config["color_num_key"]["6"]}",
                                           bg=config["color_num_key"]["6"], fg="black", font=("Arial", 10))
        mouse_key_6_color_label.place(x=10, y=70)
        key_color_labels[6] = mouse_key_6_color_label

        mouse_key_6_color_setting_button = tk.Button(button_key_setting_window, text="设置鼠标6键颜色",
                                                     command=lambda: change_color(6),
                                                     font=("Arial", 10),
                                                     width=16, height=1, fg="black", relief="raised",
                                                     bd=1, bg=config["color_num_key"]['6'],
                                                     activebackground="lightblue", activeforeground="black",
                                                     )
        mouse_key_6_color_setting_button.place(x=10, y=100)
        key_color_setting_buttons[6] = mouse_key_6_color_setting_button

    button_key_color_setting_button = tk.Button(setting_window, text="鼠标键颜色设置",
                                                command=show_button_key_color_setting_window,
                                                font=("Arial", 10),
                                                width=14, height=1, bg="lightgray", fg="black", relief="raised", bd=1,
                                                activebackground="lightblue", activeforeground="black",
                                                cursor="hand2",
                                                overrelief="raised", highlightcolor="white",
                                                highlightbackground="white", highlightthickness=1,
                                                state="normal" if config["USE_BUTTON_KEY"] else "disabled",
                                                )

    button_key_color_setting_button.place(x=190, y=430)

    def if_USE_BUTTON_KEY__check():
        global config
        config["USE_BUTTON_KEY"] = if_USE_BUTTON_KEY_ckbtn_var.get()
        if if_USE_BUTTON_KEY_ckbtn_var.get():
            button_key_color_setting_button.config(state="normal")
        else:
            button_key_color_setting_button.config(state="disabled")

    if_USE_BUTTON_KEY_ckbtn_var = tk.BooleanVar()
    if_USE_BUTTON_KEY_ckbtn_var.set(bool(config["USE_BUTTON_KEY"]))
    if_USE_BUTTON_KEY_ckbtn = ttk.Checkbutton(setting_window, text="是否使用鼠标按键标记颜色",
                                              variable=if_USE_BUTTON_KEY_ckbtn_var,
                                              command=if_USE_BUTTON_KEY__check, style="Switch.TCheckbutton", onvalue=1,
                                              offvalue=0)
    if_USE_BUTTON_KEY_ckbtn.place(x=10, y=430)

    if_USE_MOUSE_WHEEL_ckbtn_var = tk.BooleanVar()
    if_USE_MOUSE_WHEEL_ckbtn_var.set(bool(config["USE_MOUSE_WHEEL"]))
    if_USE_MOUSE_WHEEL_ckbtn = ttk.Checkbutton(setting_window, text="是否使用鼠标滚轮上下翻页",
                                               variable=if_USE_MOUSE_WHEEL_ckbtn_var,
                                               style="Switch.TCheckbutton",
                                               onvalue=1,
                                               offvalue=0)
    if_USE_MOUSE_WHEEL_ckbtn.place(x=10, y=460)

    if_USE_KEY_TO_TURN_and_DOWN_ckbtn_var = tk.BooleanVar()
    if_USE_KEY_TO_TURN_and_DOWN_ckbtn_var.set(bool(config["USE_KEY_TO_TURN_and_DOWN"]))
    if_USE_KEY_TO_TURN_and_DOWN_ckbtn = ttk.Checkbutton(setting_window, text="是否使用键盘按键上下翻页",
                                                        variable=if_USE_KEY_TO_TURN_and_DOWN_ckbtn_var,
                                                        style="Switch.TCheckbutton", onvalue=1,
                                                        offvalue=0)
    if_USE_KEY_TO_TURN_and_DOWN_ckbtn.place(x=10, y=490)

    """
    添加对鼠标按键标记颜色的设置
    """

    reload_key_show_label = tk.Label(setting_window, text=f"当前重载热键：{config["reload_key"]}")
    reload_key_show_label.place(x=10, y=520)

    def ask_reload_key():
        if messagebox.askyesno("提示", "是否要重置热键？重置热键后，需要重新启动软件才能生效！", parent=win):
            k = simpledialog.askstring("重载热键", "请输入重载热键", parent=win)
            if k is not None and 0 < len(k) < 2:
                config["reload_key"] = k
                reload_key_show_label.config(text=f"当前重载热键：{k}")
            else:
                messagebox.showerror("错误", "热键错误！请输入一个字符！")

    reload_key_setting_button = tk.Button(setting_window, text="设置重载热键",
                                          command=ask_reload_key,
                                          font=("Arial", 10),
                                          width=16, height=1, bg="lightgray", fg="black", relief="raised", bd=1,
                                          activebackground="lightblue", activeforeground="black", cursor="hand2",
                                          overrelief="raised", state="normal", highlightcolor="white",
                                          )

    reload_key_setting_button.place(x=10, y=550)

    def if_USE_RELOAD_TIP__check():
        global config
        config["USE_RELOAD_TIP"] = if_USE_RELOAD_TIP_ckbtn_var.get()

    if_USE_RELOAD_TIP_ckbtn_var = tk.BooleanVar()
    if_USE_RELOAD_TIP_ckbtn_var.set(bool(config["USE_RELOAD_TIP"]))
    if_USE_RELOAD_TIP_ckbtn = ttk.Checkbutton(setting_window, text="是否启用重载提示",
                                              variable=if_USE_RELOAD_TIP_ckbtn_var,
                                              command=if_USE_RELOAD_TIP__check, style="Switch.TCheckbutton",
                                              onvalue=1,
                                              offvalue=0)
    if_USE_RELOAD_TIP_ckbtn.place(x=10, y=590)

    save_key_show_label = tk.Label(setting_window, text=f"当前保存热键：{config["save_key"]}")
    save_key_show_label.place(x=10, y=620)

    def ask_save_key():
        k = simpledialog.askstring("保存热键", "请输入保存热键", parent=win)
        if k is not None and 0 < len(k) < 2:
            config["save_key"] = k
            save_key_show_label.config(text=f"当前保存热键：{k}")
        else:
            messagebox.showerror("错误", "热键错误！请输入一个字符！")

    save_key_setting_button = tk.Button(setting_window, text="设置保存热键",
                                        command=ask_save_key,
                                        font=("Arial", 10),
                                        width=16, height=1, bg="lightgray", fg="black", relief="raised", bd=1,
                                        activebackground="lightblue", activeforeground="black", cursor="hand2",
                                        overrelief="raised", state="normal", highlightcolor="white",
                                        )

    save_key_setting_button.place(x=10, y=650)

    def if_USE_SAVE_TIP__check():
        global config
        config["USE_SAVE_TIP"] = if_USE_SAVE_TIP_ckbtn_var.get()

    if_USE_SAVE_TIP_ckbtn_var = tk.BooleanVar()
    if_USE_SAVE_TIP_ckbtn_var.set(bool(config["USE_SAVE_TIP"]))
    if_USE_SAVE_TIP_ckbtn = ttk.Checkbutton(setting_window, text="是否启用保存提示",
                                            variable=if_USE_SAVE_TIP_ckbtn_var,
                                            command=if_USE_SAVE_TIP__check,
                                            style="Switch.TCheckbutton", onvalue=1,
                                            offvalue=0)
    if_USE_SAVE_TIP_ckbtn.place(x=10, y=680)

    interval_show_label = tk.Label(setting_window, text=f"当前间隔：{config["interval"]}")
    interval_show_label.place(x=10, y=710)

    def ask_interval():
        k = simpledialog.askinteger("间隔(正整数)", "请输入间隔(越小，展示内容越多，程序响应越慢)", parent=win)
        if k is not None and k > 0:
            config["interval"] = k
            interval_show_label.config(text=f"当前间隔：{k}")
        else:
            messagebox.showerror("错误", "间隔错误！请输入一个正整数！")

    interval_setting_button = tk.Button(setting_window, text="设置间隔",
                                        command=ask_interval,
                                        font=("Arial", 10),
                                        width=16, height=1, bg="lightgray", fg="black", relief="raised", bd=1,
                                        activebackground="lightblue", activeforeground="black", cursor="hand2",
                                        overrelief="raised", state="normal", highlightcolor="white",
                                        )

    interval_setting_button.place(x=10, y=740)

    def if_USE_SAVE_TIP_WHEN_SETTING_CLOSE__check():
        global config
        config["USE_SAVE_TIP_WHEN_SETTING_CLOSE"] = if_USE_SAVE_TIP_WHEN_SETTING_CLOSE_ckbtn_var.get()

    if_USE_SAVE_TIP_WHEN_SETTING_CLOSE_ckbtn_var = tk.BooleanVar()
    if_USE_SAVE_TIP_WHEN_SETTING_CLOSE_ckbtn_var.set(bool(config["USE_SAVE_TIP_WHEN_SETTING_CLOSE"]))
    if_USE_SAVE_TIP_WHEN_SETTING_CLOSE_ckbtn = ttk.Checkbutton(setting_window, text="是否启用设置界面关闭时的保存提示",
                                                               variable=if_USE_SAVE_TIP_WHEN_SETTING_CLOSE_ckbtn_var,
                                                               command=if_USE_SAVE_TIP_WHEN_SETTING_CLOSE__check,
                                                               style="Switch.TCheckbutton", onvalue=1,
                                                               offvalue=0)
    if_USE_SAVE_TIP_WHEN_SETTING_CLOSE_ckbtn.place(x=260, y=710)

    def if_USE_SAVE_TIP_WHEN_MAIN_CLOSE__check():
        global config
        config["USE_SAVE_TIP_WHEN_MAIN_CLOSE"] = if_USE_SAVE_TIP_WHEN_MAIN_CLOSE_ckbtn_var.get()

    if_USE_SAVE_TIP_WHEN_MAIN_CLOSE_ckbtn_var = tk.BooleanVar()
    if_USE_SAVE_TIP_WHEN_MAIN_CLOSE_ckbtn_var.set(bool(config["USE_SAVE_TIP_WHEN_MAIN_CLOSE"]))
    if_USE_SAVE_TIP_WHEN_MAIN_CLOSE_ckbtn = ttk.Checkbutton(setting_window, text="是否启用翻译界面关闭时的保存提示",
                                                            variable=if_USE_SAVE_TIP_WHEN_MAIN_CLOSE_ckbtn_var,
                                                            command=if_USE_SAVE_TIP_WHEN_MAIN_CLOSE__check,
                                                            style="Switch.TCheckbutton", onvalue=1,
                                                            offvalue=0)
    if_USE_SAVE_TIP_WHEN_MAIN_CLOSE_ckbtn.place(x=260, y=740)

    #################################################

    right_click_menu_setting_window = tk.Menu(win, tearoff=0)
    right_click_menu_setting_window.add_command(label="保存配置至硬盘", command=save_to_hard_drive)

    def show_menu_(event):
        right_click_menu_setting_window.post(event.x_root, event.y_root)

    setting_window.bind("<Button-3>", show_menu_)

    meu = tk.Menu(win, tearoff=0)
    meu.add_command(label="保存配置至硬盘", command=save_to_hard_drive)

    setting_window.config(menu=meu)


def change_translate_api() -> None:
    global config
    config["translate_api"] = mue_translate_api_choose_var.get()


def translate(text: str, sourceLang: str = "auto", targetLang: str = "zh") -> str | None:
    if config["translate_api"] == GOOGLE:
        return None
    elif config["translate_api"] == BAIDU:
        return None
    elif config["translate_api"] == SOUGO:
        return translate_with_check(text, sourceLang, targetLang)
    elif config["translate_api"] == TENCENT:
        return None
    elif config["translate_api"] == DEEPL:
        return deepl_translate_with_check(text, sourceLang, targetLang)

    return None


def fast_option(r: str) -> bool:
    if r:
        pass
    t = [
        mue_translate_options_fast_var_remove_jp.get() and r == 'jp',
        mue_translate_options_fast_var_remove_ko.get() and r == 'ko'
    ]
    print(t)
    if not any(t):
        return True
    return False


def check(lang: str) -> bool:
    if if_open_fast_translate.get():
        if lang != "zh-cn" and fast_option(lang):
            return True
        return False
    else:
        if lang != "zh-cn":
            return True
        return False


def translate_and_auto_fill() -> None:
    text_translated = translate(inputs[keys_list[page]].get())
    if text_translated is not None:
        inputs[keys_list[page]].delete(0, tk.END)
        inputs[keys_list[page]].insert(0, text_translated)
        inputs[keys_list[page]].focus_set()


def translate_and_copy() -> None:
    text_translated = translate(inputs[keys_list[page]].get())
    if text_translated is not None:
        pyperclip.copy(text_translated)


def translate_and_auto_fill_all() -> None:
    global translate_api

    if translate_api == DEEPL:
        messagebox.showwarning("警告", "如果使用DeepL进行批量翻译，你的IP地址有极大可能被永久封禁，请谨慎使用！")
        if not messagebox.askokcancel("警告", "是否继续？(翻译间隔为3秒)"):
            return None

    def translate_all() -> None:
        global keys_list, inputs, page, translate_api, show_progress_window
        show_progress_window = tk.Toplevel(win)
        show_progress_window.title("翻译进度")
        show_progress_window.geometry("300x100")
        show_progress_window.resizable(False, False)
        show_progress_window.iconbitmap("tb.ico")
        show_progress_window.protocol("WM_DELETE_WINDOW", lambda: None)
        bar = ttk.Progressbar(show_progress_window, orient="horizontal", length=280, mode="determinate")
        bar["maximum"] = len(keys_list)
        bar.place(x=10, y=10)

        def to_f() -> None:
            global page
            page = n

        def stop_event_() -> None:
            stop_event.set()
            show_progress_window.destroy()
            return None

        bar_btn = tk.Button(show_progress_window, text="0/0\n0%", font=("Arial", 10), width=25, height=2,
                            bg="lightgray",
                            fg="black", relief="raised", bd=1, activebackground="lightblue", activeforeground="black",
                            state="normal", highlightcolor="white", command=to_f)
        bar_btn.place(x=10, y=40)

        stop_btn = tk.Button(show_progress_window, text="停止", font=("Arial", 10), width=4, height=2,
                             bg="lightgray",
                             fg="black", relief="raised", bd=1, activebackground="lightblue", activeforeground="black",
                             state="normal", highlightcolor="white", command=stop_event_)
        stop_btn.place(x=220, y=40)

        for n in range(len(keys_list)):
            r: str = ''
            try:
                r = langdetect.detect(inputs[keys_list[n]].get())
            except langdetect.lang_detect_exception.LangDetectException:
                # messagebox.showerror("错误", "无法检测当前语言")
                pass
            print(r)
            if check(r):
                if stop_event.is_set():
                    show_progress_window.destroy()
                    return None
                if translate_api == DEEPL:
                    time.sleep(3)
                if stop_event.is_set():
                    show_progress_window.destroy()
                    return None
                text_translated = translate(inputs[keys_list[n]].get())
                if text_translated is not None:
                    inputs[keys_list[n]].delete(0, tk.END)
                    inputs[keys_list[n]].insert(0, text_translated)
                    inputs[keys_list[n]].focus_set()

            if stop_event.is_set():
                show_progress_window.destroy()
                return None
            bar["value"] = n + 1
            if stop_event.is_set():
                show_progress_window.destroy()
                return None
            bar_btn.config(text=f"{bar['value']}/{bar['maximum']}\n{bar['value'] / bar['maximum'] * 100:.2f}%")
            if bar["value"] == bar["maximum"]:
                show_progress_window.destroy()
                return None
            if stop_event.is_set():
                show_progress_window.destroy()
                return None

            show_progress_window.update_idletasks()

        messagebox.showinfo("提示", "翻译完成")

    t1 = threading.Thread(target=translate_all)
    t1.start()


def translate_and_write_into_json_all() -> None:
    def t() -> None:
        global keys_list, inputs, page, translate_api, show_progress_window
        show_progress_window = tk.Toplevel(win)
        show_progress_window.title("翻译进度")
        show_progress_window.geometry("300x100")
        show_progress_window.resizable(False, False)
        show_progress_window.iconbitmap("tb.ico")
        show_progress_window.protocol("WM_DELETE_WINDOW", lambda: None)
        bar = ttk.Progressbar(show_progress_window, orient="horizontal", length=280, mode="determinate")
        bar["maximum"] = len(keys_list)
        bar.place(x=10, y=10)

        def to_f() -> None:
            global page
            page = n

        def stop_event_() -> None:
            stop_event.set()
            show_progress_window.destroy()
            return None

        bar_btn = tk.Button(show_progress_window, text="0/0\n0%", font=("Arial", 10), width=25, height=2,
                            bg="lightgray",
                            fg="black", relief="raised", bd=1, activebackground="lightblue", activeforeground="black",
                            state="normal", highlightcolor="white", command=to_f)
        bar_btn.place(x=10, y=40)

        stop_btn = tk.Button(show_progress_window, text="停止", font=("Arial", 10), width=4, height=2,
                             bg="lightgray",
                             fg="black", relief="raised", bd=1, activebackground="lightblue", activeforeground="black",
                             state="normal", highlightcolor="white", command=stop_event_)
        stop_btn.place(x=220, y=40)

        output_json: dict[str, str] = {}

        for n in range(len(keys_list)):
            r: str = ''
            try:
                r = langdetect.detect(inputs[keys_list[n]].get())
            except langdetect.lang_detect_exception.LangDetectException:
                # messagebox.showerror("错误", "无法检测当前语言")
                pass
            print(r)
            if check(r):
                if stop_event.is_set():
                    show_progress_window.destroy()
                    return None
                if translate_api == DEEPL:
                    time.sleep(3)
                if stop_event.is_set():
                    show_progress_window.destroy()
                    return None
                text_translated = translate(inputs[keys_list[n]].get())
                if text_translated is not None:
                    output_json[keys_list[n]] = text_translated

            if stop_event.is_set():
                show_progress_window.destroy()
                return None
            bar["value"] = n + 1
            if stop_event.is_set():
                show_progress_window.destroy()
                return None
            bar_btn.config(text=f"{bar['value']}/{bar['maximum']}\n{bar['value'] / bar['maximum'] * 100:.2f}%")
            if bar["value"] == bar["maximum"]:
                show_progress_window.destroy()
                return None
            if stop_event.is_set():
                show_progress_window.destroy()
                return None

            show_progress_window.update_idletasks()

        messagebox.showinfo("提示", "翻译完成\n开始写入文件")

        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(output_json, f, ensure_ascii=False, indent=4)

        messagebox.showinfo("提示", "写入完成")

    t1 = threading.Thread(target=t)
    t1.start()


right_click_menu = tk.Menu(win, tearoff=0)
right_click_menu.add_command(label="添加一项", command=add_item)
right_click_menu.add_command(label="删除一项", command=remove_item)
right_click_menu.add_command(label="自动补全与对比语言文件缺少部分", command=complete_missing_parts)
right_click_menu.add_separator()
right_click_menu.add_command(label="翻译当前项并自动替换(谨慎使用)", command=translate_and_auto_fill)
right_click_menu.add_command(label="翻译当前项并复制", command=translate_and_copy)
right_click_menu.add_separator()
right_click_menu.add_command(label="失去所有输入框焦点", command=release_focus)
right_click_menu.add_command(label="保存", command=save)
right_click_menu.add_command(label="从硬盘重载", command=reload_from_hard_drive)
right_click_menu.add_command(label="从内存重载", command=reload)
right_click_menu.add_separator()
right_click_menu.add_command(label="设置", command=show_setting_window)
right_click_menu.add_separator()
right_click_menu.add_command(label="退出", command=quit_win)

win.bind("<Button-3>", show_menu)

menubar = tk.Menu(win)
menubar.add_command(label="设置", command=show_setting_window)

mue_reload = tk.Menu(win, tearoff=0)
mue_reload.add_command(label="从硬盘重载", command=reload_from_hard_drive)
mue_reload.add_command(label="从内存重载", command=reload)

menubar.add_cascade(label="重载", menu=mue_reload)

mue_operator = tk.Menu(win, tearoff=0)
mue_operator.add_command(label="添加一项", command=add_item)
mue_operator.add_command(label="删除一项", command=remove_item)
mue_operator.add_command(label="自动补全与对比语言文件缺少部分", command=complete_missing_parts)

menubar.add_cascade(label="操作", menu=mue_operator)

mue_translate_api_choose = tk.Menu(win, tearoff=0)
mue_translate_api_choose_var = tk.StringVar()
mue_translate_api_choose.add_radiobutton(label="搜狗", command=lambda: change_translate_api,
                                         variable=mue_translate_api_choose_var, value=SOUGO)
# mue_translate_api_choose.add_command(label="百度", command=lambda: change_translate_api(BAIDU))
# mue_translate_api_choose.add_command(label="腾讯", command=lambda: change_translate_api(TENCENT))
# mue_translate_api_choose.add_command(label="有道", command=lambda: change_translate_api(YOUDAO))
mue_translate_api_choose.add_radiobutton(label="Deepl(有翻译频率限制)", command=lambda: change_translate_api,
                                         variable=mue_translate_api_choose_var, value=DEEPL)

menubar.add_cascade(label="更改翻译API", menu=mue_translate_api_choose)

mue_translate = tk.Menu(win, tearoff=0)
mue_translate.add_command(label="翻译当前项并自动替换(谨慎使用)", command=translate_and_auto_fill)
mue_translate.add_command(label="翻译当前项并复制", command=translate_and_copy)
mue_translate.add_separator()
mue_translate.add_command(label="翻译全部项并自动替换(谨慎使用)", command=translate_and_auto_fill_all)
mue_translate.add_command(label="翻译全部项并写入json文件", command=translate_and_write_into_json_all)

menubar.add_cascade(label="翻译", menu=mue_translate)

mue_translate_options = tk.Menu(win, tearoff=0)
if_open_fast_translate = tk.BooleanVar()
mue_translate_options.add_checkbutton(label="开启快速翻译", variable=if_open_fast_translate)

mue_translate_options_fast = tk.Menu(win, tearoff=0)
mue_translate_options_fast_var_remove_ko = tk.BooleanVar()
mue_translate_options_fast_var_remove_jp = tk.BooleanVar()
mue_translate_options_fast.add_checkbutton(label="忽略韩语", variable=mue_translate_options_fast_var_remove_ko)
mue_translate_options_fast.add_checkbutton(label="忽略日语", variable=mue_translate_options_fast_var_remove_jp)

mue_translate_options.add_cascade(label="快速翻译(忽略语言)", menu=mue_translate_options_fast)

menubar.add_cascade(label="翻译选项", menu=mue_translate_options)

menubar.add_command(label="失去所有输入框焦点", command=release_focus)
menubar.add_command(label="保存", command=save)

menubar.add_command(label="退出", command=quit_win)

win.config(menu=menubar)

win.protocol("WM_DELETE_WINDOW", quit_win)


def quit_win_(event=None):
    global stop_event
    if event:
        pass
    if USE_SAVE_TIP_WHEN_MAIN_CLOSE:
        if messagebox.askyesno("保存", "是否保存？"):
            save()
    stop_event.set()
    win.destroy()


win.bind("<Control-q>", quit_win_)


def update():
    global show_num

    show_num = win.winfo_height() // interval

    for k_, v_ in states.items():
        labels[k_].config(background=v_)

    for k_, v_ in inputs.items():
        main_lang.change_lang(k_, v_.get())

    for _ in range(len(show_order)):
        if page - 1 < _ < show_num + page + 1:
            labels[keys_list[_]].place(x=5, y=(_ - page) * interval)
            inputs[keys_list[_]].place(x=lens_key[_] * 9 + 10, y=(_ - page) * interval)
        else:
            labels[show_order[_]].place_forget()
            inputs[show_order[_]].place_forget()

    if stop_event.is_set() and not show_progress_window.winfo_exists():
        stop_event.clear()

    win.update_idletasks()
    win.after(0, update)


update()

win.mainloop()
