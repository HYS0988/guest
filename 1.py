import requests
from lxml import etree

url = 'https://s.weibo.com/top/summary?cate=realtimehot'
r = requests.get(url)
print('r的内容{}'.format(r.content))
html = etree.HTML(r.text)
print(html)
nodes = html.xpath("//div[@class='data']/table/tbody/tr")
print('{:2}   {:7}   {}'.format('序号', '搜索次数', '热搜内容'))
for node in nodes[1:]:
    hot_paiming = node.xpath('./td[1]/text()')[0]
    hot_name = node.xpath('./td[2]/a/text()')[0]
    hot_search_nums = node.xpath('./td[2]/span/text()')[0]
    print('{:2}   {:7}   {}'.format(hot_paiming, hot_search_nums, hot_name))
