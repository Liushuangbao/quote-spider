import requests, sqlite3, time
from bs4 import BeautifulSoup

def get_page(url):
    try:
        resp = requests.get(url, timeout=7)
        resp.raise_for_status()
    except Exception as e:
        print("请求失败:", e)
        return None

    return BeautifulSoup(resp.text, "html.parser")
    
def parse_page(soup):
    data = [] 
    for q in soup.find_all("div", class_="quote"):
        text = q.find("span", class_="text").get_text()
        author = q.find("small", class_="author").get_text()
        tags = [t.get_text() for t in q.find_all("a", class_="tag")]
        data.append((text, author, ",".join(tags)))
    return data

def save(data):
    conn = sqlite3.connect("quote.db")
    cur = conn.cursor()

    cur.execute("""
            CREATE TABLE IF NOT EXISTS quotes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT, author TEXT, tags TEXT)
            """)

    for text, author, tags in data:
        cur.execute(
            "INSERT INTO quotes (text, author, tags) VALUES (?, ?, ?)",
            (text, author, tags)
        )

    conn.commit()
    conn.close()

def clear_db():
    conn = sqlite3.connect("quote.db")
    cur = conn.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS quotes
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT, author TEXT, tags TEXT)
            """)
    cur.execute("DELETE FROM quotes")
    conn.commit()
    conn.close()

def main():
    clear_db()
    
    BASE = "https://quotes.toscrape.com"
    url = "/"
    start = time.time()
    print("查询数据中...")

    while url:
        soup = get_page(BASE + url)
        if soup is None:
            break
        save(parse_page(soup))
        next_tag = soup.find("li", class_="next")
        url = next_tag.find("a")["href"] if next_tag else None
        time.sleep(0.2)

    conn = sqlite3.connect("quote.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM quotes")
    print("数据库里有", cur.fetchone()[0], "条")
    conn.close()

    over = time.time()

    print("全部抓完...", f"共耗时{over-start:.2f}")

main()
