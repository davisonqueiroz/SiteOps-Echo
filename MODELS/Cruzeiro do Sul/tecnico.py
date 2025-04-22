import MODELS.excel_file as ef
import pandas as pd

def sheet_process(self,file_msp,file_campus):
    self.msp = ef.new_dataframe(file_msp,"Modelo Sem Parar")
    self.port_tec = ef.new_dataframe(file_msp,"Polo X Portfólio Técnico")
    self.tec_nursing = ef.new_dataframe(file_msp,"Polo X Portfólio Tec Enfermagem")

    self.campus = ef.new_dataframe(file_campus,"Sheet 1")
    
    self.pending_nursing,self.pending = None,None

def nursing_treatment(self):
    ef.xlookup_pd(self.tec_nursing,self.campus,'ID_POLO','metadata_code','id','campus_id')
    if ef.verify_nas(self.tec_nursing['campus_id']):
        self.pending_nursing = ef.get_nulls_in_dataframe(self.tec_nursing,'campus_id')
        self.tec_nursing = ef.remove_nas_dataframe(self.tec_nursing,'campus_id')
    self.tec_nursing['concat'] = ef.concat_pd([self.tec_nursing['campus_id'],self.tec_nursing['ID_POLO']],";campus_code:")
    self.nursing_txt_join = ef.textjoin_pd(self.tec_nursing['concat'])

def create_columns_search(self):
    ef.xlookup_pd(self.port_tec,self.msp,'NOME_FILI','Nome da IES','ID da IES','university_id')
    self.port_tec['concat'] = ef.concat_pd([self.port_tec['university_id'],self.port_tec['ID_POLO']])
    self.port_tec['concat2'] = ef.concat_pd([self.port_tec['university_id'],self.port_tec['NOME_POL']])

    self.campus['concat'] = ef.concat_pd([self.campus['university_id'],self.campus['metadata_code']],"-")
    self.campus['concat2'] = ef.concat_pd([self.campus['university_id'],self.campus['name_from_university']],"-")

def fill_in_campus_id(self):
    ef.xlookup_pd(self.port_tec,self.campus,'concat','concat','id','campus_id')
    if ef.verify_nas(self.port_tec['concat']):
        nulls = ef.get_nulls_in_dataframe(self.port_tec,'concat')
        nulls = ef.delete_column_dataframe(self.port_tec,'campus_id')
        self.port_tec = ef.remove_nas_dataframe(self.port_tec,'concat')
        ef.xlookup_pd(nulls,self.campus,'concat2','concat2','id','campus_id')
        if ef.verify_nas(nulls['campus_id']):
            self.pending = ef.get_nulls_in_dataframe(nulls,'concat2')
            nulls = ef.remove_nas_dataframe(nulls,'campus_id')
        self.port_tec = ef.concat_dataframes(self.port_tec,nulls)

def names_treatment(self):
    self.port_tec = ef.replace_pd(self.port_tec,'DESC_CURS'," ","")
    self.port_tec = ef.replace_pd(self.port_tec,'DESC_CURS',".","")

    self.msp['cursos'] = self.msp['Nome do Curso']
    self.msp = ef.replace_pd(self.msp,'cursos',".","")

    self.port_tec['concat_curso'] = ef.concat_pd([self.port_tec['campus_id'],self.port_tec['DESC_CURS']], "-")
    self.port_tec = ef.remove_duplicates_pd(self.port_tec,'concat_curso')

def fill_in_msp(self):
    self.port_tec['ids_concatenados'] = ef.concat_pd([self.port_tec['campus_id'],self.port_tec['ID_POLO']], ";campus_code:")
    ids_campus = []
    for index,row in self.msp.iterrows():
        filter = (self.port_tec['university_id'] == row['ID da IES'] ) & (self.port_tec['DESC_CURS'] == row['curso'])
        filtereds = self.port_tec.loc[filter,'ids_concatenados']
        result = ef.textjoin_pd(filtereds)
        if row['curso'] == 'TECNICO ENFERMAGEM':
            ids_campus.append(self.nursing_txt_join)
        else:
            ids_campus.append(result)
    
    self.msp['ID do Campus'] = ids_campus

def saving_and_separing_pendings(self):
    with pd.ExcelWriter("teste.xlsx",mode= 'a',if_sheet_exists='replace') as writer:
        self.msp.to_excel(writer,sheet_name='Modelo Sem Parar',index= False)
        if self.pending is not None:
            self.pending.to_excel(writer,sheet_name='Pendencias portfolio',index= False)
        if self.pending_nursing is not None:
            self.pending_nursing.to_excel(writer,sheet_name='Pendencias enfermagem',index= False)

