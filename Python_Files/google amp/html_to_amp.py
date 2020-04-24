import requests, re, os
from bs4 import BeautifulSoup

site = 'https://www.eurookna.ru'
# url = 'https://www.eurookna.ru/balcony/plastikovye-balkon/'
author = 'eurookna.ru'
code = "cp1251"
noimage = '/local/templates/201907/images/banner_2020_small.jpg'
phone = '+7 (495) 137-06-32'


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
    return results


with open('urls.txt', 'r') as input_file:
    urls = input_file.read().splitlines()

x = 0
for url in urls:  # зперечисляем все URL в списке
    data = get_html(url)
    a = parse(data)
    x += 1
    print(x, url)  # оставим для отображения процесса
    path = 'amp/' + url.replace(site, '')
    try:
        os.makedirs(path)
    except OSError:
        print("Создать директорию %s не удалось" % path)
    else:
        print("Успешно создана директория %s" % path)
    output_file = open(path + '/index.html', 'w', encoding="utf-8")
    output_file.write( '''<!doctype html>
<html ⚡ lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
        <link rel="canonical" href="'''+ url +'''">
        <link rel= "shortcut icon" href= "amp_favicon.png">
        <title>'''+  a[0]['title'] + '''</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;900&display=swap" rel="stylesheet">
        <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>
        <style amp-custom>
        html {
              line-height: 1.15;
              -webkit-text-size-adjust: 100%;
            }
            body {
              margin: 0;
            }
            main {
              display: block;
            }
            h1 {
              font-size: 2em;
              margin: 0.67em 0;
            }
            hr {
              -webkit-box-sizing: content-box;
              box-sizing: content-box;
              height: 0;
              overflow: visible;
            }
            pre {
              font-family: monospace, monospace;
              font-size: 1em;
            }
            a {
              background-color: transparent;
            }
            abbr[title] {
              border-bottom: none;
              text-decoration: underline;
              -webkit-text-decoration: underline dotted;
              text-decoration: underline dotted;
            }
            b,
            strong {
              font-weight: bolder;
            }
            code,
            kbd,
            samp {
              font-family: monospace, monospace;
              font-size: 1em;
            }
            small {
              font-size: 80%;
            }
            sub,
            sup {
              font-size: 75%;
              line-height: 0;
              position: relative;
              vertical-align: baseline;
            }
            sub {
              bottom: -0.25em;
            }
            sup {
              top: -0.5em;
            }
            img {
              border-style: none;
            }
            button,
            input,
            optgroup,
            select,
            textarea {
              font-family: inherit;
              font-size: 100%;
              line-height: 1.15;
              margin: 0;
            }
            button,
            input {
              overflow: visible;
            }
            button,
            select {
              text-transform: none;
            }
            button,
            [type="button"],
            [type="reset"],
            [type="submit"] {
              -webkit-appearance: button;
            }
            button::-moz-focus-inner,
            [type="button"]::-moz-focus-inner,
            [type="reset"]::-moz-focus-inner,
            [type="submit"]::-moz-focus-inner {
              border-style: none;
              padding: 0;
            }
            button:-moz-focusring,
            [type="button"]:-moz-focusring,
            [type="reset"]:-moz-focusring,
            [type="submit"]:-moz-focusring {
              outline: 1px dotted ButtonText;
            }
            fieldset {
              padding: 0.35em 0.75em 0.625em;
            }
            legend {
              -webkit-box-sizing: border-box;
              box-sizing: border-box;
              color: inherit;
              display: table;
              max-width: 100%;
              padding: 0;
              white-space: normal;
            }
            progress {
              vertical-align: baseline;
            }
            textarea {
              overflow: auto;
            }
            [type="checkbox"],
            [type="radio"] {
              -webkit-box-sizing: border-box;
              box-sizing: border-box;
              padding: 0;
            }
            [type="number"]::-webkit-inner-spin-button,
            [type="number"]::-webkit-outer-spin-button {
              height: auto;
            }
            [type="search"] {
              -webkit-appearance: textfield;
              outline-offset: -2px;
            }
            [type="search"]::-webkit-search-decoration {
              -webkit-appearance: none;
            }
            ::-webkit-file-upload-button {
              -webkit-appearance: button;
              font: inherit;
            }
            details {
              display: block;
            }
            summary {
              display: list-item;
            }
            template {
              display: none;
            }
            [hidden] {
              display: none;
            }
            .button {
              cursor: pointer;
              background-color: #ed1c24;
              color: #fff;
              margin: 0;
              border: none;
              border-radius: 0;
              display: inline-block;
              -webkit-box-sizing: border-box;
              box-sizing: border-box;
              padding: 0 30px;
              vertical-align: middle;
              font-size: 16px;
              line-height: 46px;
              text-align: center;
              text-decoration: none;
              text-transform: uppercase;
              -webkit-transition: 0.1s ease-in-out;
              -o-transition: 0.1s ease-in-out;
              transition: 0.1s ease-in-out;
              -webkit-transition-property: color, background-color, border-color;
              -o-transition-property: color, background-color, border-color;
              transition-property: color, background-color, border-color;
            }
            .button:hover,
            .button:focus {
              background-color: #de1219;
              color: #fff;
            }
            .button--nav {
              background-color: transparent;
              color: #211d70;
              border: 2px solid #211d70;
            }
            .button--nav:hover,
            .button--nav:focus {
              background-color: #1b185c;
              color: #fff;
              border-color: #1b185c;
            }
            .section {
              padding: 20px 0;
            }
            @media (min-width: 960px) {
              .section {
                padding: 40px 0;
              }
            }
            .section--nopd {
              padding: 0;
            }
            .section--about {
              background: url(../img/manufacture.jpg) center top no-repeat;
              background-size: cover;
              padding-left: 15px;
              padding-right: 15px;
              color: #fff;
            }
            .section--discount {
              background-color: #ffe650;
              padding-left: 15px;
              padding-right: 15px;
            }
            .section--points {
              background: url(../img/bg-points.jpg) center top no-repeat;
              background-size: cover;
              padding-left: 15px;
              padding-right: 15px;
              padding-bottom: 25px;
              color: #fff;
            }
            @media (min-width: 960px) {
              .section--points {
                padding-bottom: 55px;
              }
            }
            .section--footer {
              background-color: #f3f3f3;
            }
            .container {
              padding-left: 15px;
              padding-right: 15px;
              max-width: 960px;
              -webkit-box-sizing: border-box;
              box-sizing: border-box;
              margin: 0 auto;
              position: relative;
            }
            input {
              height: 50px;
              vertical-align: middle;
              display: inline-block;
              -webkit-box-sizing: border-box;
              box-sizing: border-box;
              margin: 0;
              border-radius: 0;
              font: inherit;
              overflow: visible;
              outline: none;
              max-width: 100%;
              width: 100%;
              border: 0 none;
              padding: 0 10px;
              background: #fff;
              color: #01090f;
              -webkit-transition: 0.2s ease-in-out;
              -o-transition: 0.2s ease-in-out;
              transition: 0.2s ease-in-out;
              -webkit-transition-property: color, background-color, border;
              -o-transition-property: color, background-color, border;
              transition-property: color, background-color, border;
            }
            .row {
              margin-left: -15px;
              margin-right: -15px;
              letter-spacing: -0.36em;
            }
            .col {
              letter-spacing: normal;
              display: inline-block;
              vertical-align: top;
              width: calc(100% - 30px);
              padding-left: 15px;
              padding-right: 15px;
            }
            .col--vam {
              vertical-align: middle;
            }
            .col--2 {
              width: calc(100% / 2 - 30px);
            }
            .col--3 {
              width: calc(100% / 3 - 30px);
            }
            @media (min-width: 640px) {
              .col--s2 {
                width: calc(100% / 2 - 30px);
              }
              .col--s3 {
                width: calc(100% / 3 - 30px);
              }
            }
            html {
              font-family: Roboto, Arial, sans-serif;
              font-size: 16px;
              font-weight: 400;
              line-height: 1.6;
              background: #fff;
              color: #01090f;
            }
            a {
              color: #211d70;
            }
            img {
              display: block;
              max-width: 100%;
            }
            h1 {
              font-size: 1.9125rem;
              margin: 20px 0 20px 0;
              font-weight: 900;
              line-height: 1.2;
              color: #111;
              text-transform: uppercase;
            }
            h2 {
              font-size: 1.25rem;
              margin: 20px 0 20px 0;
              font-weight: 900;
              line-height: 1.4;
              color: #111;
            }
            address,
            dl,
            fieldset,
            figure,
            ol,
            p,
            pre,
            ul {
              margin: 0 0 20px 0;
            }
            #nav {
              position: fixed;
              top: 0;
              height: 100%;
              width: 80%;
              max-width: 400px;
              z-index: 10;
              background-color: #f3f3f3;
              text-align: center;
              -webkit-box-shadow: 0 10px 7px 1px rgba(0, 0, 0, 0.22);
              box-shadow: 0 10px 7px 1px rgba(0, 0, 0, 0.22);
            }
            #nav:not(:target) {
              left: -100%;
              -webkit-transition: left 1.5s;
              -o-transition: left 1.5s;
              transition: left 1.5s;
            }
            #nav:target {
              left: 0;
              -webkit-transition: left 1s;
              -o-transition: left 1s;
              transition: left 1s;
            }
            .nav__close {
              text-align: right;
              margin-top: 15px;
            }
            .nav__logo {
              padding: 30px 15px 15px;
              background-color: #ffe650;
              display: inline-block;
              margin-top: -40px;
            }
            .nav__age {
              text-transform: uppercase;
              color: #211d70;
              font-size: 1.25rem;
              line-height: 1.5;
              margin-top: 15px;
            }
            .nav__age span {
              font-size: 1.625rem;
              font-weight: 700;
              color: #ed1c24;
            }
            .nav__phone {
              font-size: 1.5rem;
              text-decoration: none;
            }
            .nav__phone a {
              font-size: 1.5rem;
              text-decoration: none;
              color: inherit;
            }
            .nav__phone span {
              color: #211d70;
            }
            .nav__phone i {
              color: #575c63;
              font-size: 0.875rem;
              font-style: normal;
              display: block;
            }
            .nav__links a {
              font-size: 1.25rem;
              color: #575c63;
              text-decoration: none;
            }
            .nav__links a:focus,
            .nav__links a:hover {
              color: #01090f;
            }
            .logo {
              text-align: center;
            }
            .logo__inner {
              padding: 15px;
              background-color: #ffe650;
              display: inline-block;
            }
            .phone {
              text-align: right;
            }
            .about,
            .logo {
              text-align: center;
            }
            .banner__text,
            .about__text {
              color: #575c63;
            }
            .about h2 {
              margin-top: 0;
            }
            .about__block {
              background: rgba(255, 255, 255, 0.8);
              padding: 15px;
              max-width: 450px;
              margin: 0 auto;
            }
            .about__text {
              margin-bottom: 0;
              text-align: left;
            }
            .steps h2 {
              margin-top: 0;
            }
            .steps h3:last-child {
              margin-bottom: 0;
            }
            .discount__head {
              font-size: 1.25rem;
              line-height: 1.4;
              text-transform: uppercase;
              text-align: center;
              font-weight: 900;
              color: #111;
            }
            .discount__form {
              max-width: 450px;
              margin: 0 auto;
            }
            .discount__phone {
              position: relative;
              padding-left: 50px;
              margin-bottom: 20px;
            }
            .discount__phone span {
              position: absolute;
              top: 0;
              bottom: 0;
              left: 0;
              width: 50px;
              z-index: 1;
              background-color: #fff;
              color: #575c63;
              padding: 15px;
              -webkit-box-sizing: border-box;
              box-sizing: border-box;
            }
            .discount__btn input {
              cursor: pointer;
            }
            .discount__btn input[value] {
              text-transform: uppercase;
              background-color: #ed1c24;
              color: #fff;
            }
            .discount__btn input[value]:hover,
            .discount__btn input[value]:focus {
              background-color: #de1219;
            }
            .discount__check {
              margin-top: 20px;
            }
            .discount__label {
              cursor: pointer;
              font-size: 0.875rem;
              line-height: 1.5;
              text-align: left;
            }
            .discount__check input {
              width: 17px;
              height: 17px;
              margin-right: 5px;
            }
            .points h2 {
              color: #fff;
              margin-top: 0;
            }
            .points__header {
              -webkit-box-sizing: border-box;
              box-sizing: border-box;
              text-transform: uppercase;
              margin-bottom: 20px;
              display: table;
            }
            .points__header i {
              font-style: normal;
              display: table-cell;
              vertical-align: middle;
            }
            .points__header span {
              margin-right: 15px;
            }
            .sert {
              padding-bottom: 20px;
            }
            @media (min-width: 960px) {
              .sert {
                padding-bottom: 50px;
              }
            }
            .sert h2 {
              margin-top: 0;
            }
            .sert p {
              margin: 20px 0 20px 0;
              color: #575c63;
            }
            .map .section {
              background-color: #ffe650;
            }
            .map__info {
              max-width: 450px;
              margin: 0 auto;
              text-align: center;
            }
            .map__head {
              font-size: 1.25rem;
              line-height: 1.4;
              text-transform: uppercase;
              text-align: center;
              font-weight: 900;
              color: #111;
            }
            .map .button {
              display: block;
            }
            .footer h3 {
              margin: 0 0 20px 0;
            }
            .footer ul {
              padding-left: 0;
            }
            .footer li {
              list-style-type: none;
            }
            .footer a {
              text-decoration: none;
              color: #575c63;
              padding: 5px 0;
              display: block;
            }
            .footer a:hover,
            .footer a:focus {
              color: #01090f;
            }
            .footer__list a {
              font-weight: 700;
            }
            a.footer__phone {
              color: #01090f;
              text-transform: uppercase;
              font-weight: 700;
            }
            .footer__phone:hover {
              color: #01090f;
            }
            a.footer__phone span {
              color: #211d70;
            }
            .footer__socials a,
            .footer__pay a {
              display: inline-block;
              vertical-align: middle;
            }
            .footer .footer__btn {
              text-transform: uppercase;
              color: #ed1c24;
              font-size: 0.875rem;
              line-height: 1.5;
              font-weight: 700;
            }
            .footer .footer__btn:hover,
            .footer .footer__btn:focus {
              color: #ed1c24;
              text-decoration: underline;
            }
            .note {
              color: #575c63;
              font-size: 0.875rem;
              line-height: 1.5;
              margin-bottom: 0;
            }
            .p__price {
              font-size: 1.25rem;
              font-weight:bold;
              line-height: 1.5;
              color: #211d70;
            }
	    </style>
        <script async src= "https://cdn.ampproject.org/v0.js"></script>
    </head>
    <body>
        <div id="nav">
            <div class="container">
                <div class="nav__close">
                    <a href="##">
                        <svg width="14" height="14" viewBox="0 0 14 14" xmlns="http://www.w3.org/2000/svg" data-svg="close-icon">
                            <line fill="none" stroke="#000" stroke-width="1.1" x1="1" y1="1" x2="13" y2="13"></line>
                            <line fill="none" stroke="#000" stroke-width="1.1" x1="13" y1="1" x2="1" y2="13"></line>
                        </svg>
                    </a>
                </div>
                <div class="nav__logo">
                    <a href="/">
                        <img width="80" src="https://www.eurookna.ru/local/templates/201907/images/eurookna-logo.svg">
                    </a>
                </div>
                <p class="nav__age">Нам <span>24</span> года</p>
                <p><a class="button button--nav" href="">Заказать звонок</a></p>
                <p><a class="button button--nav" href="">Вызвать замерщика</a></p>
                <p class="nav__phone"><a href="tel:''' + re.sub(r'\s+', '', phone) + '''">''' + re.sub(r'\s+', '', phone) + '''</span></a><i>прием заявок круглосуточно</i></p>
                <p class="nav__links">
                    <a href="https://www.eurookna.ru/">Пластиковые окна</a><br>
                    <a href="https://www.eurookna.ru/balcony/">Балконы и лоджии</a><br>
                    <a href="https://www.eurookna.ru/derevyannye-okna/">Деревянные окна</a><br>
                    <a href="https://www.eurookna.ru/teplyy-alyuminiy/">Теплый алюминий</a><br>
                    <a href="https://www.eurookna.ru/calculation/#calcform">Рассчитать стоимость</a><br>
                    <a href="https://www.eurookna.ru/okna/plastikovye-zavod/#contact">Контакты</a>
                </p>
            </div>
        </div>
        <header>
            <div class="header">
                <div class="container">
                    <div class="row">
                        <div class="col col--3 col--vam">
                            <div class="menu">
                                <a href="#nav">
                                    <svg width="20" height="20" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" data-svg="navbar-toggle-icon">
                                        <rect y="9" width="20" height="2"></rect>
                                        <rect y="3" width="20" height="2"></rect>
                                        <rect y="15" width="20" height="2"></rect>
                                    </svg>
                                </a>
                            </div>
                        </div>
                        <div class="col col--3 col--vam">
                            <div class="logo">
                                <div class="logo__inner">
                                    <a href="/">
                                        <img width="55" src="https://www.eurookna.ru/local/templates/201907/images/eurookna-logo.svg">
                                    </a>
                                </div>
                            </div>
                        </div>
                        <div class="col col--3 col--vam">
                            <div class="phone">
                                <a href="tel:''' + re.sub(r'\s+', '', phone) + '''">
                                    <svg width="21.6" height="21.6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" data-svg="eo-phone-3">
                                        <path d="M18.48 22.926L17.2869 23.584C10.307 27.204 -1.79503 6.09 5.00698 2.1L6.15298 1.463L9.86698 7.93L8.72698 8.562C6.66097 9.807 11.487 18.269 13.607 17.107L14.769 16.465L18.479 22.925L18.48 22.926ZM8.67197 0L6.99197 0.975L10.706 7.441L12.386 6.467L8.67298 0H8.67197ZM17.285 14.997L15.605 15.972L19.319 22.439L20.999 21.463L17.2839 14.996L17.285 14.997Z" fill="#000"></path>
                                    </svg>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </header>   
        <article>          
            <div class="section banner">
                <div class="container">
                    <amp-img src="''' + site + a[0]['main_image_url'][0] + '''" layout="responsive" width="266" height="150"></amp-img>
                    <h1>''' + a[0]['h1'] + '''</h1>
                    '''
    )
    if a[0]['preview_text'] != '':
        output_file.write(  # если есть блок с данным текстом то выводим жтот текст
                    '''<p>''' + a[0]['preview_text'] + '''</p>
                    '''
        )

    if a[0]['price'] != '':
        output_file.write(  # если указана цена то выводим
                    '''<p class="p__price">''' + a[0]['price'] + '''</p>'''
        )

    output_file.write(
    '''
                    <a class="button" href="tel:''' + re.sub(r'\s+', '', phone) + '''">Заказать</a>'''
    )
    output_file.write(
    '''      
                </div>
            </div>
        </article>
        <div class="section steps">
            <div class="container">
                <h2>''' + a[0]['small_seo_text_h2'] + '''</h2>
                <p>''' + a[0]['small_seo_text'] + '''</p>
                '''
    )
    if a[0]['seo_text'] != '':
        output_file.write(  # если есть сео-текст выводим
            a[0]['seo_text']
        )
    if a[0]['advantages'] != None:
        output_file.write(  # если есть преимущества выводим
            '''<h2>''' + a[0]['advantages_h2'] + '''</h2>
            '''
        )
        for adv in a[0]['advantages']:
            output_file.write(  # перечисляем преимущества
            '''<h3>''' + if_empty_p(adv[0]).strip().capitalize() + '''</h3>
            '''
            )
            if adv[1] != '':
                output_file.write(
                '''<p>''' + if_empty_p(adv[1]).strip() + '''</p>
                '''
                )
    output_file.write(
    '''
            </div>
        </div>
        <div class="section sert">
            <div class="container">
                <h2>Дипломы и сертификаты</h2>
                <div class="row">
                    <div class="col col--2 col--s3">
                        <img src="https://www.eurookna.ru/upload/medialibrary/8f6/8f6c4a7200a078934dcde2c4275bd04e.jpg" alt="Премия «Золотое окно 2018»">
                        <p>Премия «Золотое окно 2018»</p>
                    </div>
                    <div class="col col--2 col--s3">
                        <img src="https://www.eurookna.ru/upload/medialibrary/92a/92a9446f9e715599a6da33c76e4e8e87.jpg" alt="Сертификат VEKA">
                        <p>Сертификат VEKA</p>
                    </div>
                    <div class="col col--2 col--s3">
                        <img src="https://www.eurookna.ru/upload/medialibrary/ad4/ad46ff3cc64f997214dc3edd8cc6c994.jpg" alt="Премия «Золотое окно 2016»">
                        <p>Премия «Золотое окно 2016» asdf asdf asdf asdfsd</p>
                    </div>
                    <div class="col col--2 col--s3">
                        <img src="https://www.eurookna.ru/upload/medialibrary/213/213fd72919cac2de5a7b3dc5298d244d.jpg" alt="Свидетельство от МФЗП лауреату «Лучшие в Москве»">
                        <p>Свидетельство от МФЗП лауреату «Лучшие в Москве»</p>
                    </div>
                    <div class="col col--2 col--s3">
                        <img src="https://www.eurookna.ru/upload/medialibrary/d3d/d3dafa43d3f0661d10072f159421b817.jpg" alt="Премия «Золотое окно 2014»">
                        <p>Премия «Золотое окно 2014»</p>
                    </div>
                    <div class="col col--2 col--s3">
                        <img src="https://www.eurookna.ru/upload/medialibrary/4f5/4f56adb7ab8d8d9e4a4b2345943dd8b5.jpg" alt="Свидетельство от МФЗП лауреату «Лучшие в Москве»">
                        <p>Свидетельство от МФЗП лауреату «Лучшие в Москве»</p>
                    </div>
                </div>
            </div>
        </div> 
        <div class="container map">
            <img src="img/map.jpg" alt="">
            <div class="section">
                <div class="container">
                    <div class="map__info">
                        <p class="map__head">Адрес центрального офиса продаж:</p>
                        <p class="map__text">127006, г. Москва, м. Новослободская, <br> ул. Долгоруковская, д. 21, стр. 1, этаж 3, офис 303, <br> тел.: +7 495 725-60-65 (круглосуточно).</p>
                        <p><a href="" class="button">Схема проезда</a></p>
                        <p><a href="" class="button">Задать вопрос</a></p>
                    </div>
                </div>
            </div>
        </div>
        <div class="footer">
            <div class="container">
                <div class="section section--footer">
                    <div class="container">
                        <div class="row">
                            <div class="col col--s3">
                                <p class="footer__socials">
                                    <a href="https://www.facebook.com/EuroOknaMoscow" target="_blank">
                                        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" data-svg="eo-facebook-2">
                                            <path d="M0 0V24H24V0H0ZM16 7H14.077C13.461 7 13 7.252 13 7.889V9H16L15.761 12H13V20H10V12H8V9H10V7.077C10 5.055 11.064 4 13.461 4H16V7Z" fill="#4267B2"></path>
                                        </svg>
                                    </a>
                                    <a href="https://vk.com/eurooknaru" target="_blank">
                                        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" data-svg="eo-vk-2">
                                            <path d="M0 0V24H24V0H0ZM19.25 16.996H17.117C15.912 16.996 15.707 16.309 14.715 15.317C13.818 14.42 13.321 15.108 13.341 16.385C13.347 16.724 13.18 16.996 12.775 16.996C11.511 16.996 9.695 17.174 7.857 15.19C5.974 13.157 4 9.079 4 8.677C4 8.44 4.196 8.333 4.524 8.333H6.694C7.268 8.333 7.317 8.617 7.477 8.982C8.144 10.503 9.742 13.556 10.167 11.852C10.411 10.874 10.511 8.607 9.464 8.412C8.87 8.302 9.916 7.666 11.432 7.666C11.809 7.666 12.218 7.707 12.637 7.803C13.406 7.982 13.408 8.326 13.398 8.829C13.359 10.732 13.129 12.013 13.631 12.336C14.11 12.646 15.37 10.619 16.034 9.055C16.217 8.622 16.254 8.333 16.769 8.333H19.424C20.813 8.333 19.242 10.33 18.041 11.89C17.073 13.145 17.125 13.17 18.249 14.214C19.051 14.958 19.999 15.974 19.999 16.55C20 16.822 19.788 16.996 19.25 16.996Z" fill="#659AD0"></path>
                                        </svg>
                                    </a>
                                    <a href="https://www.youtube.com/user/EuroOkna" target="_blank">
                                        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" data-svg="eo-vk-2">
                                            <path d="M0 0V24H24V0H0ZM19.25 16.996H17.117C15.912 16.996 15.707 16.309 14.715 15.317C13.818 14.42 13.321 15.108 13.341 16.385C13.347 16.724 13.18 16.996 12.775 16.996C11.511 16.996 9.695 17.174 7.857 15.19C5.974 13.157 4 9.079 4 8.677C4 8.44 4.196 8.333 4.524 8.333H6.694C7.268 8.333 7.317 8.617 7.477 8.982C8.144 10.503 9.742 13.556 10.167 11.852C10.411 10.874 10.511 8.607 9.464 8.412C8.87 8.302 9.916 7.666 11.432 7.666C11.809 7.666 12.218 7.707 12.637 7.803C13.406 7.982 13.408 8.326 13.398 8.829C13.359 10.732 13.129 12.013 13.631 12.336C14.11 12.646 15.37 10.619 16.034 9.055C16.217 8.622 16.254 8.333 16.769 8.333H19.424C20.813 8.333 19.242 10.33 18.041 11.89C17.073 13.145 17.125 13.17 18.249 14.214C19.051 14.958 19.999 15.974 19.999 16.55C20 16.822 19.788 16.996 19.25 16.996Z" fill="#FF0000"></path>
                                        </svg>
                                    </a>
                                </p>
                                <p>
                                    <a class="footer__phone" href="tel:''' + re.sub(r'\s+', '', phone) + '''">''' + re.sub(r'\s+', '', phone) + '''</span></a>
                                    <a class="footer__btn" href="">Заказать звонок</a>
                                </p>
                                <p>127006, г. Москва, <br> м. Новослободская, <br> ул. Долгоруковская, д. 21, <br> стр. 1, этаж 3, офис 303.</p>
                            </div>
                            <div class="col col--s3">
                                <ul class="footer__list">
                                    <li><a href="https://www.eurookna.ru/">Пластиковые окна</a></li>
                                    <li><a href="https://www.eurookna.ru/balcony/">Остекление балкона</a></li>
                                    <li><a href="https://www.eurookna.ru/derevyannye-okna/">Деревянные окна</a></li>
                                    <li><a href="https://www.eurookna.ru/teplyy-alyuminiy/">Теплый алюминий</a></li>
                                    <li><a href="https://www.eurookna.ru/calculation/">Калькулятор окон</a></li>
                                    <li><a href="https://www.eurookna.ru/about/">О компании</a></li>
                                    <li><a href="https://www.eurookna.ru/sotrudnichestvo/">Сотрудничество</a></li>
                                    <li><a href="https://www.eurookna.ru/vakansii/">Вакансии</a></li>
                                </ul>
                            </div>
                            <div class="col col--s3">
                                <h3>Принимаем к оплате</h3>
                                <p class="footer__pay">
                                    <a>
                                        <img width="35" src="https://www.eurookna.ru/local/templates/201907/images/mastercard.svg" alt="mastercard">
                                    </a>
                                    <a>
                                        <img width="35" src="https://www.eurookna.ru/local/templates/201907/images/visacard.svg" alt="visacard">
                                    </a>
                                    <a>
                                        <img width="35" src="https://www.eurookna.ru/local/templates/201907/images/jcbcard.svg" alt="jcbcard">
                                    </a>
                                    <a>
                                        <img width="35" src="https://www.eurookna.ru/local/templates/201907/images/mircard.svg" alt="mircard">
                                    </a>
                                    <a href="https://halvacard.ru/shops/stroitelnye-materialy/EvroOkna">
                                        <img width="35" src="https://www.eurookna.ru/local/templates/201907/images/halvacard.svg" alt="halvacard">
                                    </a>
                                </p>
                                <a class="footer__btn" href="https://www.eurookna.ru/cabinet_sb/">Оплатить заказ</a>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col">
                                <p class="note">ВНИМАНИЕ! Наш интернет-ресурс носит исключительно информационный характер и не является публичной офертой, определяемой положениями Статьи 437(2) ГК РФ. <br>
                                © 1995 — 2019 ООО «ЕвроОкна». ИНН/КПП - 5042143994/504201001, ОГРН - 1175007002280, Р/ЧС - ПАО СБЕРБАНК 40702810040000021321 | Политика конфиденциальности</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>       
    </body>
</html>'''
    )
output_file.close()