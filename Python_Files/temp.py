import requests, re
from bs4 import BeautifulSoup
site = 'https://www.eurookna.ru'
#url = 'https://www.eurookna.ru/balcony/plastikovye-balkon/'
author = 'eurookna.ru'
code = "cp1251"
noimage = '/local/templates/201907/images/banner_2020_small.jpg'
phone = '+7 (495) 137-06-32'

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

def get_small_seo_text_h2(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        small_seo_text_h2 = soup.find('section', class_='turbo-small-text').find('h2').text.strip()
    except:
        small_seo_text_h2 = ''
    return small_seo_text_h2

def get_small_seo_text(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        small_seo_text = soup.find('section', class_='turbo-small-text').find('h2').findNext('div').text.strip()
    except:
        small_seo_text = ''
    return small_seo_text

def if_empty_p(text):
     soup = BeautifulSoup(text, 'lxml')
     return re.sub(r'\s+', ' ', text.strip())


def get_seo_text(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        soup.find('div', class_='turbo-article').text.strip()
        seo_text = soup.find('div', class_='turbo-article')
    except:
        seo_text = ''
    return seo_text

def get_price(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        price = soup.find('p', class_='turbo-price').text.strip()
    except:
        price = ''
    return price

def get_advantages_h2(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        advantages_h2 = soup.find('section', class_='turbo-advantages').find('h2').text.strip()
    except:
        advantages_h2 = ''
    return advantages_h2

def get_advantages(html):
    soup = BeautifulSoup(html, 'lxml')
    advantages = []
    try:
        all = soup.findAll('div', attrs={"class": "turbo-advantages-item-head"})
        for i in range(len(all)):
            advantages.append([all[i].text.capitalize(), soup.findAll('p', attrs={"class" : "turbo-advantages-item-body"})[i].text])
    except:
        advantages = None
    return advantages

# Собираем данные

def parse(data):
    results = []
    soup = BeautifulSoup(data, 'lxml')

    h1 = get_head(data)[0]
    title = soup.title.string.strip()
    description = soup.findAll(attrs={"name":"description"})[0]['content'].strip()
    main_image_url = get_image(data)
    preview_text = if_empty_p(get_preview_text(data))
    small_seo_text_h2 = get_small_seo_text_h2(data)
    small_seo_text = if_empty_p(get_small_seo_text(data))
    seo_text = if_empty_p(str(get_seo_text(data)))
    price = if_empty_p(str(get_price(data)))
    advantages_h2 = if_empty_p(str(get_advantages_h2(data)))
    advantages = get_advantages(data)
    results.append({
        'title': title,
        'h1': h1,
        'description' : description,
        'main_image_url' : main_image_url,
        'preview_text' : preview_text,
        'small_seo_text_h2' : small_seo_text_h2,
        'small_seo_text' : small_seo_text,
        'seo_text' : seo_text,
        'price' : price,
        'advantages_h2' : advantages_h2,
        'advantages' : advantages
    })
    return results


with open('urls.txt', 'r') as input_file:
    urls = input_file.read().splitlines()

with open('temp.xml', 'w') as output_file:
    output_file.write(
'''
<?xml version="1.0" encoding="'''+ code + '''"?>
<rss xmlns:yandex="http://news.yandex.ru" 
     xmlns:media="http://search.yahoo.com/mrss/" 
     xmlns:turbo="http://turbo.yandex.ru" 
     version="2.0">
    <channel>  
'''
    )

for url in urls:
    data = get_html(url)
    a = parse(data)
    print(url)
    #print(get_advantages(data))
    # soup = BeautifulSoup(data, 'lxml')
    # print(soup.find('section', class_='turbo-advantages'))

    with open('temp.xml', 'a') as output_file:
        output_file.write(
'''     
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
                    </header>
                    <p>'''+ a[0]['preview_text'] +'''</p>
                    <p><big>'''+ a[0]['price'] +'''</big></p>
                    <button
                          formaction="tel:'''+ re.sub(r'\s+', '', phone) +'''"
                          data-background-color="red"
                          data-color="white"
                          data-turbo="false"
                          data-primary="true"
                        >
                        Заказать
                    </button>
                    <h2>'''+ a[0]['small_seo_text_h2'] +'''</h2>
                    <p>''' + a[0]['small_seo_text'] + '''</p>
                    '''+ a[0]['seo_text'] +'''
                    <button
                          formaction="tel:'''+ re.sub(r'\s+', '', phone) +'''"
                          data-background-color="red"
                          data-color="white"
                          data-turbo="false"
                          data-primary="true"
                        >
                        '''+ phone +
                        '''
                    </button>
                    <h2>'''+ a[0]['advantages_h2'] +'''</h2>'''
        )

    for adv in a[0]['advantages']:
        with open('temp.xml', 'a') as output_file:
            output_file.write(
'''
                    <h3>'''+ adv[0] +'''</h3>
                    <p>''' + adv[1] + '''</p>                    
'''
            )
    with open('temp.xml', 'a') as output_file:
        output_file.write(
                '''
                ]]>
            </turbo:content>
        </item>
'''
        )
with open('temp.xml', 'a') as output_file:
    output_file.write(
'''
    </channel>
</rss>
'''
    )