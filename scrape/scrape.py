import string
import re
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# import os
# os.environ['MOZ_HEADLESS'] = '1'

file = open('links', 'r')
lines = file.readlines()

options = Options()
options.page_load_strategy = 'eager'
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
# create a new Firefox session

expiration_list = {}

for line in lines:

    print(line)
    driver.get(line)
    df_list = pd.read_html(driver.page_source)

    for i, df in enumerate(df_list):
    
        df = df.T.reset_index().T.reset_index(drop=True)
        # Not fridge columns
        for column in df.columns[1:]:
            fridge = False;
            if "fri" in str(column).lower():
                continue
    
            for index, row in df.iterrows():
                s = str(df[column][index])
                if "fri" in s.lower():
                    fridge = True;
                    break
    
            if fridge == False:
                df = df.drop(columns = [column])
    
        if df.shape[1] != 2:
            continue
    
        df.columns = ['foods', 'dates'] #rename the columns
    
        dfs = []
        splits = [0]
    
        c = df.columns[0]
        for index, row in df.iloc[1:].iterrows():
            s = str(df[c][index])
            if "open" in s.lower():
                splits.append(index)
    
        splits.append(df.shape[0])
    
        pairs = []
    
        for i in range(1, len(splits)):
            pairs.append([splits[i - 1], splits[i]])
    
        for p in pairs:
            dfs.append(df.iloc[p[0]:p[1], :])
    
        dic = {"day" : 1, "week" : 7, "month" : 30, "year": 365}
    
        for d in dfs:
            d = d.dropna()
            for index, row in d.iloc[1:].iterrows():
    
                if not any(i.isdigit() for i in d['dates'][index]):
                    continue
                s = str(d['foods'][index])
                s = s.replace('for', '')
                s = s.replace('lasts', '')
                s = s.replace('last', '')
                d.at[index, c] = s
                
                date = str.lower(d['dates'][index])
                num = int(re.search(r'\d+', date).group())

                for k in dic:
                    if k in date:
                        num *= dic[k]
    
                d.at[index, 'dates'] = num
    
            for index, row in d.iloc[1:].iterrows():
                if type(d['dates'][index]) is int:
                    expiration_list[d.at[index, 'foods']] = d.at[index, 'dates']
    
with open('result.json', 'w') as fp:
    json.dump(expiration_list, fp, indent="")
