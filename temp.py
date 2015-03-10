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
    link='http://uae.souq.com/ae-en/1000-words-and-pictures-by-terry-burton-2006-terry-burton-7285998/i/'
    #print link,link2 ##print downloaded link
    file_name="ae_en\\"+str(counter)+".html"
    try:
        #link2=link.replace('ae-en','ae-ar')
        org_page=urllib2.urlopen(link)
        #targ_page=urllib2.urlopen(link2)
        org_html=org_page.read()
        org_html=org_html.replace('item_tab_contents_wrapper ','')
        outdir="output"
        text_extract(org_html,outdir)
        #targ_file.write(str(targ_html))
        #targ_file.close()
    except   :
        print "could not download %s"%link


def text_extract(org_html,outdir):
    org_soup = BeautifulSoup(''.join(org_html))

    org_part={}
    #print trg_title
    org_title=org_soup.findAll('h1',{'class':'item-title'})

    org_desc=org_soup.findAll('div',{'class':'itemDescription'})
    org_part['itemDescription']=org_desc
    org_desc=org_soup.findAll('div',{'class':'item-desc'})[0].text
    print org_desc

    org_part['Description']=org_desc








if __name__ == "__main__":
    main()