#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#usage: python extractor.py -i<listfile> -o<outdir>
# or
# python extractor.py


import urllib2 # For extracting site pages
from BeautifulSoup import BeautifulSoup          # For processing HTML
import os #For Creating Dir
import io #For opening file in UTF8
import sys,getopt


def main(argv):
    fcounter=0
    list_address='final.list.txt'
    output_dir='output'

    try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","odir="])
    except getopt.GetoptError:
      print 'test.py -i <listfile> -o <outputdir>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print 'extractor.py -i <inputfile> -o <outputdir>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         list_address = arg
      elif opt in ("-o", "--odir"):
         output_dir = arg

    try:
        list_file=open(list_address,'r')
    except :
        print 'No such file or directory:',list_address
        exit(-1)
    print 'Reading Link List'
    links=list_file.readlines()
    counter=1;
    all_file_count=len(links)
    print "Start Downloading Pages..."
    for link in links:
        fcounter+=1
        try:
            link2=link.replace('ae-en','ae-ar')
            print link,link2
            org_page=urllib2.urlopen(link)
            trg_page=urllib2.urlopen(link2)

            org_html=org_page.read().decode('utf-8','ignore')
            org_html=org_html.replace('item_tab_contents_wrapper ','')
            trg_html=trg_page.read().decode('utf-8','ignore')
            trg_html=trg_html.replace('item_tab_contents_wrapper ','')
            outdir=output_dir
            counter=text_extract(trg_html,link2,org_html,link,outdir,counter)
            print fcounter,'/',all_file_count,":",counter
        except   :
            print "could not download %s"%link


def text_extract(trg_html,trg_link,org_html,org_link,out_dir,counter):
    ok=False
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
    trg_out+=unicode("\n<title>"+trg_title[0].text.strip()+"</title>\n")
    org_out+=unicode("\n<title>"+org_title[0].text.strip()+"</title>\n")


    #Exetracting Different type of Desc
    trg_desc=trg_soup.findAll('div',{'class':'itemDescription'})
    org_desc=org_soup.findAll('div',{'class':'itemDescription'})

    trg_part['itemDescription']=trg_desc
    org_part['itemDescription']=org_desc

    trg_desc=trg_soup.findAll('li',{'id':'Description'})
    org_desc=org_soup.findAll('li',{'id':'Description'})

    if isArabic(trg_desc):
        trg_part['Description']=trg_desc
        org_part['Description']=org_desc

    trg_desc=trg_soup.findAll('div',{'class':'item-desc'})
    org_desc=org_soup.findAll('div',{'class':'item-desc'})

    if isArabic(trg_desc):
        trg_part['item-desc']=trg_desc
        org_part['item-desc']=org_desc

    trg_desc=trg_soup.findAll('div',{'class':'product_text'})
    org_desc=org_soup.findAll('div',{'class':'product_text'})
    if isArabic(trg_desc):
        trg_part['product_text']=trg_desc
        org_part['product_text']=org_desc
    if ok:
        print trg_title[0].text
        for item in trg_part.keys():
            if len(trg_part[item])>0:
                trg_out+=unicode('<desc type="'+item+'">\n'+trg_part[item][0].text.replace('ENDHERE','\n').replace('ENDSTART','\n').replace('END','\n')+"</desc>\n")
        print org_title[0].text
        for item in org_part.keys():
            if len(org_part[item])>0:
                org_out+=unicode('<desc type="'+item+'">\n'+org_part[item][0].text.replace('ENDHERE','\n').replace('ENDSTART','\n').replace('END','\n')+"</desc>\n")
        trg_out+=unicode("</doc>")
        org_out+=unicode("</doc>")
        en_path=os.path.join(out_dir,'en')
        ar_path=os.path.join(out_dir,'ar')
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        if not os.path.exists(en_path):
            os.makedirs(en_path)
        if not os.path.exists(ar_path):
            os.makedirs(ar_path)

        org_path=os.path.join(en_path,str(counter)+".en")
        trg_path=os.path.join(ar_path,str(counter)+".ar")
        org_file=io.open(org_path,'w',encoding='utf-8')
        trg_file=io.open(trg_path,'w',encoding='utf-8')
        org_file.write(org_out)
        trg_file.write(trg_out)
        org_file.close()
        trg_file.close()

        counter+=1
    return counter


def isArabic(seq):
    aset=['ا','ب','ت','ث','ي','ي','ن','م','ل','ك','ق','ف','غ','ع','ظ','س']
    """ Check whether sequence seq contains ANY of the items in aset. """
    for c in seq:
        if c in aset: return True
    return False




if __name__ == "__main__":
    main(sys.argv[1:])