from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import re

my_url = "https://www.yelp.com/search?cflt=restaurants&find_loc=San+Francisco%2C+CA"

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html,"html.parser")

containers = page_soup.findAll("div",{'class':'lemon--div__373c0__6Tkil searchResult__373c0__1yggB border-color--default__373c0__2oFDT'})
#print(len(containers))
# print(soup.prettify(containers[5]))

# container=containers[5]

filename = "output.csv"
f=open(filename,'w')

headers = "Name,Address,Phone_no,Website_url\n"
f.write(headers)

for container in containers:

    name1 = container.findAll("h3",{'class':'lemon--h3__373c0__5Q5tF heading--h3__373c0__1n4Of alternate__373c0__1uacp'})
    name2=name1[0].text
    name = name2[2:].strip()

    address1 = container.findAll("div",{'class':'lemon--div__373c0__6Tkil u-padding-t-half u-padding-l2 border-color--default__373c0__2oFDT text-align--right__373c0__3fmmn'})
    add = address1[0].text
    phno = add[:14]
    addr = add[14:]
    address = re.sub(r"(\w)([A-Z])", r"\1 \2", addr)
    # print(phno)
    # print(re.sub(r"(\w)([A-Z])", r"\1 \2", addr))

    url1 = "https://www.yelp.com" + container.h3.a['href']
    uClient1 = uReq(url1)
    page_html1=uClient1.read()
    uClient1.close()
    page_soup1=soup(page_html1,"html.parser")
    containers1=page_soup1.findAll("span",{'class':"biz-website js-biz-website js-add-url-tagging"})
    if not containers1:
        pass
    else:
        container1=containers1[0].text
        container11=container1[17:].strip()
        web_url="https://" + container11
        # print(web_url)
        f.write(name+","+address+","+phno+","+web_url+"\n")
        containers1=[]

f.close()
