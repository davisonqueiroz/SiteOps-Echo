from GUI.default_window import window
import customtkinter as ctk
from PIL import Image, ImageTk

class menu_window(window):

    

    def __init__(self,window_title,width,height,posx,posy):
        super().__init__(window_title,width,height)
        self.window.geometry(f'{width}x{height}+{posx}+{posy}')
        self.base_colour = "#EEEEEE"
        self.secondary_colour = "#304FFE"
        self.menu_icon = ctk.CTkImage(Image.open("ICONS/menu_icon.png"),size=(30,30))
        self.labels_dict = {}
        self.frame_width = 45

    def create_button(self, name_btn, text, height, width, pos_horz, pos_vert, font =("Arial",16), command=None, fg_color=None,text_color = "white",bg_color =None, position_type="place",corner_radius = 0,image = None,border_width= 0,hover_color = None):
        button = super().create_button(name_btn, text, height, width, pos_horz, pos_vert, font, command, fg_color,position_type)
        button.configure(bg_color = bg_color,corner_radius = corner_radius,image = image,border_width= border_width,hover_color = hover_color,text_color= text_color)
        

    def create_menu_bar(self):
        self.menu_bar_frame = ctk.CTkFrame(self.window,border_color=self.secondary_colour,fg_color=self.secondary_colour)
        self.menu_bar_frame.pack(side=ctk.LEFT,fill=ctk.Y,padx=2,pady=3)
        self.menu_bar_frame.pack_propagate(False)
        self.menu_bar_frame.configure(width=45)

        self.create_button("menu_btn","",30,30,4,10,bg_color=self.secondary_colour,hover_color=self.base_colour,image=self.menu_icon,fg_color=self.secondary_colour,command=self.alterate_menu_command)
        
        
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

    def extending_animation(self):
        if self.frame_width < 200:
            self.frame_width +=5
            self.menu_bar_frame.configure(width= self.frame_width)
            self.window.after(2,self.extending_animation)

    def folding_animation(self):
        if self.frame_width > 45:
            self.frame_width -=5
            self.menu_bar_frame.configure(width= self.frame_width)
            self.window.after(2,self.folding_animation)
        
    def alterate_menu_command(self):
        if self.frame_width == 200:
            self.folding_animation()
        else:
            self.extending_animation()