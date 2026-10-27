# 1阶
# import requests
# url = "https://quotes.toscrape.com/"
# resp = requests.get(url, timeout=9)

# print("状态码：", resp.status_code)
# print("网页长度：", len(resp.text))
# print(resp.text[ :500])


# 2阶
# from bs4 import BeautifulSoup
# import requests
# resp = requests.get("https://quotes.toscrape.com/",  timeout=9)
# soup = BeautifulSoup(resp.text, "html.parser")

# quotes = soup.find_all("div", class_="quote")
# print(f"抓到{len(quotes)}条")

# def main():
#     data = [(q.find("span", class_="text").get_text(),
#                 q.find("small", class_="author").get_text()) for q in quotes]
#     for text ,author in data:
#         print(text)
#         print("--", author)
#         print()

# main()


# 3阶
import time
import requests
from bs4 import BeautifulSoup

BASE = "https://quotes.toscrape.com"
url = "/"
total = 0

start = time.time()
while url:
    try:
        resp = requests.get(BASE + url, timeout=9)
        resp.raise_for_status
    except Exception as e:
        print("请求失败：", e)

    soup = BeautifulSoup(resp.text, "html.parser")
    for q in soup.find_all("div", class_="quote"):
        text = q.find("span", class_="text").get_text()
        author = q.find("small", class_="author").get_text()
        total += 1
        print(total, author)

    next_tag = soup.find("li", class_="next")
    url = next_tag.find("a")["href"] if next_tag else None   

over = time.time()
print(f"全部抓完，共{total}条...")
print(f"用时{over - start}...")

        
