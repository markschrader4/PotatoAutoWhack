from tkinter import Frame, Label, Button, Scale, HORIZONTAL, Menu, messagebox
from PotatoAutoWhack import PotatoAutoWhack
from Mouse import Mouse
from time import sleep
from pickle import load, dump


class StartPage(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        label = Label(self, text="FAPI Helper", font=("Bulleto Killa", 18))
        label.pack(pady=10, padx=10)
        
        button_auto_whack = Button(self, text="Auto Whack",
                                      command=lambda: 
                                          controller.show_frame(PageAutoWhack))
        button_auto_whack.pack(pady=5, padx=10)
        
        button_attack_speed_up = Button(self, text="Attack Speed Up",
                                      command=self.start_attack_speed_up)
        button_attack_speed_up.pack(pady=5, padx=10)
        
        slider_screen_alpha = Scale(self, label='Opacity', resolution=0.1,
                                       command=lambda x: 
                                           self.go_dim(controller, x),
                                       from_=0.1, to=1.0, orient=HORIZONTAL)
        slider_screen_alpha.set(1)
        slider_screen_alpha.pack(pady=5, padx=10)
        
        button_quit = Button(self, text="Quit", command=controller.destroy)
        button_quit.pack(pady=5, padx=10)
        
    def start_attack_speed_up(self):
        mousepos = Mouse.getmousepos()
        Mouse.click(500, 500)
        sleep(0.1)
        for i in range(30):
            Mouse.click(500, 500)
            sleep(0.01)
        Mouse.move(mousepos[0], mousepos[1])
        
    def menubar(self, controller):
        emptyMenu = Menu(controller)
        return emptyMenu
        
    def go_dim(self, controller, val):
        controller.alpha_val = val
        controller.attributes('-alpha', val)
        
    def on_focus(self, controller):
        controller.geometry("200x240")
        controller.attributes('-alpha', controller.alpha_val)
        
    
class PageAutoWhack(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.pwhack = self.load_auto_whack()
        
        label = Label(self, text="Auto Whack", font=("Bulleto Killa", 18))
        label.pack(pady=10, padx=10)
        
        button_start = Button(self, text="Start",
                                      command=self.start_auto_whack)
        button_start.pack(pady=3, padx=10)
        
        button_back = Button(self, text="Main Menu",
                                      command=lambda: 
                                          controller.show_frame(StartPage))
        button_back.pack(pady=10, padx=10)
        
    def start_auto_whack(self):
        
            self.pwhack = self.load_auto_whack()
            self.pwhack.start()
        
            #print("Error (most likely due to unicolored screen) - Closing")
            #self.pwhack.close()
            
    def load_auto_whack(self):
        try:
            filehandler = open('storedms.obj', 'rb')
            storedMousePos = load(filehandler)
            pwhack = PotatoAutoWhack(screenStartx=storedMousePos[0][0],
                               screenStarty=storedMousePos[0][1],
                               screenEndx=storedMousePos[1][0],
                               screenEndy=storedMousePos[1][1],
                               showWindow=self.pwhack.showWindow)
            filehandler.close()
        except:
            print("Error - File does not exist")
            pwhack = PotatoAutoWhack()#create with default values
        return pwhack
            
    def menubar(self, controller):
        menubar = Menu(controller)
        editMenu = Menu(menubar, tearoff=0)
        editMenu.add_command(label="Screen",underline=0,
                             command=lambda: controller.show_frame(PageEditScreen))
        menubar.add_cascade(label="Edit", menu=editMenu)
        return menubar
    
    def on_focus(self, controller):
        controller.attributes('-alpha', controller.alpha_val)
        controller.attributes('-fullscreen', False)
        controller.geometry("200x140+0+0")
    
    
class PageEditScreen(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.numClicks = 0
        self.mousePos = []
        button_cancel = Button(self, text="CANCEL",
                                      command=lambda: controller.show_frame(PageAutoWhack))
        button_cancel.grid(sticky = "s")
        
    def menubar(self, controller):
        emptyMenu = Menu(controller)
        return emptyMenu
    
    def on_focus(self, controller):
        #reset vals
        self.numClicks = 0
        self.mousePos = []
        controller.attributes('-alpha', 0.5)
        controller.attributes('-fullscreen', True)
        messagebox.showinfo("How to edit screen", ("Click once at the top " +
                               "left of the whack a potato area and once at " +
                               "the bottom right. DO NOT include the moving " +
                               "lights or COMBO. To cancel, click CANCEL at " +
                               "top left."))
        self.bind('<Button-1>', lambda x: self.clicked(x, controller))
        
    def clicked(self, event, controller):
        x = event.x
        y = event.y
        print("Button-1 clicked at %d, %d" %(x, y))
        self.mousePos.append((x, y))
        print(self.mousePos)
        self.numClicks += 1
        if(self.numClicks == 2):
            #save mouse info
            filehandler = open('storedms.obj', 'wb')
            dump(self.mousePos, filehandler)
            filehandler.close()
            
            controller.show_frame(PageAutoWhack)
            messagebox.showinfo("Success", ("Screen position successfully " +
                                               "saved."))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        