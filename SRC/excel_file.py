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

     #sheets manipulation

    def new_sheet(self,sheet_name):
        self.book.sheets.add(sheet_name)

    def get_sheet(self,sheet_name):
        return self.book.sheets[f'{sheet_name}']
    
    def get_first_sheet(self):
        return self.book.sheets[0]
    
    def delete_sheet(self,sheet_name):
        sheet_delete = self.get_sheet(sheet_name)
        sheet_delete.delete()

    def move_sheet_to_beginning(self,sheet_name):
        sheet_name.api.Move(Before = self.book.sheets[0].api)

    def rename_sheet(self,current_name,new_name):
        sheet = self.get_sheet(current_name)
        sheet.name = new_name