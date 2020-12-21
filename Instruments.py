#from selenium import webdriver
#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
#from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
#from selenium.webdriver.firefox.options import Options
import os


import Configuration
import DBclient

DATABASE = None

def connect_db():
    global DATABASE
    DATABASE = DBclient.DB('127.0.0.1',666)
    DATABASE.connect()


def exist(url:str):
    if DATABASE.exist('sites','url',Configuration.DB_SCHEME['sites']['url'],url):
        return True

    if DATABASE.exist('to_process','url',Configuration.DB_SCHEME['to_process']['url'],url):
        return True

    return False


def new_url(url:str):
    DATABASE.append('to_process',[url],[Configuration.DB_SCHEME['to_process']['url']])


def dump():
    DATABASE.dump()


def get_url_to_process()->str:
    try:
        url = DATABASE.pop('to_process',0,[Configuration.DB_SCHEME['to_process']['url']])[0]
    except:
        return False
    return url


def exist_site(url:str):
    if DATABASE.exist('sites','url',Configuration.DB_SCHEME['sites']['url'],url):
        return True

    return False

def append_site(url:str,name:str,info:str,isup:bool,rating:int):
    DATABASE.append('sites',[url,name,info,isup,rating],Configuration.SITES_TYPES)


def is_photo(url:str):
    for ext in Configuration.photo_formats:
        if ext in url:
            return True

    False


def get_driver():
    #torexe = os.popen(Configuration.TOR_BINARY)
    #binary = FirefoxBinary(Configuration.TOR_BINARY)
    profile = FirefoxProfile(r'C:\Users\User\Desktop\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default')
    profile.set_preference("network.proxy.type",1)
    profile.set_preference("network.proxy.socks", "127.0.0.1")
    profile.set_preference("network.proxy.socks_port", 9150)
    profile.set_preference("network.proxy.socks_remote_dns", True)
    profile.update_preferences()
    options = Options()
    options.add_argument("-profile")
    options.add_argument(r'C:\Users\User\Desktop\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default')
    #driver = webdriver.Firefox(profile,firefox_binary=binary,options=options)
    driver = webdriver.Firefox(profile)
    driver.set_page_load_timeout(50)
    return driver



def append_urls_to_database(urls):
    for url in urls:
        if exist(url):
            continue
        new_url(url)


