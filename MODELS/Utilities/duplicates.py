import pandas as pd
import os
from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu
from GUI.widgets.notifications import Notification 

class RemoverDuplicadas:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.sheet = sma(self.excel_file)
        self.df = self.sheet.load()
        self.type_table = self.sheet.get_sheet_type()
        self.df_no_dup = None
        self.df_dup = None
        self.no_dup_file = None

    def set_columns_to_compare(self):
        if self.type_table == "msp_offers":
            return [
                "ID do Campus",
                "Nome do Curso",
                "Grau",
                "Modalidade",
                "Turno",
                "Duração do Curso",
                "Mensalidade sem desconto"
            ]
        elif self.type_table == "exp_offers":
            return [
                "university_id",
                "campus_id", 
                "name_from_university",
                "level",
                "kind",
                "shift",
                "enrollment_semester",
                "max_payments",
                "full_price"
            ]
        else:
            raise ValueError("Tipo de tabela não reconhecido")

    def execute(self):
        print(self.type_table)

        # Gera o caminho de saída com base no nome do arquivo original
        base_nome = os.path.splitext(os.path.basename(self.excel_file))[0]
        self.no_dup_file = os.path.join(os.path.dirname(self.excel_file), f"No_dup_{base_nome}.xlsx")

        print('1------------')
        print(self.no_dup_file)

        colunas_para_comparacao = self.set_columns_to_compare()

        print('2------------')
        self.df_no_dup= dfu.remove_duplicates_by_columns(self.df,colunas_para_comparacao)
        print('3------------')
        self.df_dup = dfu.get_duplicates_by_column(self.df,colunas_para_comparacao)
        print('4------------')
        self.save()
        print('5------------')  

    def save(self):
        try:
            dfu.save_multiple_dataframes(
                [self.df_no_dup, self.df_dup],
                self.no_dup_file,
                ["Sem Duplicadas", "Duplicadas"]
            )
        except Exception as e:
            Notification.error("Error ao Salvar",f"Erro ao salvar o arquivo Excel: {e}")