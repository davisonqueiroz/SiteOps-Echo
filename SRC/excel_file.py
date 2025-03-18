import xlwings as xw
import os 
import pandas as pd

class excel_file:
    def __init__(self,path = None,visibility = True, filtered = False):
        if path:
            self.path = path
            self.visibility = visibility
            self.filtered = filtered
            self.book = xw.Book(self.path)
        else:
            self.book = xw.Book()
            self.path = None
            self.visibility = visibility
            self.filtered = filtered

    #file manipulation

    def new_workbook(self,directory,name):
        file_path = os.path.join(directory,name)
        self.save_workbook(file_path)

    def close_workbook(self):
        self.book.close()
    
    def save_workbook(self,path):
        self.book.save(path)

    def quit_whitout_saving(self):
        self.book.app.quit()