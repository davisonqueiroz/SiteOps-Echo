import pandas as pd
import os
from GUI.widgets.notifications import Notification

class MSPConverter:
    def __init__(self,exp_file):
        self.exp_file = exp_file

        self.offers_msp_dict = {
            'university_name': 'Nome da IES',
            'university_id': 'ID da IES',
            'campus_name_from_university': 'Nome do Campus',
            'campus_id': 'ID do Campus',
            'name_from_university': 'Nome do Curso',
            'level': 'Grau',
            'kind': 'Modalidade',
            'shift': 'Turno',
            'period_kind': 'Tipo de duração do curso',
            'max_periods': 'Duração do Curso',
            'max_payments': 'Quantidade de Parcelas',
            'full_price': 'Mensalidade sem desconto',
            'offered_price': 'Mensalidade com desconto',
            'discount_percentage': 'Porcentagem de desconto da bolsa (Fixo/1º Semestre)',
            'commercial_discount': 'Mensalidade balcão',
            'university_regressive_discount': 'Porcentagem de desconto IES',
            'start': 'Data de Início da Oferta',
            'end': 'Data de Fim da Oferta',
            'limited': 'LIMITADA?',
            'total_seats': 'Quantidade de Vagas',
            'enrollment_semester': 'Semestre de Ingresso',
            'offer_special_conditions': 'Benefício 1 (Chave OSC)',
            'offer_extra_warning': 'Avisos',
            'offer_extra_benefit': 'Benefícios Extras',
            'campaign': 'Campanha',
            'restricted': 'Restrita?',
            'systems': 'Tipo de restrição (systems:)',
            'ecode_pool_name': 'ecode_pool_name'
        }

        self.remove_columns = [
            'offer_id', 'campus_name', 'name', 'regressive_discount',
            'real_discount', 'created_at', 'paid_seats', 'reserved_seats',
            'saleable_seats', 'position', 'campus_state', 'univ_offer_enabled',
            'course_enabled', 'offer_enabled', 'open_channel_type', 'status',
            'university_offer_id', 'course_id', 'forced_disabled',
            'passing_grade', 'external_id', 'uuid', 'show_on_main_search',
            'stock_type'
        ]

        self.extra_columns = [
            ('Qual valor usar? % ou R$', 'Quantidade de Parcelas', ''),
            ('Porcentagem total de desconto da bolsa (2º Semestre)', 'Porcentagem de desconto da bolsa (Fixo/1º Semestre)', ''),
            ('Mensalidade com desconto (2º Semestre)', 'Porcentagem total de desconto da bolsa (2º Semestre)', ''),
            ('Frequência das aulas', 'Campanha', ''),
            ('Taxa de matrícula', 'Frequência das aulas', ''),
            ('Data de início das aulas', 'Taxa de matrícula', ''),
            ('Carga horária do Curso (em horas)', 'Data de início das aulas', ''),
            ('TCC Obrigatório?', 'Carga horária do Curso (em horas)', ''),
            ('Benefício 2 (Chave OSC)', 'Benefício 1 (Chave OSC)', ''),
            ('COD CURSO', 'Tipo de restrição (systems:)', ''),
            ('COD IES', 'COD CURSO', ''),
            ('COD CAMPUS', 'COD IES', ''),
            ('COD TIPO GRAD', 'COD CAMPUS', ''),
            ('COD TURNO', 'COD TIPO GRAD', ''),
            ('COD CURSO PAI', 'COD TURNO', ''),
            ('COD CAMPUS PAI', 'COD CURSO PAI', ''),
            ('CONCURSO', 'COD CAMPUS PAI', ''),
            ('CodCursoVest', 'CONCURSO', ''),
            ('CodCursoIES', 'CodCursoVest', ''),
            ('NomeCurso', 'CodCursoIES', ''),
            ('TurnoMetadata', 'NomeCurso', ''),
            ('CURRICULO', 'TurnoMetadata', ''),
            ('CodCampus', 'CURRICULO', ''),
            ('CodCampanha', 'CodCampus', ''),
            ('affiliate_link', 'CodCampanha', ''),
            ('tags', 'affiliate_link', '')
        ]

        self.metadata_mapping = {
            'code': 'COD CURSO',
            'campus_code': 'COD CAMPUS',
            'ies_code': 'COD IES',
            'level_code': 'COD TIPO GRAD',
            'shift_code': 'COD TURNO',
            'cod_curso_pai': 'COD CURSO PAI',
            'cod_campus_pai': 'COD CAMPUS PAI',
            'CONCURSO': 'CONCURSO',
            'CURSO_VEST': 'CodCursoVest',
            'CURSO': 'CodCursoIES',
            'DESCRICAO': 'NomeCurso',
            'TURNO': 'TurnoMetadata',
            'CURRICULO': 'CURRICULO',
            'UNIDADE_FISICA': 'CodCampus',
            'COD_CAMPANHA': 'CodCampanha',
            'affiliate_link': 'affiliate_link',
            'tags': 'tags'
        }

        self.course_metadata_mapping = {
            'total_hours': 'Carga horária do Curso (em horas)',
            'obligatory_monograph': 'TCC Obrigatório?'
        }

        self.clean_columns = [
            'Qual valor usar? % ou R$', 'Mensalidade sem desconto', 'Mensalidade com desconto',
            'Porcentagem de desconto da bolsa (Fixo/1º Semestre)', 'regressive_discount',
            'Mensalidade balcão', 'Porcentagem de desconto IES', 'Data de Início da Oferta',
            'Data de Fim da Oferta', 'LIMITADA?', 'Quantidade de Vagas', 'Semestre de Ingresso',
            'Benefício 1 (Chave OSC)', 'Benefício 2 (Chave OSC)', 'Avisos', 'Benefícios Extras',
            'Campanha', 'Frequência das aulas', 'Taxa de matrícula', 'Data de início das aulas',
            'course_metadata', 'Restrita?', 'ecode_pool_name', 'Tipo de restrição (systems:)'
        ]

    def parse_metadata(self, value):
        try:
            if pd.isna(value) or str(value).strip() == '':
                return {}
            result = {}
            for pair in str(value).split(';'):
                if ':' in pair:
                    key, val = pair.split(':', 1)
                    result[key.strip()] = val.strip()
            return result
        except Exception:
            print(f"⚠️ Ignorado metadata inválido: {value}")
            return {}

    def convert(self):
        try:
            base_nome = os.path.splitext(os.path.basename(self.exp_file))[0]
            msp_file = os.path.join(os.path.dirname(self.exp_file), f"MSP_{base_nome}.xlsx")

            df = pd.read_excel(self.exp_file, engine='openpyxl')
            df = df.drop(columns=[col for col in self.remove_columns if col in df.columns])
            df = df.rename(columns=self.offers_msp_dict)

            df.insert(loc=df.columns.get_loc('Nome da IES'), column='v5.0 10/01', value='')

            for new_col, ref_col, default_val in self.extra_columns:
                if ref_col in df.columns:
                    pos = df.columns.get_loc(ref_col) + 1
                    df.insert(loc=pos, column=new_col, value=default_val)
                else:
                    Notification.error("Erro metadata",f"⚠️ Coluna de referência '{ref_col}' não encontrada. Não foi possível inserir '{new_col}'.")

            if 'metadata' in df.columns:
                metadata_parsed = df['metadata'].apply(self.parse_metadata)
                for key, col_dest in self.metadata_mapping.items():
                    df[col_dest] = metadata_parsed.apply(lambda d: d.get(key, ''))
                df = df.drop(columns=['metadata'])

            if 'course_metadata' in df.columns:
                course_metadata_parsed = df['course_metadata'].apply(self.parse_metadata)
                for key, col_dest in self.course_metadata_mapping.items():
                    df[col_dest] = course_metadata_parsed.apply(lambda d: d.get(key, ''))
                df = df.drop(columns=['course_metadata'])

            for col in self.clean_columns:
                if col in df.columns:
                    df[col] = ''

            df.to_excel(msp_file, index=False)
            Notification.info("Arquivo Salvo",f"\n✅ Arquivo {msp_file} criado com sucesso com a estrutura MSP!")

        except Exception as e:
            Notification.error("Erro de processamento",f"❌ Ocorreu um erro durante o processamento: {e}")