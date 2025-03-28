from GUI.default_window import *
from GUI.menu import *

class card_frame(menu_window):
    def __init__(self,menu_instance):
        self.menu_instance = menu_instance
        self.components = {}

    def create_card(self,title,select_text,row,column,padx,pady):
        #,description,selec_title
        self.card = super().create_frame(self.menu_instance.central_frame,self.menu_instance.tertiary_color,self.menu_instance.secondary_color,corner_radius= 30,width= 210, height= 280,position_type= "grid",row=row,column= column,padx=padx,pady=pady)
        title_lbl = super().create_label(self.card,"title",title,60,16,self.menu_instance.base_color,bg_color= self.menu_instance.secondary_color,font=("Arial Black",20))
        select_lbl = super().create_label(self.card,"select_lbl",select_text,15,130,self.menu_instance.base_color,bg_color= self.menu_instance.secondary_color)
        select_btn = super().create_button("select_btn","Select archive",25,90,60
        ,128,master= self.card,bg_color= "transparent",fg_color= self.menu_instance.base_color,corner_radius=20,hover_color=self.menu_instance.base_color,text_color=self.menu_instance.secondary_color)
        select_lbl = super().create_label(self.card,"select_lbl","ADD",15,165,self.menu_instance.base_color,bg_color= self.menu_instance.secondary_color)
        select_btn = super().create_button("select_btn","Select archive",25,90,60
        ,163,master= self.card,bg_color= "transparent",fg_color= self.menu_instance.base_color,corner_radius=20,hover_color=self.menu_instance.base_color,text_color=self.menu_instance.secondary_color)
        generate_btn = super().create_button("generate_btn","Gerar",40,120,45
        ,210,master= self.card,bg_color= "transparent",fg_color= self.menu_instance.base_color,corner_radius=20,hover_color=self.menu_instance.base_color,text_color=self.menu_instance.secondary_color)
