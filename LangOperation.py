import os

__all__ = ['LangOperation', 'if_skip']


def if_skip(key: str | None):
    if key is None:
        return True

    if key == '':
        return True
    elif key == ' ':
        return True
    elif key == '#':
        return True

    if key.startswith('//') or key.startswith('/*') or key.startswith('*/') or key.startswith('#'):
        return True

    if key.endswith('//') or key.endswith('/*') or key.endswith('*/') or key.endswith('#'):
        return True

    if key == len(key) * '#':
        return True

    if '=' not in key:
        return True

    if len(key.split('=')) < 2:
        return True

    return False


class LangOperation:
    """
    该类用于操作语言文件，包括读取、对比、写入和保存语言文件。
    """

    def __init__(self, lang_path: str) -> None:
        """
        初始化方法，用于加载语言文件到内存中。

        参数:
        - lang_path: 语言文件的路径。
        """
        # 检查语言文件路径是否存在，如果不存在则抛出异常
        if not os.path.exists(lang_path):
            raise FileNotFoundError(f'{lang_path} not found')

        # 检查是不是lang文件
        if not lang_path.endswith('.lang'):
            raise ValueError(f'{lang_path} is not a lang file')

        # 打开语言文件并读取所有行
        with open(lang_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 处理读取的每一行，将其转换为字典格式
        lang_dict = {}
        for line in lines:
            line = line.strip()
            if line and not if_skip(line):
                key, value = line.split('=')
                lang_dict[key] = value

        # 初始化实例变量
        self.lang_path = lang_path
        self.lines = lang_dict

    def read_lang(self) -> dict[str, str]:
        """
        读取语言文件的内容。

        返回:
        包含语言项的字典。
        """
        return self.lines

    def contrast_lang(self, other: 'LangOperation') -> dict[str, str]:
        """
        对比当前语言文件与另一个语言文件的差异。

        参数:
        - other: 另一个LangOperation对象，用于对比。

        返回:
        一个字典，包含在当前语言文件中不存在而另一个文件中存在的语言项。
        """
        diff = {}
        for key in other.lines:
            if key not in self.lines:
                diff[key] = other.lines[key]
        return diff

    def save_lang(self, new_lang_path: str | None = None) -> None:
        """
        保存当前语言文件。如果提供了新的文件路径，则将内容保存到新路径。

        参数:
        - new_lang_path: 可选参数，指定新的语言文件路径。
        """
        if new_lang_path:
            save_path = new_lang_path
        else:
            save_path = self.lang_path

        # 将语言项字典内容写入文件
        with open(save_path, 'w', encoding='utf-8') as f:
            for key, value in self.lines.items():
                f.write(f'{key}={value}\n')

    def change_lang(self, key: str, value: str) -> None:
        """
        修改语言文件中的某个语言项。

        参数:
        - key: 需要修改的语言项的键。
        - value: 语言项的新值。
        """
        self.lines[key] = value

    def remove_lang(self, key: str) -> None:
        """
        删除语言文件中的某个语言项。

        参数:
        - key: 需要删除的语言项的键。
        """
        del self.lines[key]

    def write_lang_by_obj(self, other: 'LangOperation', cover: bool = True) -> None:
        """
        将另一个语言文件的内容写入当前语言文件。

        参数:
        - other: 另一个LangOperation对象，其内容将被写入当前文件。
        - cover: 覆盖模式，如果为True，则覆盖当前语言文件中已存在的键。
        """
        for key, value in other.lines.items():
            if key in self.lines and not cover:
                continue
            self.lines[key] = value

    def write_lang_by_dict(self, other: dict[str, str], cover: bool = True) -> None:
        """
        将字典中的内容写入当前语言文件。

        参数:
        - other: 包含语言项的字典。
        - cover: 覆盖模式，如果为True，则覆盖当前语言文件中已存在的键。
        """
        for key, value in other.items():
            if key in self.lines and not cover:
                continue
            self.lines[key] = value

    def complete_lang_by_obj(self, other: 'LangOperation') -> None:
        """
        补全该语言文件中相较于提供的LangOperation对象中的缺失项。
        """
        self.write_lang_by_obj(other, False)

    def complete_lang_by_dict(self, other: dict[str, str]) -> None:
        """
        补全该语言文件中相较于提供的字典中的缺失项。
        """
        self.write_lang_by_dict(other, False)


if __name__ == '__main__':
    # 实例化英文和中文的语言操作对象，并对比其差异
    en_lang_op = LangOperation('fy_ok/en_us.lang')
    zh_lang_op = LangOperation('fy_ok/zh_cn.lang')
    # 输出两种语言文件的差异
    for k, v in zh_lang_op.contrast_lang(en_lang_op).items():
        print(f"{k} -> {v}")

    # 循环接收用户输入，修改中文语言文件，并记录修改内容
    modifications = {}
    while True:
        try:
            key_ = input('key: ')
            value_ = input('value: ')
            zh_lang_op.change_lang(key_, value_)
            modifications[key_] = value_
        except KeyboardInterrupt:
            # 输出所有修改内容和记录的修改项
            print(en_lang_op.contrast_lang(zh_lang_op).items())
            print('-----------------------------------')
            for k, v in modifications.items():
                print(f"{k} -> {v}")
            break
