import customtkinter as ctk

class def_window:
    def __init__(self,window_title,width,height,resizable = False):
        self.window = ctk.CTk()
        self.window.title(window_title)
        self.window.geometry(f'{width}x{height}')
        self.window.resizable(resizable,resizable)
        self.objects = []

    