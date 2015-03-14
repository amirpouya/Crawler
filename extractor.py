#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# usage: python extractor.py -i<listfile> -o<outdir>
# or
# python extractor.py


import urllib2  # For extracting site pages
from BeautifulSoup import BeautifulSoup  # For processing HTML
import os  #For Creating Dir
import io  #For opening file in UTF8
import sys, getopt
from soupselect import select, monkeypatch, unmonkeypatch
import re

selectors = []


def main(argv):
    fcounter = 0
    list_address = 'link.list'
    output_dir = 'output'
    selectors_address = 'select.list'

    try:
        opts, args = getopt.getopt(argv, "hi:o:s:", ["ifile=", "odir=", 'sfile='])
    except getopt.GetoptError:
        print 'extractor.py -i <listfile> -o <outputdir> -s <selectors>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'extractor.py -i <listfile> -o <outputdir> -s <selectors>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            list_address = os.path.join(arg)
        elif opt in ("-o", "--odir"):
            output_dir = os.path.join(arg)
        elif opt in ("-s", '--sfile'):
            selectors_address = os.path.join(arg)

    try:
        list_file = open(list_address, 'r')
    except IOError:
        print 'No such file or directory:', list_address
        exit(-1)
    try:
        print 'Reading Selectors List'
        global selectors
        selectors = readSelectors(selectors_address)
        print 'Number of Rules:',len(selectors)
    except IOError :
        print 'No such file or directory:', selectors_address
        exit(-1)

    print 'Reading Link List'
    links = list_file.readlines()
    counter = 0;
    all_file_count = len(links)
    print "Start Downloading Pages..."
    for link in links[69:]:
        fcounter += 1
        try:
            link2 = link.replace('ae-en', 'ae-ar')
            print link, link2
            org_page = urllib2.urlopen(link)
            trg_page = urllib2.urlopen(link2)

            org_html = org_page.read().decode('utf-8', 'ignore')
            org_html = org_html.replace('item_tab_contents_wrapper ', '')
            trg_html = trg_page.read().decode('utf-8', 'ignore')
            trg_html = trg_html.replace('item_tab_contents_wrapper ', '')
            outdir = output_dir
            counter = text_extract(trg_html, link2, org_html, link, outdir, counter)
            print fcounter, '/', all_file_count, ":", counter
        except  :
            print "could not download %s" % link


def text_extract(trg_html, trg_link, org_html, org_link, out_dir, counter):
    ok = False
    trg_out = unicode('<doc url="' + trg_link.strip() + '">')
    org_out = unicode('<doc url="' + org_link.strip() + '">')
    multi_out=unicode('<doc en_url="'+org_link.strip()+'" '+ 'ar_url="' + trg_link.strip() + '">')

    trg_soup = BeautifulSoup(''.join(trg_html), convertEntities=BeautifulSoup.HTML_ENTITIES)
    org_soup = BeautifulSoup(''.join(org_html), convertEntities=BeautifulSoup.HTML_ENTITIES)

    trg_part = {}
    org_part = {}
    trg_title = trg_soup.findAll('h1', {'class': 'item-title'})
    #print trg_title
    org_title = org_soup.findAll('h1', {'class': 'item-title'})
    if len(trg_title) < 1 or len(org_title) < 1:
        return counter

    #Extracting and Generating XML docs

    #Title Part
    trg_out += unicode("\n<title>" + trg_title[0].text.strip() + "</title>\n")
    org_out += unicode("\n<title>" + org_title[0].text.strip() + "</title>\n")
    multi_out+=unicode("\n<title>\n"
                       +'<en>'+ org_title[0].text.strip() + '</en>\n'
                       +'<ar>'+ trg_title[0].text.strip()+ '</ar>\n'
                       +"</title>\n")
    #Exetracting Different type of Desc
    for selector in selectors:
        trg_desc = select(trg_soup, selector[0])
        org_desc = select(org_soup,selector[0])
        try:
            if len(trg_desc)==len(org_desc):
                for i in range(len(trg_desc)):
                    if isArabic(trg_desc[i].text):
                        trg_part[selector[1]+str(i)] = trg_desc[i]
                        org_part[selector[1]+str(i)] = org_desc[i]
                        ok = True
        except KeyError:
            pass

    if isArabic(trg_title[0].text):
        ok = True

    if ok:
        print trg_title[0].text
        print org_title[0].text

        for item in sorted(trg_part.keys()):
            if len(trg_part[item]) > 0:
                trg_out += unicode(
                    '<text type="' + item + '">\n' + preprecess_text(trg_part[item].text) + "\n</text>\n")
                org_out += unicode(
                    '<text type="' + item + '">\n' + preprecess_text(org_part[item].text) + "\n</text>\n")
                multi_out +=unicode('<text type="' + item + '">\n'
                                    +"<en>\n"
                                    +preprecess_text(org_part[item].text)+'\n'
                                    +"</en>\n"
                                    +"<ar>\n"
                                    +preprecess_text(trg_part[item].text)+'\n'
                                    +"</ar>\n"
                                    +"</text>\n")
        trg_out += unicode("</doc>")
        org_out += unicode("</doc>")
        multi_out+=unicode("</doc>")
        en_path = os.path.join(out_dir, 'en')
        ar_path = os.path.join(out_dir, 'ar')
        multi_path=os.path.join(out_dir, 'enar')
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        if not os.path.exists(en_path):
            os.makedirs(en_path)
        if not os.path.exists(ar_path):
            os.makedirs(ar_path)
        if not os.path.exists(multi_path):
            os.makedirs(multi_path)
        org_path = os.path.join(en_path, str(counter) + ".en")
        trg_path = os.path.join(ar_path, str(counter) + ".ar")
        multi_path = os.path.join(multi_path, str(counter) + ".enar")
        org_file = io.open(org_path, 'w', encoding='utf-8')
        trg_file = io.open(trg_path, 'w', encoding='utf-8')
        multi_file = io.open(multi_path, 'w', encoding='utf-8')
        org_file.write(org_out)
        trg_file.write(trg_out)
        multi_file.write(multi_out)
        org_file.close()
        trg_file.close()
        multi_file.close()
        counter += 1
    return counter


def isArabic(seq):
    aset = [u'ا', u'ب', u'ت', u'ث', u'ي', u'ي', u'ن', u'م', u'ل', u'ك', u'ق', u'ف', u'غ', u'ع', u'ظ', u'س']
    """ Check whether sequence seq contains ANY of the items in aset. """
    for c in seq:
        if unicode(c) in aset:
            return True
    return False


def readSelectors(selectorAdrees):
    file = io.open(selectorAdrees, 'r', encoding='utf-8')
    lines = file.readlines()
    selectors = []
    for line in lines:
        if line[0]=='//':
            continue
        toks = line.split('|||')
        if len(toks) == 2:
            selectors.append((toks[0].strip(), toks[1].strip()))
    return selectors


def preprecess_text(text):
    text=re.sub('\s\s+','',text)
    text = text.replace('ENDHERE', '\n').replace('ENDSTART', '\n').replace('END', '\n')
    text = strip_ml_tags(text)
    text=text.replace(".$('head').append('","")

    return text


def strip_ml_tags(in_text):
    s_list = list(in_text)
    i, j = 0, 0

    while i < len(s_list):
        # iterate until a left-angle bracket is found
        try:
            if s_list[i] == '<' or s_list[i]=='[':
                while s_list[i] != '/>' or s_list[i]!=']':
                    s_list.pop(i)
                s_list.pop(i)
            else:
                i = i + 1
        except:
            pass
    join_char = ''
    return join_char.join(s_list)


if __name__ == "__main__":
    main(sys.argv[1:])