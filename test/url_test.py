from urllib.parse import urlparse

def get_name_by_url(url):
    if not url:
        print("URL is empty or None")
        return None

    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path
    if path and path.endswith("/"):
        path = path[:-1]

    if domain.startswith("www."):
        domain = domain[4:]

    name = (domain.replace(".", "-") + path.replace("/", "-")).replace(".", "-")

    return name

# 测试示例
url1 = "https://scrmchampion.com"
url2 = "https://openai.com/blog/chatgpt"

print(get_name_by_url(url1))
print(get_name_by_url(url2))