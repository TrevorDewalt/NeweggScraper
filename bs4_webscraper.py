from bs4 import BeautifulSoup
import requests
import re

search_term = input("What product do you want to search for today? ")

url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131"
# &N=4131 means will only search for products in stock
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

"""
To find how many pages of related products given above search_term:
Turn page_text output into string, split string to pull out number
of pages per related search term then cast as integer
"""
page_text = doc.find(class_="list-tool-pagination-text").strong
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

search_items_found = {}

for page in range(1, pages + 1):
    url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")

    # Use re.compile to match text that contains search_term--not exclusively search_term
    items = div.find_all(text=re.compile(search_term))
    for item in items:
        parent = item.parent
        if parent.name != "a":
            continue
        link = parent['href']
        parent2 = item.find_parent(class_="item-container")
        try:
            price = parent2.find(class_="price-current").strong.string
            search_items_found[item] = {"price": int(price.replace(",", "")), "link": link}
        except:
            pass

items_sorted = sorted(search_items_found.items(), key=lambda x: x[1]['price'])

for item in items_sorted:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print("----------break----------")
