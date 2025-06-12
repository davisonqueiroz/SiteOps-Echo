import pandas as pd
import os
from MODELS.Utilities.file_encoding import FileEncoding
from GUI.widgets.notifications import Notification 

class CSVConverter:
    def __init__(self, csv_file: str):
        self.csv_file = csv_file

        base_name = os.path.basename(csv_file)  # pega só o nome do arquivo
        dir_name = os.path.dirname(csv_file)    # pega o caminho do diretório
        new_name = "xlsx_" + base_name.replace(".csv", ".xlsx")
        self.excel_file = os.path.join(dir_name, new_name)
        self.enconding = None
        self.delimiter = None
    
    def detectar_configurações(self):
        self.enconding = FileEncoding.detectar_encoding(self.csv_file)
        self.delimiter = FileEncoding.detectar_delimitador(self.csv_file,self.enconding)

    def ler_csv(self):
        try:
            return pd.read_csv(self.csv_file, delimiter=self.delimiter, encoding=self.enconding)
        except UnicodeDecodeError:
            return pd.read_csv(self.csv_file, delimiter=',', encoding='latin1')

    def converter_para_excel(self):
        if not self.csv_file:
            raise ValueError("Nenhum arquivo CSV foi encontrado")
        
        self.detectar_configurações()
        df = self.ler_csv()
        df.to_excel(self.excel_file, index=False)
        Notification.info("Arquivo Salvo",f"📁 Arquivo Excel salvo: {self.excel_file}")
