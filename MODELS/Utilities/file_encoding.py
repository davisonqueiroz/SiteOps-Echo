import chardet

class FileEncoding:
    @staticmethod
    def detectar_encoding(arquivo: str) -> str:
        with open(arquivo, "rb") as f:
            resultado = chardet.detect(f.read(1000))
            return resultado['encoding']

    @staticmethod
    def detectar_delimitador(arquivo: str, enconding: str) -> str:
        with open(arquivo, "r", encoding=enconding) as f:
            primeira_linha = f.readline()
            if "\t" in primeira_linha:
                return "\t"
            elif ";" in primeira_linha:
                return ";"
            elif "," in primeira_linha:
                return ","