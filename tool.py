__all__ = ["json_or_lang_path", "is_jar"]


def json_or_lang_path(path: str) -> bool | None:  # True -> json, False -> lang, None -> error
    """
    判断路径是否为json文件或lang文件
    :param path: 路径
    :return: True -> json, False -> lang, None -> error
    """
    import os
    if os.path.isfile(path):
        if path.endswith(".json"):
            return True
        elif path.endswith(".lang"):
            return False
    else:
        return None


def is_jar(path: str) -> bool | None:
    """
    判断路径是否为jar文件
    :param path: 路径
    :return: True -> jar, False -> not jar, error -> None
    """
    import os
    if os.path.isfile(path):
        if path.endswith(".jar"):
            return True
        else:
            return False
    else:
        return None
