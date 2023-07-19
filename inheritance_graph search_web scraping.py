# project: p3
# submitter: kenigsztein
# partner: none
# hours: 20

import os, zipfile
from collections import deque
from selenium.common.exceptions import NoSuchElementException
import time
from IPython.core.display import Image, display
import pandas as pd


class GraphScraper:
    def __init__(self):
        self.visited = set()
        self.BFSorder = []
        self.DFSorder = []

    def go(self, node):
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        if node in self.visited:
            return 
        self.visited.add(node)
        node_kids = self.go(node)
        for child in node_kids:
            self.dfs_search(child)

    def bfs_search(self, node):
        self.visits = []
        self.list = []
        self.list.append(node)
        while len(self.list):
            now = self.list[0]
            new = self.go(now)
            if now not in self.visits:
                
                self.list.remove(now)
                self.visits.append(now)
                
                for val in new:
                    if val not in self.visits and val not in self.list:
                        self.list.append(val)                
        
        
class FileScraper(GraphScraper):
    def go(self, node):
        children = []
        
        with open(os.getcwd() + '/file_nodes/' + str(node) + '.txt', 'r') as file:
            file.readline()
            child_str = file.readline()
            child_str = child_str.replace(" ", "")
            for child in child_str:
                children.append(child)
                
            children.pop(-1)
            BFS_temp = file.readline()
            DFS_temp = file.readline()
            self.BFSorder.append(BFS_temp[5:-1])
            self.DFSorder.append(DFS_temp[5:-1])
        return children
    
    def dfs_search(self,node):
        traverse = node in self.visited
        if traverse == True:
            return 
        self.visited.add(node)
        children = self.go(node)
        
        for child in children:
            self.dfs_search(child)
    def bfs_search(self, node):
        queue = deque([])
        queue.append(node)
        while len(queue) > 0:
            children = self.go(queue[0])
            self.visited.add(queue[0])
            queue.popleft()
            for child in children:
                visited = child in self.visited
                if visited == True:
                    continue 
                in_queue = child in queue
                if in_queue == True:
                    continue
                queue.append(child)
            continue 
                
               
           
class WebScraper(GraphScraper):
    # required
    def __init__(self, driver=None):
        super().__init__()
        self.driver = driver

    # these three can be done as groupwork
    def go(self, url):
        self.driver.get(url)
        try:
            btn = self.driver.find_element_by_id("DFS")
            btn.click()
            self.DFSorder.append(btn.text)
        except NoSuchElementException:
                pass
            
        try:
            btn = self.driver.find_element_by_id("BFS")
            btn.click()
            self.BFSorder.append(btn.text)
        except NoSuchElementException:
                pass
       
        links = self.driver.find_elements_by_tag_name('a')
        return [link.get_attribute("href") for link in links]
    def dfs_pass(self, start_url):
        self.DFSorder = []
        self.visited.clear()
        self.dfs_search(start_url)
        return "".join(self.DFSorder)

    def bfs_pass(self, start_url):
        self.BFSorder = []
        self.visited.clear()
        self.bfs_search(start_url)
        return "".join(self.BFSorder)

    # write the code for this one individually
    def protected_df(self, url, password):
        
        self.driver.get(url) 
        
        for passwords in password:   
            try:
                id_of_button = "btn" + passwords
                self.driver.find_element_by_id(id_of_button).click()
                
                
                
                time.sleep(.5)
                
            except NoSuchElementException:
                pass

        self.driver.find_element_by_id("attempt-button").click()
        time.sleep(0.5)
        for btns in range(4): 
            
            time.sleep(0.5)
            try:
                self.driver.find_element_by_id("more-locations-button")
            except NoSuchElementException:
                break
                
            self.driver.find_element_by_id("more-locations-button").click()
        return pd.read_html(self.driver.page_source)[0]
