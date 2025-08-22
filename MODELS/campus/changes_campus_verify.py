from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu

class CampusVerifications:
    def __init__(self,exp_campus,mps_polos):
        self.exp = exp_campus
        self.msp = mps_polos
        self.campus_update = None
        self.campus_create = None

    def _load_dataframes(self):
        self.exp_verify = sma(self.exp).load()
        self.msp_campus = sma(self.msp).load()
        self._lower_all_columns_have_string()
        if 'v1' in self.msp_campus.columns:
            self.msp_campus = self.msp_campus.drop(columns= 'v1') 
        self._separate_have_id()
        self._metadata_treatment()
        self._slug_treatment()

    def _lower_all_columns_have_string(self):
        cols = ['name','name_from_university','address','address_adjunct','neighborhood','city']
        self.exp_verify[cols] = self.exp_verify[cols].astype(str).apply(lambda x: x.str.lower())
        self.msp_campus[cols] = self.msp_campus[cols].astype(str).apply(lambda x: x.str.lower())

    def _separate_have_id(self):
        if 'id' in self.msp_campus.columns:
            if not self.msp_campus['id'].isnull().all():
                id_nulls = dfu.get_rows_have_nulls(self.msp_campus,'id')
                self.campus_update = dfu.concat_dataframes(self.campus_update,id_nulls)
                self.msp_campus = dfu.drop_rows_have_nulls(self.msp_campus,'id')

    def _metadata_treatment(self):
        self.exp_verify['metadata_code'] = self.exp_verify['metadata_code'].astype(str).str.split("#")
        self.exp_verify = self.exp_verify.explode("metadata_code",ignore_index= True)
        self.exp_verify = dfu.replace_series(self.exp_verify,'metadata_code','nan','')

    def _slug_treatment(self):
        self.exp_verify['name'] = self.exp_verify['name'].str.replace(r'[^\w\s]|_', '', regex=True)
        if not self.msp_campus.empty and 'name' in self.msp_campus.columns:
            self.msp_campus['name'] = self.msp_campus['name'].str.replace(r'[^\w\s]|_', '', regex=True)

    def _verify_from_metadata(self):
        if not self.msp_campus.empty:
            campus_metadata = dfu.xlookup(self.msp_campus,self.exp_verify,'metadata_code','metadata_code','id','id')
            if dfu.verify_if_have_nulls(campus_metadata ['id']):
                create_by_metadata = dfu.get_rows_have_nulls(campus_metadata ,'id')
                campus_metadata  = dfu.drop_rows_have_nulls(campus_metadata,'id')
                self.campus_update = dfu.concat_dataframes(self.campus_update,campus_metadata)
                self.msp_campus = create_by_metadata
            else:
                self.campus_update = dfu.concat_dataframes(self.campus_update,campus_metadata)
                self.msp_campus = dfu.remove_values_from_column(self.msp_campus,'id',self.campus_update['id'])
    
    def _verify_from_slug(self):
        if not self.msp_campus.empty:
            campus_slug = dfu.xlookup(self.msp_campus,self.exp_verify,'name','name','id','id')
            if dfu.verify_if_have_nulls(campus_slug['id']):
                create_by_slug = dfu.get_rows_have_nulls(campus_slug,'id')
                campus_slug = dfu.drop_rows_have_nulls(campus_slug,'id')
                self.campus_update = dfu.concat_dataframes(self.campus_update,campus_slug )
                self.msp_campus = create_by_slug
            else:
                self.campus_update = dfu.concat_dataframes(self.campus_update,campus_slug)
                self.msp_campus = dfu.remove_values_from_column(self.msp_campus,'id',self.campus_update['id'])

    def _verify_from_sku(self):
        if not self.msp_campus.empty:
            self.msp_campus = self.msp_campus.assign(
                concat1 = dfu.concat_series_with_separator(
                    [
                        self.msp_campus['university_id'],
                        self.msp_campus['address_number'],
                        self.msp_campus['zipcode'],
                        self.msp_campus['virtual']
                    ], 
                    ","
                )
            )
            self.exp_verify = self.exp_verify.assign(
                concat1 = dfu.concat_series_with_separator(
                    [
                        self.exp_verify['university_id'],
                        self.exp_verify['address_number'],
                        self.exp_verify['zipcode'],
                        self.exp_verify['virtual']
                    ], 
                    ","
                )
            )
            campus_sku = dfu.xlookup(self.msp_campus,self.exp_verify,'concat1','concat1','id','id')
            if dfu.verify_if_have_nulls(campus_sku['id']):
                create_by_sku = dfu.get_rows_have_nulls(campus_sku,'id')
                campus_sku = dfu.drop_rows_have_nulls(campus_sku,'id')
                self.campus_update = dfu.concat_dataframes(self.campus_update,campus_sku)
                self.msp_campus = create_by_sku
            else:
                self.campus_update = dfu.concat_dataframes(self.campus_update,campus_sku)
                self.msp_campus = dfu.remove_values_from_column(self.msp_campus,'id',self.campus_update['id'])

    def _separate_infos_in_columns(self):
        #dropar as colunas excedentes
        if 'concat1' in self.campus_update.columns:
            self.campus_update = self.campus_update.drop(columns= 'concat1')
        columns_remove = self.exp_verify.columns.difference(self.campus_update.columns)
        self.exp_verify = self.exp_verify.drop(columns= columns_remove)
        #ordenando pelo id
        self.exp_verify = self.exp_verify.sort_values('id').reset_index(drop=True)
        self.campus_update = self.campus_update.sort_values('id').reset_index(drop=True)
        # preencher com ignore
        for col in self.campus_update.columns:
            if col in ['id','university_id','virtual']:
                continue
            exp_col = self.exp_verify[col]
            for row,value_updt in enumerate(self.campus_update[col]):
                if value_updt in exp_col.values:
                    self.campus_update.at[row,col] = 'ignore'

    def _remove_columns_all_ignore(self):
        for column in self.campus_update.columns:
            if column == 'virtual' and self.campus_update[column].eq(False).all():
                self.campus_update.drop(columns= column, inplace=True)
            else:
                if self.campus_update[column].eq('ignore').all():
                    self.campus_update.drop(columns= column, inplace=True)
    
    def _remove_rows_all_ignore(self):
        cols = self.campus_update.columns.difference(['id','university_id'])
        verify = self.campus_update[cols].eq('ignore').all(axis = 1)
        self.campus_update = self.campus_update.loc[~verify]
            

    def load(self,fullpath):
        self._load_dataframes()
        self._verify_from_metadata()
        self._verify_from_slug()
        self._verify_from_sku()
        if not self.msp_campus.empty:
            self.campus_create = self.msp_campus
        if not self.campus_update.empty:
            self.campus_update['id'] = self.campus_update['id'].astype(int)
            self._separate_infos_in_columns()
            self._remove_columns_all_ignore()
            self._remove_rows_all_ignore()
        if self.campus_create is not None:
            if 'id' in self.campus_create.columns:
                self.campus_create = self.campus_create.drop(columns=['id','concat1'])
        if self.campus_create is not None and self.campus_update is not None:
            dfu.save_multiple_dataframes([self.campus_create,self.campus_update],fullpath,['Campus para Criar','Campus para Atualizar'])
        elif self.campus_create is None and self.campus_update is not None:
            dfu.save_dataframe(self.campus_update,fullpath,'Campus para Atualizar')
        elif self.campus_create is not None and self.campus_update is None:
            dfu.save_dataframe(self.campus_create,fullpath,'Campus para Criar')
        elif self.campus_create is None and self.campus_update is None:
             raise ValueError('Não há campus para atualizar ou criar')

        


            

