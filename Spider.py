

import httplib2
import io
from BeautifulSoup import BeautifulSoup, SoupStrainer
import unique


#add any links to this array
def main():
    start_links=["http://uae.souq.com/ae-en/shop-all-categories/c/","http://uae.souq.com/ae-en/"]

    http = httplib2.Http()
    listlinks=[]
    for main_link in start_links:
        status, response = http.request(main_link)
        soup=BeautifulSoup(response)
        links =soup.findAll('a')
        #crawl category pages
        for link in links:
            l=link['href']
            pos=l.find('/c/')
            if pos != -1:
                listlinks.append( l[0:pos+3])
        #crawl list pages
        for link in links:
            l=link['href']
            pos=l.find('/l/')
            if pos != -1:
                listlinks.append( l[0:pos+3])
    print "Number of Main Page:",len(listlinks)
    counter=1
    itemlist=[]
    for listpage in listlinks:
        try:
            status, response = http.request(listpage)
            soup=BeautifulSoup(response)
            links =soup.findAll('a')
            print listpage
            for link in links:
                l=link['href']
                pos=l.find('/i/')
                if pos != -1 and l.find('ae-en')!=-1:
                    itemlist.append( l[0:pos+3])
            print counter,len(itemlist)
            counter+=1
        except :
            print "Error",listpage
    uniqlist=unique.unique(itemlist)
    out=io.open('link.list','w',encoding='utf-8')
    out.write('\n'.join(uniqlist))


if __name__=='__main__':
    main()


