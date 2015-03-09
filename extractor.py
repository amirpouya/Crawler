"""
Downloads all links from a specified location and saves to machine.
Downloaded links will only be of a lower level then links specified.
To use: python downloader.py http://uae.souq.com/ae-en/

"""
import sys,re,urllib2,urllib,urlparse,io
from BeautifulSoup import BeautifulSoup          # For processing HTML
import os
#import nltk
import io
#import html2text




def main():
    list_file=open("list.txt",'r')
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
            targ_page=urllib2.urlopen(link2)
            org_html=org_page.read()
            targ_html=targ_page.read()
            targ_file=open(file_name,'w')
            outdir="output"
            text_extract(targ_html,org_html,outdir)
            #targ_file.write(str(targ_html))
            #targ_file.close()
        except KeyError :
            print "could not download %s"%link


def text_extract(trg_html,org_html,outdir):
    trg_soup = BeautifulSoup(''.join(trg_html))
    org_soup = BeautifulSoup(''.join(org_html))

    trg_title=trg_soup.findAll('h1',{'class':'item-title'})
    #print trg_title
    org_title=org_soup.findAll('h1',{'class':'item-title'})
    if len(trg_title)>0:
        print trg_title[0].text
        print org_title[0].text



if __name__ == "__main__":
    main()