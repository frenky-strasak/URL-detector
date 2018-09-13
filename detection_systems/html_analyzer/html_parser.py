"""
Get text from html.
"""

import re
import urllib.request
from bs4 import BeautifulSoup

html = urllib.request.urlopen('http://' + 'www.seznam.cz')

"""
Read simple html instead of seznam.cz
"""
# with open('test_html.html') as f:
#     html = f.read()
# f.close()


soup = BeautifulSoup(html, features="lxml")

data = soup.findAll(text=True)
# print(data)

def visible(element):
    # if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
    if element.parent.name in ['style', 'script', '[document]', 'head']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


result = filter(visible, data)
#
print(list(result))
# print(result)
