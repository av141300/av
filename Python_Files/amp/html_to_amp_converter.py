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
    all = soup.findAll('div', attrs={"class": "turbo-advantages-item-head"})
    if len(all) != 0:
        for i in range(len(all)):
            try:
                txt = soup.findAll('p', attrs={"class" : "turbo-advantages-item-body"})[i].text
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
        proizvodstvo_h2_text = [soup.find('section', class_='turbo-proizvodstvo').find('h2').text.strip(), soup.find('section', class_='turbo-proizvodstvo').find('h2').findNext('p').text.strip()]
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
    description = soup.findAll(attrs={"name":"description"})[0]['content'].strip()
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
        'description' : description,
        'main_image_url' : main_image_url,
        'preview_text' : preview_text,
        'small_seo_text_h2' : small_seo_text_h2,
        'small_seo_text' : small_seo_text,
        'seo_text' : seo_text,
        'price' : price,
        'advantages_h2' : advantages_h2,
        'advantages' : advantages,
        'proizvodstvo' : proizvodstvo,
        'proizvodstvo_h2_text' : proizvodstvo_h2_text,
        'gallery_h2' : gallery_h2,
        'gallery' : gallery
    })
    for res in results:
        print(res)
    return results


with open('urls.txt', 'r') as input_file:
    urls = input_file.read().splitlines()

with open('temp.html', 'w') as output_file:
x = 0
for url in urls: # зперечисляем все URL в списке
    data = get_html(url)
    a = parse(data)
    x += 1
    print(x, url) # оставим для отображения процесса
    output_file = open('temp.xml', 'a')
    output_file.write(# записываем стандартное начало страницы
'''    
<!doctype html>
<html ⚡ lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">

    <link rel="canonical" href="/article.html">
    <link rel="shortcut icon" href="amp_favicon.png">

    <title>News Article</title>

    <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>
    <style amp-custom>
      body {
        width: auto;
        margin: 0;
        padding: 0;
      }

      header {
        background: Tomato;
        color: white;
        font-size: 2em;
        text-align: center;
      }

      h1 {
        margin: 0;
        padding: 0.5em;
        background: white;
        box-shadow: 0px 3px 5px grey;
      }

      p {
        padding: 0.5em;
        margin: 0.5em;
      }
    </style>
    <script async src="https://cdn.ampproject.org/v0.js"></script>
  </head>
  <body>
    <header>
      News Site
    </header>
    <article>
      <h1>Article Name</h1>

      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas tortor sapien, non tristique ligula accumsan eu.</p>

      <amp-img src="mountains.jpg" layout="responsive" width="266" height="150"></amp-img>
    </article>
  </body>
</html>
'''
)
output_file.close()