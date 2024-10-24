import requests
from bs4 import BeautifulSoup


def collect_links(url):
    response = requests.get(url)
    if response.status_code != 200:
        print('Could not fetch the page')
        exit(1)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_links = set()
    for link in soup.find_all('a', href=True):
        if "/help" in link['href'] and "notion-academy" not in link['href']:
            article_links.add(url + link['href'][len('/help'):])
    return article_links


def extract_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    contents = []
    current_group = []
    for element in soup.find_all(["h1", "h2", "h3", "p"]):
        if element.name in ["h1", "h2", "h3"]:
            if current_group:
                contents.append("\n".join(current_group))
            current_group = [element.get_text(strip=True)]
        else:
            current_group.append(element.get_text(strip=True))
    return contents


def chunk_content(contents, max_chunk_size=750):
    chunks = []
    chunk = ""
    for content in contents:
        if len(chunk) + len(content) < max_chunk_size:
            chunk += content
        else:
            chunks.append(chunk)
            chunk = content
    return chunks


if __name__ == "__main__":
    base_url = "https://www.notion.so/help"
    chunks = []
    for link in collect_links(base_url):
        print(f"start collect content from link: {link}")
        chunks.extend(chunk_content(extract_content(link)))
        print(f"finish chunking for {link}")
    print(chunks)









