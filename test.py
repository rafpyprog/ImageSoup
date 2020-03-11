import requests
from bs4 import BeautifulSoup

user_agent = ('Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
                           '(KHTML, like Gecko) Chrome/41.0.2228.0 '
                           'Safari/537.36')
QUERY = 'python'
url = f'https://www.google.com/search?tbm=isch&ijn=0&q={QUERY}'
print(url)

r = requests.get(url, headers={'User-Agent': user_agent})
r.raise_for_status()
r.text

soup = BeautifulSoup(r.text, 'html.parser')

attrs = {"data-id": True, "jsname": True}
results = soup.find('div', attrs)
data_id = results['data-id']

for i in soup.find_all('script'):
    if data_id in str(i):
        script = i

import re
js = re.search('(?<=data:).*', script.text, re.DOTALL).group()[:-3]

import js2py
r = js2py.eval_js(js)
data = r()

data = data.to_list()

data = [i for i in data if isinstance(i, list)]


rdata = [i for i in data[3][0] if isinstance(i, list)][0][2]
print(len(rdata))
print(data_id)
print('RDATA:')
for n, i in enumerate(rdata):
    print(n, i)
    print('\n')







