from default_window import window
import customtkinter as ctk
from PIL import Image, ImageTk

class menu_window(window):

    

    def __init__(self,window_title,width,height,posx,posy):
        super().__init__(window_title,width,height,posx,posy)
        self.window.geometry(f'{width}x{height}+{posx}+{posy}')
        base_colour = "#EEEEEE"
        secondary_colour = "#304FFE"
        menu_icon = ctk.CTkImage(Image.open("ICONS/home_icon.png"),size=(30,30))

    def create_button(self, name_btn, text, height, width, pos_horz, pos_vert, font=..., command=None, fg_color="gray",text_color = "white",bg_color ="white", position_type="place",corner_radius = 0,image = None,border_width= 0,hover_color = "white"):
        super().create_button(name_btn, text, height, width, pos_horz, pos_vert, font, command, fg_color,text_color,bg_color,position_type,corner_radius,image,border_width,hover_color)

    def create_menu_bar(self):
        menu_bar_frame = ctk.CTkFrame(self.window,bg_color=self.secondary_colour)
        menu_bar_frame.pack(side=ctk.LEFT,fill=ctk.Y,padx=2,pady=3)
        menu_bar_frame.pack_propagate(False)
        menu_bar_frame.configure(width=45)

        self.create_button("menu_btn","",30,30,4,10,bg_color=self.secondary_color,hover_color=self.secondary_color,image=self.menu_icon)
        

