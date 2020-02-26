import requests
from lxml import html
from lxml import etree
url = 'http://eurookna.ru'
page = requests.get(url)

with open('temp.html', 'w') as output_file:
   output_file.write(str(page.text.encode('utf-8').strip()))

def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text

def parse(filename):
    results = []
    phone_number = '+79252234545' # один номер для всех страниц

    text = read_file(filename)
    tree = html.fromstring(text)

    title = tree.xpath('//title/text()')
    h1 = tree.xpath('//h1/text()')

    results.append({
      'title' : title,
      'h1': h1,
      'phone_number': phone_number
    })

    return results

a = parse('temp.html')

for i in a:
  h1 = str(i['h1'])
  title = str(i['title'])

with open('temp.xml', 'w') as output_file:
    output_file.write(
        '''
<?xml version="1.0" encoding="cp1251"?>
<item turbo="true">
    <title>'''+ title  +'''Заголовок страницы</title>
    <link>https://okna-poz.ru</link>
    <turbo:content>
        <![CDATA[
            <header>
                <h1>Ресторан «Полезный завтрак»</h1>
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
