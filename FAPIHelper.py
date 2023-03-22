from tkinter import Tk, Frame
from StartPage import StartPage, PageAutoWhack, PageEditScreen, PageEditAttackSpeed

# SOURCES:
#   https://www.youtube.com/watch?v=IYHJRnVOFlw
#   https://www.youtube.com/watch?v=A0gaXfM1UN0
#   https://stackoverflow.com/questions/37621071/tkinter-add-menu-bar-in-frames


class FAPIHelper(Tk):
    
    def __init__(self, *args, **kwargs):
        
        Tk.__init__(self, *args, **kwargs)
        
        self.alpha_val = 1.0
        
        container = Frame(self)
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
    fapi = FAPIHelper()
    fapi.title('FAPI Helper')
    fapi.geometry("200x240+0+0")
    fapi.attributes('-topmost', True)
    fapi.resizable(False, False)
    fapi.mainloop()