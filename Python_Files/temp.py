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
  text = read_file(filename)
  tree = html.fromstring(text)

  phone_number = tree.xpath('//a[@class = "phone-call"]/text()')
  h1 = tree.xpath('//h1/text()')

  results.append({
    # 'movie_id': movie_id,
    # 'name_eng': name_eng,
    # 'date_watched': date_watched,
    # 'time_watched': time_watched,
    'h1': h1,
    'phone_number': phone_number
  })
  return results

print(parse('temp.html'))
