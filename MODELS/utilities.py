from MODELS.excel_file import *
import chardet



def detectar_encoding(arquivo):
    with open(arquivo, "rb") as f:
        resultado = chardet.detect(f.read(1000))
        return resultado['encoding']
    
def detectar_delimitador(arquivo, enconding):
    with open(arquivo, "r", encoding=enconding) as f:
        primeira_linha = f.readline()
        if "\t" in primeira_linha:
            return "\t"
        elif ";" in primeira_linha:
            return ";"
        elif "," in primeira_linha:
            return ","
        
def convert_csv_to_xlsx(csv_file):

    if csv_file:
        excel_file = csv_file.replace(".csv",".xlsx")

        # Detectar enconding do arquivo
        enconding = detectar_encoding(csv_file)

        # Detectar o delimitador do arquivo
        delimitador = detectar_delimitador(csv_file,enconding)

        # Ler o CSV com o encodnding e o delimitador
        try:   
            df = new_dataframe(csv_file, type=False, delimiter=delimitador, encoding=enconding)
        except UnicodeDecodeError:
            print("⚠️ Erro de decodificação com a codificação detectada, tentando com 'latin1'...")
            df = new_dataframe(csv_file, type=False, delimiter=',',encoding='latin1')

        # Salvar em excel
        df.to_excel(excel_file,index=False)

    else:
        pass
        #print("❌ Nenhum arquivo selecionado")

