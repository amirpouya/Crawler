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
    counter=0
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
            counter=text_extract(trg_html,link2,org_html,link,outdir,counter)
            #targ_file.write(str(targ_html))
            #targ_file.close()
        except   :
            print "could not download %s"%link


def text_extract(trg_html,trg_link,org_html,org_link,outdir,counter):

    trg_out=unicode('<doc url="'+trg_link.strip()+'">')
    org_out=unicode('<doc url="'+org_link.strip()+'">')



    trg_soup = BeautifulSoup(''.join(trg_html),convertEntities=BeautifulSoup.HTML_ENTITIES)
    org_soup = BeautifulSoup(''.join(org_html),convertEntities=BeautifulSoup.HTML_ENTITIES)

    trg_part={}
    org_part={}
    trg_title=trg_soup.findAll('h1',{'class':'item-title'})
    #print trg_title
    org_title=org_soup.findAll('h1',{'class':'item-title'})
    if len(trg_title)<1 or len(org_title)<1:
        return counter

    #Extracting and Generating XML docs

    #Title Part
    trg_out+=unicode("<title>"+trg_title[0].text+"</title>")
    org_out+=unicode("<title>"+org_title[0].text+"</title>")


    #Exetracting Diffrent type of Desc
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

    print trg_title[0].text
    for item in trg_part.keys():
        if len(trg_part[item])>0:
            trg_out+=unicode('<desc type="'+item+'">'+trg_part[item][0].text+"</desc>")
    print org_title[0].text
    for item in org_part.keys():
        if len(org_part[item])>0:
            org_out+=unicode('<desc type="'+item+'">'+org_part[item][0].text+"</desc>")
    trg_out+=unicode("</doc>")
    org_out+=unicode("</doc>")
    counter+=1;

    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not os.path.exists(outdir+"\\en"):
        os.makedirs(outdir+"\\en")
    if not os.path.exists(outdir+"\\ar"):
        os.makedirs(outdir+'\\ar')

    org_file=io.open(outdir+"\\en\\"+str(counter)+".en",'w',encoding='utf-8')
    trg_file=io.open(outdir+"\\ar\\"+str(counter)+".ar",'w',encoding='utf-8')

    org_file.write(org_out)
    trg_file.write(trg_out)
    org_file.close()
    trg_file.close()

    print "--------------------------"
    return counter




if __name__ == "__main__":
    main()