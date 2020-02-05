#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 20:23:21 2020

@author: Home
"""
import os
import pandas as pd

import requests
from bs4 import BeautifulSoup


url = 'https://en.wikipedia.org/wiki/Electric_car'
page_response = requests.get(url)

#parse the page content based on html structure
page_content = BeautifulSoup(page_response.content, "html.parser")


paras = []
for i in range(0, len(page_content.find_all("p"))):
    paras.append(page_content.find_all("p")[i].text)


redirectlinks = []
for i in range(0, len(page_content.find_all("a"))):
    try:
        if page_content.find_all("a")[i].get('class')[0] == 'mw-redirect':
            redirectlinks.append(page_content.find_all("a")[i].get('href'))
    except TypeError:
        continue



"""Function to add files to directory"""
class add_text():
    
    def __init__(self, file_path, folder_name, list_text):
        
        self.file_path = file_path
        self.folder = folder_name
        self.list_text = list_text
        
    
    def create_doc(self):
        
        complete_path = self.file_path+self.folder
        os.mkdir(complete_path)
        
        for i in range(0, len(self.list_text)):
            file = "Page_Paragraph_%s" % i
            with open(complete_path+'/'+file+'.txt', "w") as text_file:
                text_file.write(self.list_text[i])
            
add_text(file_path= "/users/home/desktop/projects/Text Projects/corpus/",
         folder_name='Electric_car',
         list_text = paras).create_doc()
        
  
class save_links():
    
    def __init__(self, file_path, folder_name, list_links):
        
        self.file_path = file_path
        self.folder = folder_name
        self.links = list_links
        
    def collect_links(self):
        
        pd.DataFrame({'Links':self.links}).to_csv(self.file_path+self.folder+'.csv', index=False)
        

        
save_links(file_path = "/users/home/desktop/projects/Text Projects/links/",
           folder_name= "Electric_car",
           list_links = redirectlinks).collect_links()      
      


class get_data():
    
    def __init__(self, core_url, link_list):
        
        self.core_url = core_url
        self.links = link_list
        
        
    def scrape_wiki(self):
        
        for link in self.links:
        
            url = self.core_url+link
            page_response = requests.get(url)
            
            #parse the page content based on html structure
            page_content = BeautifulSoup(page_response.content, "html.parser")
            
            
            paras = []
            for i in range(0, len(page_content.find_all("p"))):
                paras.append(page_content.find_all("p")[i].text)
            
            
            redirectlinks = []
            for i in range(0, len(page_content.find_all("a"))):
                try:
                    if page_content.find_all("a")[i].get('class')[0] == 'mw-redirect':
                        redirectlinks.append(page_content.find_all("a")[i].get('href'))
                except TypeError:
                    continue
                
                            
            folder_name = link.split('/')[2]
            
            add_text(file_path= "/users/home/desktop/projects/Text Projects/corpus/",
                     folder_name=folder_name,
                     list_text = paras).create_doc()
            
            save_links(file_path = "/users/home/desktop/projects/Text Projects/links/",
                        folder_name= folder_name,
                        list_links = redirectlinks).collect_links() 
                



get_data(core_url = 'https://en.wikipedia.org',
         link_list = list(set(redirectlinks))).scrape_wiki()





