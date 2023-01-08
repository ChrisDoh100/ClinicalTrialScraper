import bs4 as bs
import pickle
import requests
import pandas as pd
import re
from urllib.request import urlopen
import PySimpleGUI as sg




class Bio_Gather():
    def __init__(self):
        self.resp = requests.get('https://topforeignstocks.com/stock-lists/the-complete-list-of-biotech-stocks-trading-on-nasdaq/')
        self.soup = bs.BeautifulSoup(self.resp.text,'lxml')
        self.table = self.soup.find('table',{'class':'tablepress tablepress-id-2509'})


    def building_tickers(self):
        tickers = []
        new_names = {}
        for row in self.table.findAll('tr')[1:]:
            ticker = row.findAll('td')[2].text
            name = row.findAll('td')[1].text
            new_names[ticker] = name
            tickers.append(ticker)
        return tickers,new_names

    def actual_tickers(self,tickers,new_names):
        layout = [[sg.Text('Gathering Company Information:')],
              [sg.ProgressBar(1, orientation='h', size=(20, 20), key='progress')],
          ]
        window = sg.Window('Clinical Finder', layout).Finalize()
        progress_bar = window.FindElement('progress')
        empty = ""
        new_tickers = []
        names = []
        for i in tickers:
            progress_bar.UpdateBar(tickers.index(i), len(tickers))
            resp2 = requests.get('https://finance.yahoo.com/quote/{0}/profile?p={0}'.format(i))
            soup2 = bs.BeautifulSoup(resp2.text,'lxml')
    
            for link in soup2.findAll('a',attrs = {'href':re.compile("^http://www")}):
                website = link.get('href').replace("'","")
                if not empty:
                    new_tickers.append(i)
                    names.append(new_names[i])
                else:
                    tickers.remove(i)
        window.Close()
        return new_tickers,names
    
    def create_company_info(self,new_tickers,names):
        company_table = {'Tickers':new_tickers,'Company':names}
        df = pd.DataFrame(company_table)
        file = df.to_csv('companies.csv')
        print("File Created.")
        print(type(file))
        return file

        
