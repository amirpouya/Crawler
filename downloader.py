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


tocrawl = set([sys.argv[1]])
# linkregex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?')
linkregex = re.compile('href=[\'|"](.*?)[\'"].*?')
linksrc = re.compile('src=[\'|"](.*?)[\'"].*?')
counter=0;



def main():
    link_list = []##create a list of all found links so there are no duplicates
    restrict = sys.argv[1]##used to restrict found links to only have lower level
    link_list.append(restrict)
    tagList=[]
    parent_folder = restrict.rfind('/', 0, len(restrict)-1)

    ##a.com/b/c/d/ make /d/ as parent folder
    while 1:
        try:
            crawling = tocrawl.pop()
        except KeyError:
            break
        url = urlparse.urlparse(crawling)##splits url into sections
        try:
            response_org = urllib2.urlopen(crawling)##try to open the url

        except:
            continue
        msg = response_org.read()##save source of url
        links = linkregex.findall(msg)##search for all href in source
        links = links + linksrc.findall(msg)##search for all src in source
        for link in (links.pop(0) for _ in xrange(len(links))):
            if link.startswith('/'):
                ##if /xxx a.com/b/c/ -> a.com/b/c/xxx
                link = 'http://' + url[1] + link
            elif ~link.find('#'):
                continue
            elif link.startswith('../'):
                if link.find('../../'):##only use links that are max 1 level above reference
                    ##if ../xxx.html a.com/b/c/d.html -> a.com/b/xxx.html
                    parent_pos = url[2].rfind('/')
                    parent_pos = url[2].rfind('/', 0, parent_pos-2) + 1
                    parent_url = url[2][:parent_pos]
                    new_link = link.find('/')+1
                    link = link[new_link:]
                    link = 'http://' + url[1] + parent_url + link
                else:
                    continue
            elif not link.startswith('http'):
                if url[2].find('.html'):
                    ##if xxx.html a.com/b/c/d.html -> a.com/b/c/xxx.html
                    a = url[2].rfind('/')+1
                    parent = url[2][:a]
                    link = 'http://' + url[1] + parent + link
                else:
                    ##if xxx.html a.com/b/c/ -> a.com/b/c/xxx.html
                    link = 'http://' + url[1] + url[2] + link
            if link not in link_list:
                link_list.append(link)##add link to list of already found links
                if (~link.find(restrict)):
                ##only grab links which are below input site
                    tocrawl.add(link)##add link to pending view links
                    link2 =link.replace('ae-en','ae-ar')
                    #print link,link2 ##print downloaded link
                    file_name="ae_en\\"+str(counter)+".html"
                    try:
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
                    except :
                        print "could not download %s"%link
                else:
                    continue

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