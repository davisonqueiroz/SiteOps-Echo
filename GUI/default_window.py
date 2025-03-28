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

    def create_label(self,master,name_label,text,pos_horz,pos_vert,text_color = "white",font =("Arial",16),bg_color = None,position_type = "place",width = 0, height = 20):
        label = ctk.CTkLabel(master,text=text,font=font,text_color=text_color,bg_color=bg_color,width=width,height=height)
        self.position_component(name_label,label,pos_horz,pos_vert,position_type)
        self.components[name_label] = label
        return label
    
    def create_frame(self,master,border_color,fg_color,side = None,fill = None,padx = None,pady = None,width = 200,height = None,pack_propagate = False,grid_propagate = None,corner_radius = 0,position_type = "pack",row = None,column = None):
        frame = ctk.CTkFrame(master=master,border_color=border_color,fg_color=fg_color,corner_radius=corner_radius)
        if grid_propagate != None:
            frame.grid_propagate(grid_propagate)
        if position_type == "pack":
            frame.pack(side=side,fill=fill,padx=padx,pady=pady)
            frame.pack_propagate(pack_propagate)
            frame.configure(width=width,height= height)
        elif position_type == "grid":
            frame.grid(row= row,column= column,padx = padx,pady = pady)
            frame.configure(width=width,height= height)

        return frame

    def position_component(self,comp_name,component,pos_horz,pos_vert,position_type = "place",reposition = False):
        if reposition == True:
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