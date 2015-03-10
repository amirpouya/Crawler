"""
Downloads all links from a specified location and saves to machine.
Downloaded links will only be of a lower level then links specified.
To use: python downloader.py http://uae.souq.com/ae-en/

"""
import sys,re,urllib2,urllib,urlparse,io
from BeautifulSoup import BeautifulSoup          # For processing HTML
import os
import io




def main():
    list_file=open("final.list.txt",'r')
    links=list_file.readlines()
    counter=0;
    for link in links:
        #print link,link2 ##print downloaded link
        file_name="ae_en\\"+str(counter)+".html"
        try:
            link2=link.replace('ae-en','ae-ar')
            print link,link2
            #urllib.urlretrieve(link, file_name)##download the link
            org_page=urllib2.urlopen(link)
            trg_page=urllib2.urlopen(link2)
            org_html=org_page.read()
            org_html=org_html.replace('item_tab_contents_wrapper ','')
            trg_html=trg_page.read()
            trg_html=trg_html.replace('item_tab_contents_wrapper ','')
            #targ_file=open(file_name,'w')
            outdir="output"
            text_extract(trg_html,org_html,outdir)
            #targ_file.write(str(targ_html))
            #targ_file.close()
        except   :
            print "could not download %s"%link


def text_extract(trg_html,org_html,outdir):
    trg_soup = BeautifulSoup(''.join(trg_html))
    org_soup = BeautifulSoup(''.join(org_html))

    trg_part={}
    org_part={}
    trg_title=trg_soup.findAll('h1',{'class':'item-title'})
    #print trg_title
    org_title=org_soup.findAll('h1',{'class':'item-title'})

    trg_desc=trg_soup.findAll('div',{'class':'itemDescription'})
    org_desc=org_soup.findAll('div',{'class':'itemDescription'})

    trg_part['itemDescription']=trg_desc
    org_part['itemDescription']=org_desc

    trg_desc=trg_soup.findAll('li',{'id':'Description'})
    org_desc=org_soup.findAll('li',{'id':'Description'})

    trg_part['Description']=trg_desc
    org_part['Description']=org_desc

    trg_desc=trg_soup.findAll('div',{'class':'item-desc'})
    org_desc=org_soup.findAll('div',{'class':'item-desc'})

    trg_part['item-desc']=trg_desc
    org_part['item-desc']=org_desc



    if len(trg_title)>0:
        print trg_title[0].text
        for item in trg_part.keys():
            if len(trg_part[item])>0:
                print item,trg_part[item][0].text
        print org_title[0].text
        for item in org_part.keys():
            if len(org_part[item])>0:
                print item,org_part[item][0].text




if __name__ == "__main__":
    main()