import os
import pandas as pd
import numpy as np
from MODELS.Utilities.dicionarios import lista_cidades
from GUI.widgets.notifications import Notification

class CorrigirCidades:
    def __init__(self, xlsx_file):
        self.xlsx_file = xlsx_file
        self.lista_cidades = lista_cidades
        self.df = None
        self.fixed_file = None
    
    def carregar_arquivo(self):
        if not self.xlsx_file:
            return False
        try:
            self.df = pd.read_excel(self.xlsx_file)
            base_name = os.path.basename(self.xlsx_file)  # pega só o nome do arquivo
            dir_name = os.path.dirname(self.xlsx_file)    # pega o caminho do diretório
            new_name = "fixed_cities_" + base_name
            self.fixed_file = os.path.join(dir_name, new_name)
            return True
        except Exception as e:
            Notification.error("Erro ao ler o arquivo",f"⚠️ Erro ao ler o arquivo Excel: {e}")
            return False

    def levenshtein_distance(self, s1, s2):
        len_s1, len_s2 = len(s1), len(s2)
        dp = np.zeros((len_s1 + 1, len_s2 + 1), dtype=int)

        # Inicializa a matriz
        for i in range(len_s1 + 1):
            dp[i][0] = i
        for j in range(len_s2 + 1):
            dp[0][j] = j

        # Preenche a matriz
        for i in range(1, len_s1 + 1):
            for j in range(1, len_s2 + 1):
                if s1[i - 1] == s2[j - 1]:  
                    cost = 0  
                else:
                    cost = 1  
                
                dp[i][j] = min(dp[i - 1][j] + 1,        # Remoção
                            dp[i][j - 1] + 1,           # Inserção
                            dp[i - 1][j - 1] + cost)    # Substituição
        
        return dp[len_s1, len_s2]
    
    def encontrar_correspondente(self, word, word_list):
        if word in word_list:
            return word
        closest_word = min(word_list, key = lambda x: self.levenshtein_distance(word.lower(), x.lower()))
        return closest_word if closest_word.lower()!=word.lower() else word

    def fix_cities(self):
        if self.df is None:
            Notification.error("Erro ao carregar df","⚠️ Dados não carregados.")
            return
        for idx, row in self.df.iterrows():
            cidade, estado = row["city"], row["state"]
            cidades_estado = self.lista_cidades.get(estado, [])
            if cidades_estado:
                cidade_corrigida = self.encontrar_correspondente(cidade, cidades_estado)
                self.df.at[idx, "city"] = cidade_corrigida

    def salvar_arquivo(self):
        if not self.fixed_file:
            Notification.error("Erro no arquivo de saida","⚠️ Caminho do arquivo de saída não definido.")
            return
        try:
            self.df.to_excel(self.fixed_file, index=False, engine='openpyxl')
            Notification.info("Arquivo salvo",f"✅ Arquivo salvo como: {self.fixed_file}")
        except Exception as e:
            Notification.error("Erro ao salvar o arquivo",f"⚠️ Erro ao salvar o arquivo Excel: {e}")

    def executar(self):
        if self.carregar_arquivo():
            self.fix_cities()
            self.salvar_arquivo()
    