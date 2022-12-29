try:
    import pickle # this is for saving cookies
    import os # os module 
    import sys # sys module
    from bs4 import BeautifulSoup
    from selenium import webdriver # webdriver
    from selenium.webdriver import Chrome # chrome 
    from selenium.webdriver.common.keys import Keys # keys
    from selenium.webdriver.common.by import By # by
    from selenium.webdriver.support.ui import WebDriverWait # webdriverwait
    from selenium.webdriver.support import expected_conditions # expected conditions
    from selenium.common.exceptions import TimeoutException # time out exception
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support import expected_conditions as EC # options
    from selenium.webdriver.common.proxy import Proxy, ProxyType
    import time # time module 
    import re
    import json
    import random
    from multiprocessing.pool import ThreadPool, Pool
    import threading
    import concurrent.futures
    import pyautogui as gui
    import requests # request img from web
    import shutil # save img locally
    from configparser import ConfigParser
    print("all modules are loaded!")
except ModuleNotFoundError as e:
    print("Installing packages!")
    os.system("pip install -r requirements.txt") # installing all required packages 
class AirBNB:
    file= "config.ini"
    config = ConfigParser()
    config.read(file)
    c_b_p_x=int(config['x_y']['close_button_p_x'])
    c_b_p_y=int(config['x_y']['close_button_p_y'])
    g_u_x = int(config['x_y']['gui_arrow_x'])
    g_u_y = int(config['x_y']['gui_arrow_y'])
    dg_x = int(config['x_y']['drag_down_x'])
    dg_y = int(config['x_y']['drag_down_y'])
    print(dg_x)
    images = []
    with open("user_agent.txt","r",encoding="utf-8") as f:
        user_agent = [agent for agent in f.readlines()]
    link = input("please put your link here:> ").strip()
    def scraper(self):
        options = Options()
        #options.add_extension('vpn.crx')
        options.add_argument(f'user-agent={random.choice(self.user_agent)}')
        driver = webdriver.Chrome(executable_path=r"chromedriver.exe",options=options)
        driver.set_window_size(500,500)
        driver.get(self.link)
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[11]/section/div/div/div[2]/div/div[2]/div')))
            gui.click(self.c_b_p_x,self.c_b_p_y)
            time.sleep(1)
            print("transiltion window closed!")
        except:
            pass
        print(gui.pixel(self.g_u_x,self.g_u_y))
        while gui.pixel(self.g_u_x,self.g_u_y)[0] == 241:
            bs_obj = BeautifulSoup(driver.page_source,features="html.parser")
            images = bs_obj.find_all('img',{"class":"_6tbg2q"})
            print(f"Total Scraped Images!{len(images)}")
            for image in images:
                if image['data-original-uri'] not in self.images:
                    if image['data-original-uri'] is not None:
                        self.images.append(image['data-original-uri'])
            gui.doubleClick(self.dg_x,self.dg_y)
            time.sleep(0.2)
        print(f"Total Scraped Images {len(self.images)}")
    def downloader(self,image):
        url = image
        file_name = f"scraped/{self.images.index(image)+1}.jpg"
        res = requests.get(url, stream = True)
        if res.status_code == 200:
            with open(file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)
                print('Image sucessfully Downloaded: ',file_name)
        else:
            print('Image Couldn\'t be retrieved')
    def run(self):
        self.scraper()
        with open("images.json","w",encoding="utf-8") as f:
            json.dump(self.images,f,ensure_ascii=False,indent=4)
            f.close()
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(self.downloader,self.images)
        print("Scraping Task done!")
if __name__ == "__main__":
    bot = AirBNB()
    bot.run()
            

