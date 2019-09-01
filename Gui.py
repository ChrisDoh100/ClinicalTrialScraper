from scripter import Bio_Gather as bg
from Data_wrangling import Data_Wrangling as dw
from tkinter import *
from tkinter.ttk import *
import datetime as dt

#Getting Date for gui
date_found = dt.datetime.now()

actual_date = date_found.strftime("%d-%b-%y (%H:%M:%S)")

#Getting Tickers and names
tickers = bg()

obtaining_tickers,obtaining_names = tickers.building_tickers()

new_tickers, names = tickers.actual_tickers(obtaining_tickers,obtaining_names)

data = tickers.create_company_info(new_tickers,names)

#Starting data_wrangling
data_wr = dw()
#returns an array of companies
cleaner = data_wr.csv_cleaner()
#creates the check date, 2 months ahead of current date
checker = data_wr.checker_creator()
#actual_checker
results = data_wr.company_checker(checker,cleaner)
#Cleaning up the results
results = [i.replace('+',' ').replace('%2F','/') for i in results]
#creating gui
class App(Frame):

    def __init__(self, parent,results,date_found):
        self.date_found = date_found
        self.results = results
        Frame.__init__(self, parent)
        self.CreateUI()
        self.LoadTable()
        self.grid(sticky = (N,S,W,E))
        parent.grid_rowconfigure(0, weight = 1)
        parent.grid_columnconfigure(0, weight = 1)

    def CreateUI(self):
        tv = Treeview(self)
        tv['show'] = 'headings'
        tv['columns'] = ('Company','Number','Date Found')
        tv.heading("#3", text='Date Found:', anchor='center')
        tv.column("#3", anchor="center",width=200)
        tv.heading("#2", text='Companies', anchor='center')
        tv.column("#2", anchor="center",width=200)
        tv.heading("#1", text='No:',anchor='center')
        tv.column("#1", anchor='center', width=50)
        tv.grid(sticky = (N,S,W,E))
        self.treeview = tv
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

    def LoadTable(self):
        for i,n in enumerate(results):
            self.treeview.insert('', 'end', text=i,values=( i,n, self.date_found))

def main():
    root = Tk()
    App(root,results,actual_date)
    root.mainloop()

if __name__ == '__main__':
    main()
