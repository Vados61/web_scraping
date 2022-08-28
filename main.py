import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from progress.bar import IncrementalBar


KEYWORDS = {'дизайн', 'фото', 'web', 'python'}  # по указаным ключам не было совпадений в момент проверки
base_url = 'https://habr.com/ru/all/'
headers = Headers(os="win", headers=True).generate()
ret = requests.get(base_url, headers=headers)
soup = BeautifulSoup(ret.text, 'html.parser')

posts = soup.find_all('article')
bar = IncrementalBar("Проверяем пост", max=len(posts))
for post in posts:
    text = ''
    for el in post.find(class_='tm-article-body tm-article-snippet__lead').find_all('p'):
        text += el.text
    title = post.find(class_='tm-article-snippet__title-link').find('span').text
    date = post.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title']
    href = 'https://habr.com' + post.find(class_='tm-article-snippet__title-link').attrs['href']
    intersection = KEYWORDS & set(text.lower().split()) or KEYWORDS & set(title.lower().split())
    if intersection:
        print(f'{date} - {title} - {href}')
    else:
        post_text = requests.get(href, headers=headers)
        soup_post = BeautifulSoup(post_text.text, 'html.parser')
        body = soup_post.find(id='post-content-body').find_all('p')
        text = str(text)
        for el in body:
            text += el.text
        if intersection:
            print(f'{date} - {title} - {href}')
    bar.next()
bar.finish()
