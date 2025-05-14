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