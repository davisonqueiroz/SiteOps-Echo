from default_window import window
import customtkinter as ctk
from PIL import Image, ImageTk

class menu_window(window):

    

    def __init__(self,window_title,width,height,posx,posy):
        super().__init__(window_title,width,height,posx,posy)
        self.window.geometry(f'{width}x{height}+{posx}+{posy}')
        self.base_colour = "#EEEEEE"
        self.secondary_colour = "#304FFE"
        self.menu_icon = ctk.CTkImage(Image.open("ICONS/home_icon.png"),size=(30,30))
        self.labels_dict = {}

    def create_button(self, name_btn, text, height, width, pos_horz, pos_vert, font=..., command=None, fg_color="gray",text_color = "white",bg_color ="white", position_type="place",corner_radius = 0,image = None,border_width= 0,hover_color = "white"):
        super().create_button(name_btn, text, height, width, pos_horz, pos_vert, font, command, fg_color,text_color,bg_color,position_type,corner_radius,image,border_width,hover_color)

    def create_menu_bar(self):
        self.menu_bar_frame = ctk.CTkFrame(self.window,bg_color=self.secondary_colour)
        self.menu_bar_frame.pack(side=ctk.LEFT,fill=ctk.Y,padx=2,pady=3)
        self.menu_bar_frame.pack_propagate(False)
        self.menu_bar_frame.configure(width=45)

        self.create_button("menu_btn","",30,30,4,10,bg_color=self.secondary_color,hover_color=self.secondary_color,image=self.menu_icon)
        
    def create_sub_menu_button(self,name_btn,pos_hor,pos_vert,height_btn,width_btn,height,width,fg_color = "white",text = ""):
        self.create_button(name_btn=name_btn,pos_horz=pos_hor,pos_vert=pos_vert,height=height_btn,width=width_btn,fg_color=fg_color,text=text)
        self.create_indicator(name=name_btn,pos_hor=pos_hor,pos_vert=pos_vert,height=height,width=width,fg_colour=self.secondary_colour)

    def create_indicator(self,name,pos_hor,pos_vert,height,width,fg_colour = "white"):
        lbl_indicator = ctk.ctkLabel(master = self.menu_bar_frame,fg_color=fg_colour)
        lbl_indicator.place(x=pos_hor,y=pos_vert,height=height,width=width)
        self.labels_dict[name] = lbl_indicator

    def switch_indication(self,lb_selected):
        for label in self.labels_dict.values():
            label.configure(fg_color=self.secondary_colour)
        lb_selected = self.labels_dict[lb_selected]
        lb_selected.configure(fg_color= self.base_colour)


    def open_menu_bar(self):
        self.menu_bar_frame.config(width=200)
        self.menu_btn.configure(command=self.close_menu_bar)

    def close_menu_bar(self):
        self.menu_bar_frame.config(width=45)
        self.menu_btn.configure(command=self.open_menu_bar)


    def extending_animation(self):
        current_width = self.menu_bar_frame.winfo_width()
        if not current_width > 200:
            current_width +=10
            self.window.after(ms=8,func=self.extending_animation)

    def folding_animation(self):
        current_width = self.menu_bar_frame.winfo_width()
        if current_width != 45:
            current_width -=10
            self.window.after(ms=8,func= self.folding_animation)