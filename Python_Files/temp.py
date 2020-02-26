import requests
from bs4 import BeautifulSoup
site = 'https://www.eurookna.ru'
url = 'https://www.eurookna.ru/okna/steklopaket-na-zakaz-bez-ramy/1213/'
author = 'eurookna.ru'
code = "cp1251"
noimage = '/local/templates/201907/images/banner_2020_small.jpg'

def get_html(url):
    r = requests.get(url)    # Получаем метод Response
    r.encoding = 'utf-8'      # У меня были проблемы с кодировкой, я задал в ручную
    return r.text            # Вернем данные объекта text

def get_head(html):
    soup = BeautifulSoup(html, 'lxml')
    head = soup.find_all('h1')
    heads = []
    for i in head:
       heads.append(i.string.strip())
    return heads

def get_image(html):
    soup = BeautifulSoup(html, 'lxml')
    images = []
    if soup.findAll('img',attrs={"class":"turbo-image"}) != []:
        image = soup.findAll('img', attrs={"class":"turbo-image"})
    elif soup.findAll('img', attrs={"class":"uk-cover"}) != []:
        image = soup.findAll('img', attrs={"class":"uk-cover"})
    else:
        image = [{'data-src' : noimage}]
    for i in image:
        images.append(i['data-src'].strip())
    return images

def get_preview_text(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        preview_text = soup.find('div', class_='turbo-preview-text').text.strip()
    except:
        preview_text = ''
    return preview_text

def parse(data):
    results = []
    soup = BeautifulSoup(data, 'lxml')

    h1 = get_head(data)[0]
    title = soup.title.string.strip()
    description = soup.findAll(attrs={"name":"description"})[0]['content'].strip()
    main_image_url = get_image(data)
    preview_text = get_preview_text(data)
    results.append({
        'title': title,
        'h1': h1,
        'description' : description,
        'main_image_url' : main_image_url,
        'preview_text' : preview_text
    })
    return results

data = get_html(url)
a = parse(data)

with open('temp.xml', 'w') as output_file:
    output_file.write(
'''<?xml version="1.0" encoding="'''+ code + '''"?>
<rss xmlns:yandex="http://news.yandex.ru" 
     xmlns:media="http://search.yahoo.com/mrss/" 
     xmlns:turbo="http://turbo.yandex.ru" 
     version="2.0">
    <channel>       
        <item turbo="true">
            <link>'''+ url +'''</link>
            <turbo:source>'''+ url +'''</turbo:source>
            <turbo:topic>''' + a[0]['title'] + '''</turbo:topic>
            <author>'''+ author +'''</author>
            <turbo:content>
                <![CDATA[
                    <header>
                        <h1>'''+ a[0]['h1'] +'''</h1>
                        <figure>
                            <img src="''' + site + a[0]['main_image_url'][0] + '''">
                        </figure>
                        <p>'''+ a[0]['preview_text'] +'''</p>
                        <menu>
                           <a href="http://example.com/page1.html">53453</a>
                           <a href="http://example.com/page2.html">2342</a>
                        </menu>
                    </header>
                    <figure>
                       <img src="https://avatars.mds.yandex.net/get-sbs-sd/369181/49e3683c-ef58-4067-91f9-786222aa0e65/orig">
                        <figcaption></figcaption>
                    </figure>
                   
                    <button formaction="tel:+7(123)456-78-90"
                            data-background-color="#5B97B0"
                            data-color="white"
                            data-primary="true"></button>
                    <div data-block="widget-feedback" data-stick="false">
                        <div data-block="chat" data-type="whatsapp" data-url="https://whatsapp.com"></div>
                        <div data-block="chat" data-type="telegram" data-url="http://telegram.com/"></div>
                        <div data-block="chat" data-type="vkontakte" data-url="https://vk.com/"></div>
                        <div data-block="chat" data-type="facebook" data-url="https://facebook.com"></div>
                        <div data-block="chat" data-type="viber" data-url="https://viber.com"></div>
                    </div>
                    <p><a href="#">Nullam dolor massa, porta a nulla in, ultricies vehicula arcu.</a></p>
                    <p>http://unsplash.com</p>
                ]]>
            </turbo:content>
        </item>
    </channel>
</rss>
'''
    )
