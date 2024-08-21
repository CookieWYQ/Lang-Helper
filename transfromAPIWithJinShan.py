__all__ = ["translate_with_dict"]


def translate_with_dict(text: str) -> str:
    import requests
    from bs4 import BeautifulSoup

    # 定义请求头部
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    }

    # 定义请求的URL
    url = f"https://www.iciba.com/word?w={text}"

    # 发送POST请求
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find_all("div", class_='Mean_normal__mkzjn')[0].text


if __name__ == "__main__":
    print(translate_with_check("hello"))
