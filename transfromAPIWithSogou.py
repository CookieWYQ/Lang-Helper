import requests
try:
    from bs4 import BeautifulSoup
except ImportError:
    import pip
    pip.main(['install', 'bs4'])
    from bs4 import BeautifulSoup

ERROR = 'ERROR'


class TranslateError(Exception):
    pass


def translate_with_check(text: str, sourceLang: str = "auto", targetLang: str = "zh") -> str:
    url = f"https://fanyi.sogou.com/text?keyword={text}&transfrom={sourceLang}&transto={targetLang}&model=general"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find_all(id="trans-result", class_="output-val")
    if len(result) == 0:
        raise TranslateError(ERROR + f"翻译失败(在翻译{text}时)")
    result = result[0].text
    return result


if __name__ == '__main__':
    while True:
        print(translate_with_check("hello, world"))
