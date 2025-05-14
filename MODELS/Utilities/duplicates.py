import pandas as pd
import os

def remove_duplicates(excel_file, type_table):
    if not excel_file:
        print("❌ Nenhum arquivo selecionado")
        return
    
    try:
        # Gera o caminho de saída com base no nome do arquivo original
        base_nome = os.path.splitext(os.path.basename(excel_file))[0]
        no_dup_file = os.path.join(os.path.dirname(excel_file), f"No_dup_ {base_nome}.xlsx")

        # Lê a planilha de entrada
        df = pd.read_excel(excel_file, engine='openpyxl')

        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].str.replace(r"http\S+", "", regex=True)

        # Definir as colunas a serem usadas para remoção de duplicatas
        colunas_para_comparacao_exp = [
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
        colunas_para_comparacao_msp = [
            "ID do Campus",
            "Nome do Curso",
            "Grau",
            "Modalidade",
            "Turno",
            "Duração do Curso",
            "Mensalidade sem desconto"
            ]

        # Escolhe as colunas certas conforme o tipo
        if type_table == "msp":
            colunas_para_comparacao = colunas_para_comparacao_msp
        elif type_table == "exp":
            colunas_para_comparacao = colunas_para_comparacao_exp
        else:
            print("❌ Tipo de tabela não reconhecido.")
            return

        # Cria a coluna de chave única concatenada
        df['SKU'] = df[colunas_para_comparacao].astype(str).apply(
            lambda row: '_'.join(row.values), axis=1
        )

        # Cria o df csó com as linhas duplicatas
        df_dup= df[df.duplicated(subset='SKU', keep=False)]

        # Cria um novo df removendo as duplicatas 
        df_no_dup = df.drop_duplicates(subset='SKU', keep='first')

        # Remove a coluna auxiliar da tabela modelo 'exp'
        if type_table =='exp':
            df_no_dup = df_no_dup.drop(columns=['SKU'])
            df_dup = df_dup.drop(columns=['SKU'])

        # Salvar o Df sem duplicadas na tabela original e cria uma nova aba 'Duplicados' para salvar os valores Duplicados
        try:
            with pd.ExcelWriter(no_dup_file, engine='openpyxl') as writer:
                df_no_dup.to_excel(writer, index=False)
                df_dup.to_excel(writer, index=False, sheet_name='Duplicados')
                print(f"📁 Arquivo Excel salvo: {no_dup_file}")
        except Exception as e:
            print(f"⚠️ Erro ao salvar o arquivo Excel: {e}")
    
    except Exception as e:
        print(f"❌ Ocorreu um erro durante o processamento: {e}")