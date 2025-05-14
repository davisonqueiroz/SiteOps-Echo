import pandas as pd
from file_encoding import detectar_encoding, detectar_delimitador

def convert_csv_to_xlsx(csv_file):
    if csv_file:
        excel_file = csv_file.replace(".csv", ".xlsx")
        enconding = detectar_encoding(csv_file)
        delimitador = detectar_delimitador(csv_file, enconding)

        try:
            df = pd.read_csv(csv_file, delimiter=delimitador, encoding=enconding)
        except UnicodeDecodeError:
            print("⚠️ Erro de decodificação, tentando com 'latin1'...")
            df = pd.read_csv(csv_file, delimiter=',', encoding='latin1')

        df.to_excel(excel_file, index=False)
