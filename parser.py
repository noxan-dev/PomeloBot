from bs4 import BeautifulSoup


def parse(html):
    parser = BeautifulSoup(html, 'html.parser')
    return parser.get_text('\n', strip=True)


