from GUI.content_area import *
from GUI.widgets.cards import *
from MODELS.Cruzeiro_do_Sul.pos_grad_ead import *
from MODELS.Cruzeiro_do_Sul.tecnico import *


class Utilities(ContentArea):
    def __init__(self):
        super().__init__("#F5F5F5","VBox")
        self.set_cards_area("#F5F5F5",self.content)

        self.card_exp_msp = Card("exp_msp","#FF7E29")
        self.card_exp_msp.create_front_card("Exp para MSP","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9")
        self.card_exp_msp.create_back_card("#FF7E29","Para a verificação e preenchimento correto siga as instruções: \n1. Selecione a planilha MSP. \n2. Selecione o EXP de campus.\n3.Clique em 'Gerar'\n\n*IMPORTANTE: Certifique-se de selecionar na ordem correta, conforme instruções*")
        self.card_exp_msp.set_action_btn("btn_generate", self.process_files)   
        
        self.card_duplicates = Card("duplicates","#FF7E29")
        self.card_duplicates.create_front_card("Remover Duplicadas","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9")
        self.card_duplicates.create_back_card("#FF7E29","Para a verificação e preenchimento correto siga as instruções: \n1. Selecione a planilha MSP. \n2. Selecione o EXP de campus.\n3.Clique em 'Gerar'\n\n*IMPORTANTE: Certifique-se de selecionar na ordem correta, conforme instruções*")
        self.card_duplicates.set_action_btn("btn_generate", self.process_files)
        
        self.card_csv = Card("csvtoxlsx","#FF7E29")
        self.card_csv.create_front_card("CSV para Excel","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9")
        self.card_csv.create_back_card("#FF7E29","Para a verificação e preenchimento correto siga as instruções: \n1. Selecione a planilha MSP. \n2. Selecione o EXP de campus.\n3.Clique em 'Gerar'\n\n*IMPORTANTE: Certifique-se de selecionar na ordem correta, conforme instruções*")
        self.card_csv.set_action_btn("btn_generate", self.process_files)

        self.card_fix_cities = Card("fix_cities","#FF7E29")
        self.card_fix_cities.create_front_card("Corrigir Cidades","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9")
        self.card_fix_cities.create_back_card("#FF7E29","Para a verificação e preenchimento correto siga as instruções: \n1. Selecione a planilha MSP. \n2. Selecione o EXP de campus.\n3.Clique em 'Gerar'\n\n*IMPORTANTE: Certifique-se de selecionar na ordem correta, conforme instruções*")
        self.card_fix_cities.set_action_btn("btn_generate", self.process_files)        
        
        self.add_card(self.card_exp_msp,"TOP")
        self.add_card(self.card_duplicates,"TOP")
        self.add_card(self.card_csv,"TOP")
        self.add_card(self.card_fix_cities,"BOTTOM")


    def process_files(self):
            if self.card_tecnico.paths["btn_option1"] and self.card_tecnico.paths["btn_option2"]:
                msp = self.card_tecnico.paths["btn_option2"]
                exp = self.card_tecnico.paths["btn_option1"]
                tecnico = tecnicoCruzeiro(msp,exp)
                self.card_tecnico.set_save_manager("btn_generate")
                path_save = self.card_tecnico.paths["save"]
                tecnico.saving_and_separing_pendings(path_save)
                self.card_tecnico.set_text_btns(["btn_option1","btn_option2"],"Selecione o arquivo")
