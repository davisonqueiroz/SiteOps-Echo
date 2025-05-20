from GUI.qt_core import *

class Card(QFrame):
    def __init__(self,name_card):
        super().__init__()

        self.name_card = name_card

        self.card_components = {
            self.name_card: {
                "front":{
                    "title": None,
                    "btn_option1": None,
                    "btn_option2": None,
                    "combo_box": None,
                    "btn_generate": None
                },
                "back": {
                    "description": None,
                    "close_btn": None
                }
            }
        }

    def base_card(self,bg_color):  
        self.setStyleSheet(f"background-color: {bg_color}; border-radius: 30px;")
        self.setFixedSize(220,300)
        layout_gerenc = QVBoxLayout(self)
        layout_gerenc.setSpacing(0)

        #frames superior e inferior
        top_frame = QFrame()
        bottom_frame = QFrame()

        #layout sup e inf
        top_layout = QVBoxLayout(top_frame)
        top_layout.setAlignment(Qt.AlignTop)
        top_layout.setSpacing(0)
        bottom_layout = QVBoxLayout(bottom_frame)
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom )
        bottom_layout.setSpacing(12)

        layout_gerenc.addWidget(top_frame)
        layout_gerenc.addWidget(bottom_frame)

        return [top_layout, bottom_layout,top_frame,bottom_frame]

    def create_front_card(self,title,bg_color_card,btn_opt_color,color_opt_name,color_hover_opt,btn_gnrt_color,color_gnrt_name,color_hover_gnrt):
        base_card = self.base_card(bg_color_card)
        name_label = QLabel(title)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #F5F5F5")
        name_label.setFixedHeight(30)

        btn_opt1 = self.create_btn("Selecione o arquivo",btn_opt_color,color_opt_name,"5px",color_hover_opt,170,30)
        btn_generate = self.create_btn("Gerar",btn_gnrt_color,color_gnrt_name,"5px",color_hover_gnrt,170,50)

        top_layout = base_card[0]
        bottom_layout = base_card[1]

        top_layout.addWidget(name_label)
        bottom_layout.addWidget(btn_opt1)
        bottom_layout.addWidget(btn_generate)

        self.card_components[self.name_card]["front"].update({
            "title": name_label,
            "btn_option1": btn_opt1,
            "btn_generate": btn_generate
        })
        
    def create_back_card(self,bg_color_card,description):
        base_card = self.base_card(bg_color_card)
        top_layout = base_card[0]
        bottom_layout = base_card[1]

        top_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        bottom_layout.setAlignment( Qt.AlignmentFlag.AlignTop)
    
        btn_close = self.create_btn("X","#F5F5F5","#0C0C0D","15px","#CCCCCC",30,30)

        descript_lbl = QLabel(description)
        descript_lbl.setWordWrap(True)
        descript_lbl.setAlignment(Qt.AlignmentFlag.AlignTop )
        descript_lbl.setFixedSize(193,240)

        bottom_layout.addWidget(descript_lbl)
        top_layout.addWidget(btn_close)

        self.card_components[self.name_card]["back"].update({
            "description": description,
            "close_btn": btn_close
        })

        frame_top = base_card[2]
        frame_bottom = base_card[3]

        frame_top.setFixedSize(200,40)
        frame_bottom.setContentsMargins(0,10,0,0)

    def set_style_btn(self,component,bg_color,color,border,bg_hover_color):
        component.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {color};
                border-radius: {border};
            }}
            QPushButton:hover {{
                background-color: {bg_hover_color};
            }}
        """)
        
    def add_component_card(self,component,type= "button"):
        self.bottom_layout.insertWidget(0,component)
        if type == "button":
            self.card_components[self.name_card]["front"]["btn_option2"] = component
        elif type == "combobox":
            self.card_components[self.name_card]["front"]["combo_box"] = component

        else:
            print(" Erro! Type invalido")
    def create_btn(self,text,bg_color,color,border,bg_hover_color,width,height):
        button = QPushButton(text)
        self.set_style_btn(button,bg_color,color,border,bg_hover_color)
        button.setFixedSize(width,height)
        # self.card_components[self.name_card]["front"]["btn_option2"] = button 
        return button

    def create_combobox(self,list_itens):
        cb_box = QComboBox()
        cb_box.setFixedSize(170,22)
        cb_box.setStyleSheet("background-color: #F5F5F5")
        cb_box.addItems(list_itens)
        return cb_box
    
    def get_text_cbbox(self):
        cb_box = self.card_components[self.name_card]["front"]["combobox"]
        if cb_box is not None:
            return cb_box.currentText()
        else:
            return "Erro! Não há ComboBox adicionado"
        
    def set_text_btn(self,btn_name,new_text):

        button = self.card_components[self.name_card]["front"][btn_name]
        button.setText(new_text)


    def set_action_btn(self,btn_to_set,action):
        button = self.card_components[self.name_card]["front"][btn_to_set]
        button.clicked.connect(action)
