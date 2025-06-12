import MODELS.excel_file as ef
import os
from GUI.widgets.notifications import Notification
class TableDivisor:
    def __init__(self,excel_file,quantity_divisions):
        self.excel_file = excel_file
        self.quantity_divisions = int(quantity_divisions)
        self.calc_quantity_rows()

    def calc_quantity_rows(self):
        self.table = ef.new_dataframe(self.excel_file,0)

        total_rows = self.table.iloc[:, 1].last_valid_index() + 1
        self.rows_for_division = total_rows // self.quantity_divisions

    def create_files(self,path):
        name_file = os.path.splitext(os.path.basename(self.excel_file))[0]
        for i in range(1,self.quantity_divisions):
            df_temp = ef.get_rows(self.table,range(0,self.rows_for_division))
            ef.save_df(os.path.join(path,f"{name_file}{i}.xlsx"),df_temp,"Sheet 1")
            self.table = ef.remove_rows(self.table,range(0,self.rows_for_division))
        ef.save_df(os.path.join(path,f"{name_file}{self.quantity_divisions}.xlsx"),self.table,"Sheet 1")
        Notification.info("Arquivo Salvo",f"Arquivo salva na pasta {path}")
