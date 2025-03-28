from GUI.default_window import window
import customtkinter as ctk
from PIL import Image, ImageTk

class menu_window(window):

    def __init__(self,window_title,width,height,base_color,secondary_color,tertiary_color):
        #geração da janela
        super().__init__(window_title,width,height)
        pos_x = self.window.winfo_screenwidth()
        pos_y = self.window.winfo_screenheight()
        pos_x = (pos_x // 2) - (width // 2)
        pos_y = (pos_y // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{pos_x}+{pos_y}')

        #cores base da aplicação
        self.base_color = base_color
        self.secondary_color = secondary_color
        self.tertiary_color = tertiary_color

        #criação do menu e frames principais
        self.menu_icon = ctk.CTkImage(Image.open("ASSETS/ICONS/menu_icon.png"),size=(30,30))
        self.labels_dict = {}
        self.frame_width = 60

        self.menu_bar_frame = super().create_frame(self.window,self.secondary_color,self.secondary_color,ctk.LEFT,ctk.Y,5,8,self.frame_width,corner_radius= 20)

        self.create_button("menu_btn","",30,30,8,10,hover_color=self.secondary_color,image=self.menu_icon,fg_color=self.secondary_color,command=self.alterate_menu_command,corner_radius= 3,bg_color= self.secondary_color,master= self.menu_bar_frame)

        self.central_frame = super().create_frame(self.window,self.tertiary_color,self.tertiary_color,ctk.RIGHT,ctk.BOTH,8,8,width=870,grid_propagate= False,corner_radius= 20)


    def create_button(self, name_btn, text, height, width, pos_horz, pos_vert, font =("Arial",16), command=None, fg_color="#304FFE",text_color = "white",bg_color ='white', position_type="place",corner_radius = 0,image = None,border_width= 0,hover_color = 'white',master = None):
        button = super().create_button(name_btn, text, height, width, pos_horz, pos_vert, font, command, fg_color,position_type,master=master)
        button.configure(bg_color = bg_color,corner_radius = corner_radius,image = image,border_width= border_width,hover_color = hover_color,text_color= text_color)

    def create_sub_menu_button(self,name_btn,pos_ver,image,height = 30,width = 2,bg_color = "#304FFE"):
        image_path = image
        icon = ctk.CTkImage(Image.open(image_path),size=(30,30))
        self.create_button(master = self.menu_bar_frame,name_btn=name_btn,pos_horz=12,pos_vert=pos_ver,height=30,width=30,fg_color=self.secondary_color,hover_color=self.secondary_color,bg_color=self.secondary_color,text="",image=icon,command= lambda : self.switch_indication(name_btn))
        self.create_indicator(master = self.menu_bar_frame,name=name_btn,pos_hor=6
                              ,pos_ver=pos_ver + 2,height=height,width=width,bg_color=bg_color)

    def create_indicator(self,master,name,pos_hor,pos_ver,height,width,bg_color = "white"):
        indicator = super().create_label(master,name,"",pos_hor,pos_ver,bg_color=bg_color,width=width,height=height)
        self.labels_dict[name] = indicator

    def switch_indication(self,lb_selected):
        for label in self.labels_dict.values():
            label.configure(bg_color=self.secondary_color)
        lb_selected = self.labels_dict[lb_selected]
        lb_selected.configure(bg_color= self.base_color)

    def extending_animation(self):
        if self.frame_width < 200:
            self.frame_width +=5
            self.menu_bar_frame.configure(width= self.frame_width)
            self.window.after(2,self.extending_animation)
        if self.frame_width == 200:
            self.components["menu_btn"].configure(state="normal")


    def folding_animation(self):
        if self.frame_width > 60:
            self.frame_width -=5
            self.menu_bar_frame.configure(width= self.frame_width)
            self.window.after(2,self.folding_animation)
        if self.frame_width == 60:
            self.components["menu_btn"].configure(state="normal")
   
    def alterate_menu_command(self):
        if self.components["menu_btn"].cget("state") == "disabled":
            return
        self.components["menu_btn"].configure(state="disabled")
        if self.frame_width == 200:
            self.folding_animation()
        else:
            self.extending_animation()
