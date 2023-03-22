import customtkinter
from StartPage import StartPage, PageAutoWhack, PageEditScreen, PageEditAttackSpeed

# SOURCES:
#   https://www.youtube.com/watch?v=IYHJRnVOFlw
#   https://www.youtube.com/watch?v=A0gaXfM1UN0
#   https://github.com/TomSchimansky/CustomTkinter


class FAPIHelper(customtkinter.CTk):
    
    def __init__(self, *args, **kwargs):
        
        customtkinter.CTk.__init__(self, *args, **kwargs)
        
        self.alpha_val = 1.0
        
        container = customtkinter.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, PageAutoWhack, PageEditScreen, PageEditAttackSpeed):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartPage)
        
    def show_frame(self, controller):
        frame = self.frames[controller]
        
        menubar = frame.menubar(self)
        self.configure(menu=menubar)
        
        try:
            frame.on_focus(self)
        except:
            print("no on_focus for ", frame)
        
        frame.tkraise()
    
    
if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
    fapi = FAPIHelper()
    fapi.title('FAPI Helper')
    fapi.geometry("200x200+0+0")
    fapi.attributes('-topmost', True)
    fapi.resizable(False, False)
    fapi.protocol("WM_DELETE_WINDOW", fapi.destroy)
    fapi.mainloop()