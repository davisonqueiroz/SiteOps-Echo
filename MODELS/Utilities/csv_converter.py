import pandas as pd
from file_encoding import FileEncoding

class CSVConverter:
    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self.excel_file = csv_file.replace(".csv",".xlsx")
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
