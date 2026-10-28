# quote-spider

爬 quotes.toscrape.com 全站名言，存进 SQLite。

Python 3 + requests + BeautifulSoup4 + SQLite。

## 运行

```bash
pip install requests beautifulsoup4
python spider.py
```

跑完会在同目录生成 `quote.db`，终端输出：

```
全部抓完，共 100 条，共耗时 12.34 秒
数据库里有 100 条
```

## 代码结构

```
get_page(url)     请求一个页面，返回 BeautifulSoup；失败返回 None
parse_page(soup)  从页面里拆出 [(名言, 作者, 标签), ...]
save(data)        写进数据库
main()            分页循环，把上面三个串起来
```

## 几个有意的写法

- **翻页**：读页面底部的 `li.next`，读不到就说明是最后一页
- **失败处理**：请求带 `timeout`，失败就退出循环，不至于让程序崩掉
- **写库用 `?` 占位符**：不拼字符串，避免 SQL 注入
- **每页之间 sleep 一下**：不给对方服务器添麻烦
- **最后查一次 `COUNT(*)`**：跟程序自己数的条数对一遍，确认没漏数据

## 数据样式

```
(text, author, tags)
"The world as we have created it is a process of our thinking..." | Albert Einstein | change,thinking,world
"It is our choices, Harry, that show what we truly are..."        | J.K. Rowling    | abilities,choices
```
