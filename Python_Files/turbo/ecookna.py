import requests, re
from bs4 import BeautifulSoup

site = 'https://www.ecookna.ru'
author = 'ecookna.ru'
code = "cp1251"
noimage = '/local/templates/ecookna/images/test1.jpeg'
phone = '+7 (495) 137-50-98'


def get_html(url):
    r = requests.get(url)  # Получаем метод Response
    r.encoding = 'utf-8'  # У меня были проблемы с кодировкой, я задал в ручную
    return r.text  # Вернем данные объекта text


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
    if soup.findAll('img', attrs={"class": "turbo-image"}) != []:
        image = soup.findAll('img', attrs={"class": "turbo-image"})
    elif soup.findAll('img', attrs={"class": "uk-cover"}) != []:
        image = soup.findAll('img', attrs={"class": "uk-cover"})
    else:
        image = [{'data-src': noimage}]
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
        small_seo_text_h2 = soup.find('div', class_='turbo-small-text').find('h2').text.strip()
    except:
        small_seo_text_h2 = ''
    return small_seo_text_h2


def get_small_seo_text(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        small_seo_text = soup.find('div', class_='turbo-small-text').find('h2').findNext('div').text.strip()
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
    all = soup.findAll('div', attrs={"class": "turbo-advantages-item-head"})
    if len(all) != 0:
        for i in range(len(all)):
            try:
                txt = soup.findAll('p', attrs={"class": "turbo-advantages-item-body"})[i].text
            except:
                txt = ''
            advantages.append([all[i].text.capitalize(), txt])
    else:
        advantages = None
    return advantages


def get_proizvodstvo_h2_text(html):
    soup = BeautifulSoup(html, 'lxml')
    proizvodstvo_h2_text = []
    try:
        proizvodstvo_h2_text = [soup.find('section', class_='turbo-proizvodstvo').find('h2').text.strip(),
                                soup.find('section', class_='turbo-proizvodstvo').find('h2').findNext('p').text.strip()]
    except:
        proizvodstvo_h2_text = ['', '']
    return proizvodstvo_h2_text


def get_proizvodstvo(html):
    soup = BeautifulSoup(html, 'lxml')
    proizvodstvo = []
    all_proizv = soup.findAll('div', attrs={"class": "turbo-proizvodstvo-item"})
    if len(all_proizv) != 0:
        for i in all_proizv:
            try:
                txt = i.find('p').text
            except:
                txt = ''
            proizvodstvo.append([i.find('h3').text, txt, i.find('img')['src']])
    else:
        proizvodstvo = []
    return proizvodstvo


def get_gallery_h2(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        soup.find('div', attrs={"id": "gallery-slideshow"})
        gallery_h2 = soup.find('div', attrs={"id": "gallery-slideshow"}).findPrevious('h2').text
    except:
        gallery_h2 = None
    return gallery_h2


def get_gallery(html):
    soup = BeautifulSoup(html, 'lxml')
    gallery = []
    try:
        photos = soup.find('div', attrs={"id": "gallery-slideshow"}).findAll('li')
        for i in photos:
            gallery.append(i.find('img')['data-src'])
    except:
        gallery = None
    return gallery


# Собираем данные

def parse(data):
    results = []
    soup = BeautifulSoup(data, 'lxml')

    h1 = get_head(data)[0]
    title = soup.title.string.strip()
    description = soup.findAll(attrs={"name": "description"})[0]['content'].strip()
    main_image_url = get_image(data)
    preview_text = if_empty_p(get_preview_text(data))
    small_seo_text_h2 = get_small_seo_text_h2(data)
    small_seo_text = if_empty_p(get_small_seo_text(data))
    seo_text = if_empty_p(str(get_seo_text(data)))
    price = if_empty_p(str(get_price(data)))
    proizvodstvo_h2_text = get_proizvodstvo_h2_text(data)
    proizvodstvo = get_proizvodstvo(data)
    advantages_h2 = if_empty_p(str(get_advantages_h2(data)))
    advantages = get_advantages(data)
    gallery_h2 = get_gallery_h2(data)
    gallery = get_gallery(data)
    results.append({
        'title': title,
        'h1': h1,
        'description': description,
        'main_image_url': main_image_url,
        'preview_text': preview_text,
        'small_seo_text_h2': small_seo_text_h2,
        'small_seo_text': small_seo_text,
        'seo_text': seo_text,
        'price': price,
        'advantages_h2': advantages_h2,
        'advantages': advantages,
        'proizvodstvo': proizvodstvo,
        'proizvodstvo_h2_text': proizvodstvo_h2_text,
        'gallery_h2': gallery_h2,
        'gallery': gallery
    })
    # print(results)
    return results


with open('../urls.txt', 'r') as input_file:
    urls = input_file.read().splitlines()

with open('../temp.xml', 'w') as output_file:
    output_file.write(  # записываем начало документа
        '''
        <?xml version="1.0" encoding="''' + code + '''"?>
<rss xmlns:yandex="http://news.yandex.ru" 
     xmlns:media="http://search.yahoo.com/mrss/" 
     xmlns:turbo="http://turbo.yandex.ru" 
     version="2.0">
    <channel>  
'''
    )
x = 0
for url in urls:  # зперечисляем все URL в списке
    data = get_html(url)
    a = parse(data)
    x += 1
    print(x, url)  # оставим для отображения процесса
    output_file = open('../temp.xml', 'a')
    output_file.write(  # записываем стандартное начало страницы
        '''     
        <item turbo="true">
            <link>''' + url + '''</link>
            <turbo:source>''' + url + '''</turbo:source>
            <turbo:topic>''' + a[0]['title'] + '''</turbo:topic>
            <author>''' + author + '''</author>
            <turbo:content>
                <![CDATA[
                    <header>
                        <h1>''' + a[0]['h1'] + '''</h1>
                        <figure>
                            <img src="''' + site + a[0]['main_image_url'][0] + '''" />
                        </figure>
                    </header>
'''
    )
    if a[0]['preview_text'] != '':
        output_file.write(  # если есть блок с данным текстом то выводим жтот текст
            '''            
                                <p>''' + a[0]['preview_text'] + '''</p>
'''
        )
    if a[0]['price'] != '':
        output_file.write(  # если указана цена то выводим
            '''            
                                <p><big>''' + a[0]['price'] + '''</big></p>
'''
        )

    if a[0]['small_seo_text_h2'] != '':
        output_file.write(  # если есть короткий сео-текст выводим
            '''            
                    <h2>''' + a[0]['small_seo_text_h2'] + '''</h2>
                    <p>''' + a[0]['small_seo_text'] + '''</p>
'''
        )
    output_file.write(  # всегда выводим эту кнопку
            '''        
                    <button
                          formaction="tel:''' + re.sub(r'\s+', '', phone) + '''"
                          data-background-color="red"
                          data-color="white"
                          data-turbo="false"
                          data-primary="true"
                        >
                        Заказать
                    </button>
    '''
    )
    if a[0]['seo_text'] != '':
        output_file.write(  # если есть сео-текст выводим вместе с кнопкой
            '''
                    ''' + a[0]['seo_text'] + '''
                    <button
                          formaction="tel:''' + re.sub(r'\s+', '', phone) + '''"
                          data-background-color="red"
                          data-color="white"
                          data-turbo="false"
                          data-primary="true"
                        >
                        ''' + phone +
            '''
                    </button>
'''
        )
    if a[0]['advantages'] != None:
        output_file.write(  # если есть преимущества выводим
            '''            
                                <h2>''' + a[0]['advantages_h2'] + '''</h2>
'''
        )
        for adv in a[0]['advantages']:
            output_file.write(  # перечисляем преимущества

                '''
                                    <h3>''' + if_empty_p(adv[0]).strip().capitalize() + '''</h3>
'''
            )
            if adv[1] != '':
                output_file.write(
                    '''                    
                                        <p>''' + if_empty_p(adv[1]).strip() + '''</p>                    
'''
                )
    if a[0]['proizvodstvo_h2_text'] != ['', '']:
        output_file.write(  # если есть блок про производство выводим
            '''
                                <h2>''' + if_empty_p(a[0]['proizvodstvo_h2_text'][0]).strip() + '''</h2>
                    <p>''' + if_empty_p(a[0]['proizvodstvo_h2_text'][1]).strip() + '''</p>
'''
        )
        for pr in a[0]['proizvodstvo']:
            output_file.write(  # перечисляем этапы производства
                '''
                                    <img src="''' + pr[2] + '''" alt="" />    
                    <h3>''' + if_empty_p(pr[0]).strip().capitalize() + '''</h3>
                    <p>''' + if_empty_p(pr[1]).strip() + '''</p>      

'''
            )
    if a[0]['gallery'] != None:
        output_file.write(  # Блок с галереей работ>
            '''
                                <h2>''' + a[0]['gallery_h2'] + '''</h2>
                    <div data-block="gallery">
'''
        )
        for img in a[0]['gallery']:
            output_file.write(  # Перечисляем фотографии
                '''
                                        <img src="''' + img + '''" />
'''
            )
        output_file.write(  # конец галереи
            '''        
                                    <header>''' + a[0]['gallery_h2'] + '''</header>
                    </div>
'''
        )
    output_file.write(  # статический блок с сертификатами
        '''
                 
                ]]>
            </turbo:content>
        </item>
        '''
    )

output_file.write(
    '''
    </channel>
</rss>
    '''
)
output_file.close()