from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu
import pandas as pd
import openpyxl
import os
from datetime import date
class PosGradEadCruzeiro:
    def __init__(self,offer_file,file_campus,file_ratio_campus):
        self.headers_transform = {
            " CÓDIGO DA IES" : "Nome da IES",  
            "CURSO" : "Nome do Curso",
            "METODOLOGIA" : "Modalidade",
            "DURAÇÃO (MESES)" : "Duração do Curso",
            "QUANTD PARCELAS" : "Quantidade de Parcelas",
            "PREÇO PARCELAS" : "Mensalidade sem desconto",
            "PORCENTAGEM DE DESCONTO" : "Porcentagem de desconto da bolsa (Fixo/1 º Semestre)",
        }   
        self.offers = offer_file
        self.campus = file_campus
        self.campus_ratio = file_ratio_campus

    def _load_dataframes(self):
        self.offers = sma(self.offers).convert_to_msp_offers_and_load(self.headers_transform)
        self.campus = sma(self.campus).load()
        self.pole_ratio_unp = sma(self.campus_ratio,"UNIPÊ").load()
        self.pole_ratio_pos = sma(self.campus_ratio,"POSITIVO").load()

    def _adjusts_in_msp(self):
        self.msp_columns_adjusts()
        self.transform_and_subtract_value()
        self.separe_universities_courses()

    def _adjusts_in_campus(self):
        self.remove_campus_have_nulls()
        self.separate_campus()
        self.lookup_campus_ids()
        self.remove_campus_that_repeat()

    def _fill_campus_id_in_msps(self):
        self.concat_values_in_ratio_and_join()
        self.create_concat_campus()
        self.fill_in_campus_id_msp()
        self.concat_ies_offers()

    def msp_columns_adjusts(self):
        self.offers['Turno'] = "Virtual"
        self.offers['Tipo de duração do curso'] = "mes"
        self.offers['Grau'] = "Especialização (pós-graduação)"
        self.offers['Qual valor usar?\n% ou R$'] = "porcentagem"
        self.offers['LIMTADA?'] = "FALSE"
        self.offers['Data de Início da Oferta?'] = self._get_date_actually()
        self.offers['Porcentagem de desconto IES'] = self._transform_and_subtract_value(self.offers,'Porcentagem de desconto da bolsa (Fixo/1 º Semestre)')
        self.offers['ID da IES'] = dfu.find_and_replace(self.offers,'Nome da IES','CRUZEIRO DO SUL - PÓS EAD','ID da IES',3719)
        self.offers['ID da IES'] = dfu.find_and_replace(self.offers,'Nome da IES','POSITIVO - PÓS-GRADUAÇÃO EAD','ID da IES',1639)
        self.offers['ID da IES'] = dfu.find_and_replace(self.offers,'Nome da IES','UNIPÊ - PÓS-GRADUAÇÃO EAD','ID da IES',1593)
        #TODO: Pegar data end, OSC e semestre de ingresso por formulário

    def get_date_actually(self):
        today = date.now()
        return today.strftime("%d%m%Y")
    
    def transform_and_subtract_value(self,dataframe,column_name):
        dataframe[column_name] = dataframe[column_name].astype(float)
        dataframe[column_name] = dataframe[column_name] - 0.05
        return dataframe[column_name].round(2)

    def separe_universities_courses(self):
        self.unipe = dfu.filter_content_by_column(self.offers,'UNIPÊ - PÓS-GRADUAÇÃO EAD','ID da IES')
        self.positivo = dfu.filter_content_by_column(self.offers,'POSITIVO - PÓS-GRADUAÇÃO EAD','ID da IES')
        self.cruzeiro = dfu.filter_content_by_column(self.offers,'CRUZEIRO DO SUL - PÓS EAD','ID da IES')

    def remove_campus_have_nulls(self):
        if dfu.verify_if_have_nulls(self.campus['metadata_code']):
            self.pending_campus = dfu.get_rows_have_nulls(self.campus,'metadata_code')
            self.campus = dfu.dropna_rows_by_column(self.campus,'metadata_code')
        
    def separate_campus(self):
        self.exp_unp = dfu.filter_content_by_column(self.campus,"1593","university_id")
        self.exp_pos = dfu.filter_content_by_column(self.campus,"1639","university_id")
        self.exp_cruzeiro = dfu.filter_content_by_column(self.campus,"3719","university_id")
    
    def lookup_campus_ids(self):
        self.pole_ratio_unp = dfu.xlookup(self.pole_ratio_unp,self.exp_unp,'COD_POLO','metadata_code','id','campus_id')
        self.pole_ratio_pos = dfu.xlookup(self.pole_ratio_pos,self.exp_pos,'COD_POLO','metadata_code','id','campus_id')
        if dfu.verify_if_have_nulls(self.pole_ratio_unp['campus_id']):
            self.pending_unp = dfu.get_rows_have_nulls(self.pole_ratio_unp,'campus_id')
            self.pole_ratio_unp = dfu.dropna_rows_by_column(self.pole_ratio_unp,'campus_id')
        if dfu.verify_if_have_nulls(self.pole_ratio_pos['campus_id']):
            self.pending_pos = dfu.get_rows_have_nulls(self.pole_ratio_pos,'campus_id')
            self.pole_ratio_pos = dfu.dropna_rows_by_column(self.pole_ratio_pos,'campus_id')
            self.campus_ratio_pending = dfu.concat_dataframes(self.pending_pos,self.pending_unp)

    def remove_campus_that_repeat(self):
        self.exp_cruzeiro = dfu.remove_values_from_column(self.exp_cruzeiro,'metadata_code',self.pole_ratio_pos['COD_POLO'])
        self.exp_cruzeiro = dfu.remove_values_from_column(self.exp_cruzeiro,'metadata_code',self.pole_ratio_unp['COD_POLO'])

    def concat_values_in_ratio_and_join(self):
        self.pole_ratio_unp['concat'] = dfu.concat_series_with_separator([self.pole_ratio_unp['campus_id'],self.pole_ratio_unp['COD_POLO']],';campus_code:')
        self.pole_ratio_pos['concat'] = dfu.concat_series_with_separator([self.pole_ratio_pos['campus_id'],self.pole_ratio_pos['COD_POLO']],';campus_code:')
        self.join_unp = dfu.textjoin_unique(self.pole_ratio_unp['concat'])
        self.join_pos = dfu.textjoin_unique(self.pole_ratio_pos['concat'])

    def create_concat_campus(self):
        keys = dfu.concat_series_with_separator([self.exp_cruzeiro['id'],self.exp_cruzeiro['metadata_code']],';campus_code:')
        keys_count = keys.str.len()
        limit_cells = 32767
        sum_cells = 0
        self.groups = []
        init = 0
        for row in range(keys):
            current_length = keys_count.iloc[row] + 1
            sum_cells += current_length
            if limit_cells < sum_cells:
                result = dfu.textjoin_unique(keys.iloc[init:row])
                self.groups.append(result)
                init = row
                sum_cells = keys_count.iloc[row] 
        if init < len(keys):
            result = dfu.textjoin_unique(keys.iloc[init:])
            self.groups.append(result)

    def fill_in_campus_id_msp(self):
        self.unipe = dfu.find_and_replace(self.unipe,'Nome da IES','UNIPÊ - PÓS-GRADUAÇÃO EAD','ID do Campus',self.join_unp)
        if len(self.pole_ratio_pos) == 1:
            self.campus_pos = self.pole_ratio_pos['campus_id'][0]   
            self.positivo = dfu.find_and_replace(self.positivo,'Nome da IES','POSITIVO - PÓS-GRADUAÇÃO EAD','COD CAMPUS',self.join_pos)
            self.positivo = dfu.find_and_replace(self.positivo,'Nome da IES','POSITIVO - PÓS-GRADUAÇÃO EAD','ID do Campus',self.campus_pos)
        else:
            self.positivo = dfu.find_and_replace(self.positivo,'Nome da IES','POSITIVO - PÓS-GRADUAÇÃO EAD','ID do Campus',self.join_pos)
    
    def concat_ies_offers(self):
        self.msp = dfu.concat_dataframes(self.positivo,self.unipe)

    def create_files_and_save(self,file_save):
        range_for = len(self.groups)
        for i in range(range_for):
            self.df_temp = dfu.find_and_replace(self.cruzeiro,'Nome da IES','CRUZEIRO DO SUL - PÓS EAD',"ID do Campus",self.groups[i])
            dfu.save_dataframe(os.path.join(file_save,f"CRUZEIRO_POS_GRAD{i}.xlsx"),self.df_temp,'Modelo Sem Parar')
        dfu.save_dataframe(os.path.join(file_save, "UNIPE_E_POSITIVO.xlsx"),self.msp,'Modelo Sem Parar')

    def load(self,file_to_save):
        self._load_dataframes()
        self._adjusts_in_msp()
        self._adjusts_in_campus()
        self._fill_campus_id_in_msps()
        try:
            self.create_files_and_save(file_to_save)
        except Exception as e:
            print (f"Erro durante o processamento: {e}")
