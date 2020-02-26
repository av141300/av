import requests
from bs4 import BeautifulSoup

url = 'https://www.eurookna.ru/okna/plastikovye-proizvoditelya/'

def get_html(url):
    r = requests.get(url)    # Получаем метод Response
    r.encoding = 'utf8'      # У меня были проблемы с кодировкой, я задал в ручную
    return r.text            # Вернем данные объекта text

def get_head(html):
    soup = BeautifulSoup(html, 'lxml')
    head = soup.find_all('h1')
    heads = []
    for i in head:
       heads.append(i.string.strip())
    return heads

def parse(data):
    results = []
    soup = BeautifulSoup(data, 'lxml')

    h1 = get_head(data)[0]
    title = soup.title.string.strip()
    results.append({
        'title': title,
        'h1': h1,
    })
    return results


data = get_html(url)
a = parse(data)

with open('temp.xml', 'w') as output_file:
    output_file.write(
        '''
<?xml version="1.0" encoding="cp1251"?>
<item turbo="true">
    <title>''' + a[0]['title'] + '''</title>
    <link>'''+ url +'''</link>
    <turbo:content>
        <![CDATA[
            <header>
                <h1>'''+ a[0]['h1'] +'''</h1>
                <h2>Вкусно и полезно</h2>
                <figure>
                    <img src="https://avatars.mds.yandex.net/get-sbs-sd/403988/e6f459c3-8ada-44bf-a6c9-dbceb60f3757/orig">
                </figure>
                <menu>
                   <a href="http://example.com/page1.html">Пункт меню 1</a>
                   <a href="http://example.com/page2.html">Пункт меню 2</a>
                </menu>
            </header>
            <p>Как хорошо начать день? Вкусно и полезно позавтракать!</p>
            <p>Приходите к нам на завтрак. Фотографии наших блюд ищите <a href="#">на нашем сайте</a>.</p>
            <h2>Меню</h2>
            <figure>
               <img src="https://avatars.mds.yandex.net/get-sbs-sd/369181/49e3683c-ef58-4067-91f9-786222aa0e65/orig">
                <figcaption>Омлет с травами</figcaption>
            </figure>
            <p>В нашем меню всегда есть свежие, вкусные и полезные блюда.</p>
            <p>Убедитесь в этом сами.</p>
            <button formaction="tel:+7(123)456-78-90"
                    data-background-color="#5B97B0"
                    data-color="white"
                    data-primary="true">Заказать столик</button>
            <div data-block="widget-feedback" data-stick="false">
                <div data-block="chat" data-type="whatsapp" data-url="https://whatsapp.com"></div>
                <div data-block="chat" data-type="telegram" data-url="http://telegram.com/"></div>
                <div data-block="chat" data-type="vkontakte" data-url="https://vk.com/"></div>
                <div data-block="chat" data-type="facebook" data-url="https://facebook.com"></div>
                <div data-block="chat" data-type="viber" data-url="https://viber.com"></div>
            </div>
            <p>Наш адрес: <a href="#">Nullam dolor massa, porta a nulla in, ultricies vehicula arcu.</a></p>
            <p>Фотографии — http://unsplash.com</p>
        ]]>
    </turbo:content>
</item>

        '''
    )
