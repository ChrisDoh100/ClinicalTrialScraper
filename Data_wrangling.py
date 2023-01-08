import pandas as pd
import bs4 as bs
import datetime
import calendar
import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver  = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver,10)

class Data_Wrangling():
    def __init__(self):
        self.data = pd.read_csv('nasdaq_screener_healthcare.csv')
        print(self.data['Name'])

    def name_cleanup(name):
        name = name.replace(",","").replace("/","%2F").replace(" ","+").replace("Common","")
        name = name.replace("Stock","").replace("Shares","").replace("Preferred","").replace("Cumulative","")
        return name

    def csv_cleaner(self):
        badwords = ["Stock","Preffered","Cumulative","Shares","Common",",","Series A","Depository","Ordinary","Class A","Class B","Warrants"]
        companies = []
        print(self.data.columns)
        print(self.data['Name'])
        self.data['Name'] = self.data['Name'].replace(",","").replace("/","%2F").replace(" ","+")
        for i in self.data['Name']:
            for j in badwords:
                i = i.replace(j,"")
            i=i.strip()
            i = i.replace(",","").replace("/","%2F").replace(" ","+")
            companies.append(i)
        return companies

    def checker_creator(self):

        current_date = datetime.datetime.now()
        projected_month = current_date.month+2
        name_month = calendar.month_name[current_date.month]
        name_year = str(current_date.year)
        checker = [name_year,name_month]
        print(checker[0],checker[1])
        return checker

    def company_checker(self,checker,companies):
        trials_dates = []
        company_trial_dates = {}
        selected_companies = []
        layout = [[sg.Text('Checking for matches:')],
              [sg.ProgressBar(1, orientation='h', size=(20, 20), key='progress')],
          ]
        window = sg.Window('Clinical Finder', layout).Finalize()
        progress_bar = window.FindElement('progress')
        for company in companies:
            print(company)
            progress_bar.UpdateBar(companies.index(company), len(companies))
            currenturl = "https://clinicaltrials.gov/ct2/results?term={0}&age_v=&gndr=&type=&rslt=&phase=2&Search=Apply".format(company)
            driver.get(currenturl)
            get_url = driver.current_url
            wait.until(EC.url_contains("clinicaltrials.gov"))
            l=driver.find_elements("id","theDataTable")
            if not l:
                continue
            print(company)
            driver.find_element(By.XPATH, "//button[@title='Choose columns to display from a list']").click()
            driver.find_element(By.XPATH, "//span[text()='Study Completion']").click()
            if get_url==currenturl:
                page_source = driver.page_source
            soup= bs.BeautifulSoup(page_source,'html.parser')
            table=soup.find('table',{'id':'theDataTable'})
            print(table)
            table=soup.find('table',{'id':'theDataTable'})
            rows = table.contents[2]
            for row in rows:
                td = row.findAll('td')
                if not td[6].contents:
                    continue
                trials_dates.append(td[6].contents[0])
                print(td[6].contents[0])

            company_trial_dates[company] = trials_dates
            for i in trials_dates:
                check =  all(j in i for j in checker)
                if check:
                    selected_companies.append(company)
            del trials_dates[:]
        window.close()
        return selected_companies


