# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 20:58:17 2022

@author: Furtherun
"""

"""
This program is used to get the Rust crates information automatically. 
The top 1000 crates infomation is writed in a csv file, named RustCrateInfo.csv.
"""

from msedge.selenium_tools import Edge, EdgeOptions
import time
import random
import csv
import codecs

edge_options = EdgeOptions()
edge_options.use_chromium = True
edge_options.add_argument("headless")

edge_driver_path = ".\msedgedriver.exe"

# url = "https://crates.io/crates?page=1&sort=downloads"
base_url = "https://crates.io/crates?page="

start_page = 1
end_page = 20

crate_idx = 1
link_dict = {}

fileName = "RustCrateInfo.csv"

with codecs.open (fileName, 'w+', 'utf-8') as csvfile:
    title = ['Crate Id', 'Crate Name', 'Crate Version', 'Homepage', 
              'Documentation', 'Repository']
    w = csv.DictWriter(csvfile, fieldnames=title)
    
    w.writeheader()
    
    for page in range(start_page, end_page+1):
        edge = Edge(executable_path=edge_driver_path, options=edge_options)
        edge.get(base_url + str(page) + "&sort=downloads")
        
        time.sleep(3+random.randint(1, 2))
        
        link_dict.clear()
        
        for crate_row in edge.find_elements_by_class_name("_crate-row_s6xett"):
            crate_name = crate_row.find_element_by_class_name("_name_s6xett") \
                .get_attribute("textContent").strip()
            try:
                crate_version = \
                    crate_row.find_element_by_class_name("_version_s6xett") \
                    .get_attribute("textContent").strip()
                
                link_dict['Crate Version'] = crate_version
            except:
                pass
            
            for link_box in crate_row.find_elements_by_class_name("_quick-links_s6xett"):
                for link_item in link_box.find_elements_by_tag_name("a"):
                    link_dict[link_item.get_attribute("textContent")] = \
                        link_item.get_attribute("href")
            
            for link in ['Crate Version', 'Homepage', 
                          'Documentation', 'Repository']:
                if link not in link_dict:
                    link_dict[link] = " "
                    
            w.writerow({'Crate Id': crate_idx, 'Crate Name': crate_name,
                        'Crate Version': crate_version,
                        'Homepage': link_dict['Homepage'],
                        'Documentation': link_dict['Documentation'],
                        'Repository': link_dict['Repository']})
            
            print("%d row Finished ..." % crate_idx)
            
            crate_idx += 1
            
        print("%d page Finished ..." % page)
        edge.close()

edge.quit()

print("--- Mission Finished  ---")


# =============================================================================
# """
# Another try by requests and BeautifulSoup library, I failed because I could
# not deal with 

# <noscript>
#   For full functionality of this site it is necessary to enable JavaScript.
# </noscript>

# I know little about JS knowledge.
# """

# import requests
# from bs4 import BeautifulSoup

# if __name__ == "__main__":
#     base_url = "https://crates.io/crates"
#     max_page = 1
    
#     user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
#         AppleWebKit/537.36 \(KHTML, like Gecko) Chrome/96.0.4664.110 \
#             Safari/537.36 Edg/96.0.1054.62"
#     accept = "text/html,application/xhtml+xml,\
#         application/xml;q=0.9,image/webp,image/apng,*/*;\
#             q=0.8,application/signed-exchange;v=b3;q=0.9"
    
#     headers = {"user-agent": user_agent, "accept": accept}
#     # headers = {"user-agent": user_agent.random, "accept": accept}
#     # print(headers)
#     # r = requests.get(url)
#     # print(r.status_code)
#     for page in range(1, max_page+1):
#         params = {"page": str(page), "sort": "download"}
#         with requests.get(base_url, params=params, headers=headers) as r:
#             # print(r.status_code)
#             # print(r.url)
#             print(r.text)
#             soup = BeautifulSoup(r.text, "html.parser")
#             print(soup.find_all('a'))
# =============================================================================


