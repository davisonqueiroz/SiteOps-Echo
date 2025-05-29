import MODELS.excel_file as ef
import pandas as pd
import openpyxl
import os
class pos_grad_ead:
    def __init__(self,file_msp,file_campus,file_relation_campus):
        file_msp = file_msp
        file_campus = file_campus
        file_relation_campus = file_relation_campus

        self.sheet_process(file_msp,file_campus,file_relation_campus)
        self.lookup_ids()
        self.remove_repetitions()
        self.concat_and_join()
        self.concat_campus()
        self.separing_universities_msp()

    def sheet_process(self,file_msp,file_exp,file_relation):

        self.relation_pending,self.course_pendings,self.campus_pending =  None, None, None
        dtype_campus = {
            'id' : str,
            'metadata_code' : str,
            'university_id' : str
        }
        dtype_msp = {
            'ID_POLO' : str,
            'COD_CURSO' : str
        }
        dtype_relation = {
            'COD_POLO' : str
        }
        self.msp = ef.new_dataframe(file_msp,"Modelo Sem Parar",dtype= dtype_msp)
        self.relation_unipe = ef.new_dataframe(file_relation,"UNIPÊ",dtype= dtype_relation)
        self.relation_positivo = ef.new_dataframe(file_relation,"POSITIVO",dtype= dtype_relation)
        self.exp_cruzeiro = ef.new_dataframe(file_exp,"Sheet 1",dtype= dtype_campus)
        if ef.verify_nas(self.exp_cruzeiro['metadata_code']):
            self.campus_pending = ef.get_nulls_in_dataframe(self.exp_cruzeiro,'metadata_code')
            self.exp_cruzeiro = ef.remove_nas_dataframe(self.exp_cruzeiro,'metadata_code')
        self.exp_unipe = ef.new_filtered_dataframe(self.exp_cruzeiro,"1593","university_id")
        self.exp_positivo = ef.new_filtered_dataframe(self.exp_cruzeiro,"1639","university_id")
        self.exp_cruzeiro = ef.new_filtered_dataframe(self.exp_cruzeiro,"3719","university_id")

    def lookup_ids(self):

        ef.xlookup_pd(self.relation_unipe,self.exp_unipe,'COD_POLO','metadata_code','id','campus_id')
        ef.xlookup_pd(self.relation_positivo,self.exp_positivo,'COD_POLO','metadata_code','id','campus_id')
        if ef.verify_nas(self.relation_positivo['campus_id']):
            self.relation_pending = ef.get_nulls_in_dataframe(self.relation_positivo,'campus_id')
            self.relation_positivo = ef.remove_nas_dataframe(self.relation_positivo,'campus_id')
        if ef.verify_nas(self.relation_unipe['campus_id']):
            self.relation_pending = ef.get_nulls_in_dataframe(self.relation_unipe,'campus_id')
            self.relation_unipe = ef.remove_nas_dataframe(self.relation_unipe,'campus_id')
        

    def remove_repetitions(self):
        self.exp_cruzeiro = ef.remove_specify_from_df(self.relation_positivo['COD_POLO'],self.exp_cruzeiro,'metadata_code')
        self.exp_cruzeiro = ef.remove_specify_from_df(self.relation_unipe['COD_POLO'],self.exp_cruzeiro,'metadata_code')

    def concat_and_join(self):
        self.relation_positivo['concat'] = ef.concat_pd([self.relation_positivo['campus_id'],self.relation_positivo['COD_POLO']],';campus_code:')
        self.relation_unipe['concat'] = ef.concat_pd([self.relation_unipe['campus_id'],self.relation_unipe['COD_POLO']],';campus_code:')

        self.textjoin_pos = ef.textjoin_pd(self.relation_positivo['concat'])
        self.textjoin_unipe = ef.textjoin_pd(self.relation_unipe['concat'])


    def concat_campus(self):

        self.exp_cruzeiro['concat'] = ef.concat_pd([self.exp_cruzeiro['id'],self.exp_cruzeiro['metadata_code']],';campus_code:')
        limit_cells = 32767
        lenght_actually = 0
        self.groups = []
        result = None
        init = 0
        key = 0

        for row,content in enumerate (self.exp_cruzeiro['concat']):
            content_lenght = len(str(content))
            if lenght_actually + content_lenght > limit_cells:
                result = ef.textjoin_pd(self.exp_cruzeiro['concat'].iloc[init:row])
                self.groups.append(result)
                key += 1
                init = row
                lenght_actually = 0
            lenght_actually += content_lenght
        
        if init <= len(self.exp_cruzeiro):
            result =  None
            result = ef.textjoin_pd(self.exp_cruzeiro['concat'].iloc[init:])
            self.groups.append(result)
                    
    def separing_universities_msp(self):
        self.msp_cruzeiro = ef.new_filtered_dataframe(self.msp,"CRUZEIRO DO SUL - PÓS EAD",'Nome da IES')
        self.msp = ef.remove_specify_from_df(self.msp_cruzeiro['Nome da IES'],self.msp,'Nome da IES')
        self.msp = ef.associate_value_from(self.msp,'Nome da IES','UNIPÊ - PÓS-GRADUAÇÃO EAD','ID do Campus',self.textjoin_unipe)
        if len(self.relation_positivo ) == 1:
            self.campus_positivo = self.relation_positivo['campus_id'][0]   
            self.msp = ef.associate_value_from(self.msp,'Nome da IES','POSITIVO - PÓS-GRADUAÇÃO EAD','COD CAMPUS',self.textjoin_pos)
            self.msp = ef.associate_value_from(self.msp,'Nome da IES','POSITIVO - PÓS-GRADUAÇÃO EAD','ID do Campus',self.campus_positivo)
        else:
            self.msp = ef.associate_value_from(self.msp,'Nome da IES','POSITIVO - PÓS-GRADUAÇÃO EAD','ID do Campus',self.textjoin_pos)

    def create_files_limited(self,path):
        range_for = len(self.groups)

        for i in range(range_for):
            self.df_temp = ef.associate_value_from(self.msp_cruzeiro,'Nome da IES','CRUZEIRO DO SUL - PÓS EAD',"ID do Campus",self.groups[i])

            ef.save_df(os.path.join(path,f"CRUZEIRO_POS_GRAD{i}.xlsx"),self.df_temp,'Modelo Sem Parar')
        ef.save_df(os.path.join(path, "UNIPE_E_POSITIVO.xlsx"),self.msp,'Modelo Sem Parar')


