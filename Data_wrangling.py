import pandas as pd
import requests as r
import bs4 as bs
import html5lib
import datetime
import calendar
import PySimpleGUI as sg

class Data_Wrangling():
    def __init__(self):
        self.data = pd.read_csv('companies.csv')

    def csv_cleaner(self):
        companies = []
        empty=""
        print(self.data.columns)
        print(self.data['Company'])
        self.data['Company'] = self.data['Company'].replace(",","").replace("/","%2F").replace(" ","+")
        for i in self.data['Company']:
            i = i.replace(",","").replace("/","%2F").replace(" ","+")
            companies.append(i)
        return companies

    def checker_creator(self):

        current_date = datetime.datetime.now()
        projected_month = current_date.month +2
        name_month = calendar.month_name[projected_month]
        name_year = str(current_date.year)
        checker = [name_year,name_month]

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
            response = r.get('https://clinicaltrials.gov/ct2/results?term={0}&age_v=&gndr=&type=&rslt=&phase=2&Search=Apply'.format(company))
            if response.status_code == 200:
                soup= bs.BeautifulSoup(response.text,'html5lib')
                table=soup.find('table',{'id':'theDataTable'})
                for row in table.findAll("tr"):
                    current_trial = row.findAll('td')[3].text
                    current_trial_number = row.findAll('td')[1].text
                    trials_dates.append(row.findAll('td')[20].text)
    
                company_trial_dates[company] = trials_dates
                for i in trials_dates:
                    check =  all(j in i for j in checker)
                    if check:
                        selected_companies.append(company)
                del trials_dates[:]
        window.close()
        return selected_companies


