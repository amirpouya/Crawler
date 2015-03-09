import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import seen
link="http://uae.souq.com/ae-en/shop-all-categories/c/"

http = httplib2.Http()
status, response = http.request(link)
soup=BeautifulSoup(response)
links =soup.findAll('a')
listlinks=[]
for link in links:
    l=link['href']
    pos=l.find('/l/')
    if pos != -1:
        listlinks.append( l[0:pos+3])
print "Number of Categor:",len(listlinks)
counter=1
for listpage in listlinks:
    try:
        status, response = http.request(listpage)
        soup=BeautifulSoup(response)
        links =soup.findAll('a')
        print listpage
        for link in links:
            l=link['href']
            pos=l.find('/i/')
            if pos != -1:
                listlinks.append( l[0:pos+3])
        print counter,len(listlinks)
        counter+=1
    except:
        pass
uniq=seen.f7(listlinks)
out=open('link.list','w')
out.write('\n'.join(uniq))

