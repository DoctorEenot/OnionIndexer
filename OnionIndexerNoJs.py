import Instruments
import time
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
import logging


session = None


def get_root(url:str):
    offset_left = url.find('//')
    offset_right = url.find('/',offset_left+2)
    if offset_right==-1 or offset_left==-1:
        return url

    return url[:offset_right]

    

def get_all_urls(root:str,main_url:str,soup):
    to_return = []
    tags = soup.find_all('a')
    parsed_main_url = ''
    if main_url[-1]=='/':
        parsed_main_url = main_url[:len(main_url)-1]
    else:
        parsed_main_url = main_url
    for tag in tags:
        url = tag.get('href')
        if url == None or len(url) == 0:
            continue
        if url==root:
            continue
        if Instruments.is_photo(url):
            continue
        url_root = get_root(url)
        if url[:4] != 'http':
            if '://' in url or 'mailto:' in url or 'xmpp:' in url:
                continue

            if url[0]=='#':
                continue
            else:
                offset = url.find('#')
                if offset != -1:
                    if url[:offset] in parsed_main_url:
                        continue
                    else:
                        url = url[:offset]


            url = root+url
        else:
            if '.onion' not in url_root:
                continue
            offset = url.find('#',len(url_root))
            if offset != -1:
                url = url[:offset]
            #if '#' in url[len(url_root):]:
            #    continue

        print(f'\t{url}')
        url = quote(url,safe=':/?&=%',encoding='utf-8')

        #if Instruments.exist(url):
            #continue
        #Instruments.new_url(url)
        to_return.append(url)
    return to_return





def get_title(soup):
    try:
        title = soup.title.string
    except:
        title = None
    if title == None:
        return ''
    return title


#def get_all_text(soup):
#    top = driver.find_element_by_tag_name('body')
#    text = top.text
#    return text

def main_loop():
    global session
    while True:
        #Instruments.dump()
        url = Instruments.get_url_to_process()
        
        if url == False:
            time.sleep(2)
            continue
        if Instruments.is_photo(url):
            continue
        print(f'Kernel url: {url}')
        ison=True

        start_time = time.time()
        try:
            response = session.get(url,timeout=Instruments.Configuration.MAX_RESPONSE_TIME)
        except Exception as e:
            ison=False

        time_taken = int(time.time()-start_time)

        
        point = 0

        not_html = False

        if ison:
            try:
                if 'text' not in response.headers['content-type'].lower():
                    not_html = True
            except:
                if 'html' not in response.text[:len(response.text)//2]:
                    not_html = True

            if time_taken == 0:
                points = 100
            else:
                points = Instruments.Configuration.MAX_RESPONSE_TIME//time_taken
            if not not_html:
                soup = BeautifulSoup(response.text,'html.parser')
                urls = get_all_urls(get_root(url),url,soup)
                Instruments.append_urls_to_database(urls)

        if not Instruments.exist_site(url):
            if not ison:
                Instruments.append_site(url,'None','None',False,0)
                continue
            if not_html:
                Instruments.append_site(url,'None','NotHtml',True,points)
            title = get_title(soup)
            Instruments.append_site(url,title,'None',True,points)
        time.sleep(0.2)


def get_session():
    session = requests.session()
    
    session.proxies = Instruments.Configuration.proxies
    return session


def main():
    global session
    Instruments.connect_db()
    session = get_session()
    
    try:
        main_loop()
    except Exception as e:
        logging.warning('Exception ',exc_info=e)

    input('Exception Accured')





if __name__ == '__main__':
    main()
