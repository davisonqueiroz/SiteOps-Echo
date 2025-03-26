import customtkinter as ctk

class window:
    def __init__(self,window_title,width,height,resizable = False):
        self.window = ctk.CTk()
        self.window.title(window_title)
        self.window.geometry(f'{width}x{height}')
        self.window.resizable(resizable,resizable)
        self.components = {}       
    
    def create_button(self,name_btn,text,height,width,pos_horz,pos_vert,font =("Arial",16),command = None,fg_color = None,position_type = "place",master = None):
        button = ctk.CTkButton(master = master,text=text,height=height,width=width,font=font,fg_color=fg_color,command=command)
        self.position_component(name_btn,button,pos_horz,pos_vert,position_type)
        self.components[name_btn] = button   
        return button 

    def create_label(self,name_label,text,pos_horz,pos_vert,text_color = "white",font =("Arial",16),bg_color = None,position_type = "place"):
        label = ctk.CTkLabel(self.window,text=text,font=font,text_color=text_color,bg_color=bg_color)
        self.position_component(name_label,label,pos_horz,pos_vert,position_type)
        self.components[name_label] = label
        return label

    def position_component(self,comp_name,component,pos_horz,pos_vert,position_type = "place"):
        if comp_name in self.components:
            if position_type =="place":    
                self.components[comp_name].place_forget()
            elif position_type == "grid":
                self.components[comp_name].grid_forget()
            elif position_type == "pack":        
                self.components[comp_name].pack_forget()
        
        if position_type =="place":
            component.place(x=pos_horz,y=pos_vert)
        elif position_type == "grid":
            component.grid(row=pos_vert,column=pos_horz)
        elif position_type == "pack":
            component.pack(padx=pos_horz,pady=pos_vert)

    def remove_component(self,comp_name):
        if comp_name in self.components:
            self.components[comp_name].destroy()
            self.components.pop(comp_name)

    def display(self):
        self.window.mainloop()
    
    def quit_window(self):
        self.window.quit() 