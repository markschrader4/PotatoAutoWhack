from customtkinter import CTkFrame, CTkLabel, CTkFont, CTkButton, CTkSlider
from tkinter import Menu, messagebox
from PotatoAutoWhack import PotatoAutoWhack
from Mouse import Mouse
from time import sleep
from pickle import load, dump


class StartPage(CTkFrame):
    
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        
        label = CTkLabel(self, text="FAPI Helper",
                                       font=CTkFont(size=20, weight="bold"))
        label.pack(pady=10, padx=10)
        
        button_auto_whack = CTkButton(self, text="Auto Whack",
                                      command=lambda: controller.show_frame(PageAutoWhack),
                                          fg_color="transparent", border_width=2,
                                          text_color=("gray10", "#DCE4EE"))
        button_auto_whack.pack(pady=5, padx=10)
        
        button_attack_speed_up = CTkButton(self, text="Attack Speed Up",
                                      command=self.start_attack_speed_up,
                                      fg_color="transparent", border_width=2,
                                          text_color=("gray10", "#DCE4EE"))
        button_attack_speed_up.pack(pady=5, padx=10)
        
        slider_screen_alpha = CTkSlider(self, number_of_steps=9,
                                       command=lambda x: 
                                           self.go_dim(controller, x),
                                       from_=0.1, to=1.0)
        slider_screen_alpha.set(1)
        slider_screen_alpha.pack(pady=5, padx=10)
        
        button_quit = CTkButton(self, text="Quit", command=controller.destroy,
                                              fg_color="transparent", border_width=2,
                                          text_color=("gray10", "#DCE4EE"))
        button_quit.pack(pady=5, padx=10)
        
    def start_attack_speed_up(self):
        mousepos = Mouse.getmousepos()
        storedMousePos = self.load_attack_speed_up()
        Mouse.click(storedMousePos[0][0], storedMousePos[0][1])
        sleep(0.1)
        for i in range(30):
            Mouse.click(storedMousePos[0][0], storedMousePos[0][1])
            sleep(0.01)
        Mouse.move(mousepos[0], mousepos[1])
        
    def load_attack_speed_up(self):
        try:
            filehandler = open('storedas.obj', 'rb')
            storedMousePos = load(filehandler)
            filehandler.close()
        except:
            print("Error - File does not exist")
            storedMousePos = [500, 500]#create with default values
        return storedMousePos
        
    def go_dim(self, controller, val):
        controller.alpha_val = val
        controller.attributes('-alpha', val)
        
    def showHelp(self):
        messagebox.showinfo("Information", ("Welcome to FAPIHelper. This app " +
                               "was adapted for the f2p steam game 'Farmers " +
                               "Against Potatoes Idle'. It currently has 2 " + 
                               "features: Auto Potato Whack and Attack Speed Up. " +
                               "Be mindful that both of these features will " +
                               "take over the mouse for a limited time."))
        
    def menubar(self, controller):
        menubar = Menu(controller)
        editMenu = Menu(menubar, tearoff=0)
        editMenu.add_command(label="Attack Speed",underline=0,
                             command=lambda: controller.show_frame(PageEditAttackSpeed))
        helpMenu = Menu(menubar, tearoff=0)
        helpMenu.add_command(label="Info", underline=0,
                             command=self.showHelp)
        menubar.add_cascade(label="Edit", menu=editMenu)
        menubar.add_cascade(label="Help", menu=helpMenu)
        return menubar
        
    def on_focus(self, controller):
        controller.geometry("200x200")
        controller.attributes('-fullscreen', False)
        controller.attributes('-alpha', controller.alpha_val)
        
        
class PageEditAttackSpeed(CTkFrame):
    
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        self.numClicks = 0
        self.mousePos = []
        button_cancel = CTkButton(self, text="CANCEL",
                                      command=lambda: controller.show_frame(StartPage),
                                      fg_color="transparent", border_width=2,
                                          text_color=("gray10", "#DCE4EE"))
        button_cancel.grid(sticky = "s")
        
    def clicked(self, event, controller):
        x = event.x
        y = event.y
        print("Button-1 clicked at %d, %d" %(x, y))
        self.mousePos.append((x, y))
        print(self.mousePos)
        self.numClicks += 1
        if(self.numClicks == 1):
            #save mouse info
            filehandler = open('storedas.obj', 'wb')
            dump(self.mousePos, filehandler)
            filehandler.close()
            
            controller.show_frame(StartPage)
            messagebox.showinfo("Success", ("Position successfully saved."))
        
    def menubar(self, controller):
        emptyMenu = Menu(controller)
        return emptyMenu
    
    def on_focus(self, controller):
        #reset vals
        self.numClicks = 0
        self.mousePos = []
        controller.attributes('-alpha', 0.5)
        controller.attributes('-fullscreen', True)
        messagebox.showinfo("How to edit", ("Click once at the " +
                               "location the 'Attack Apeed Up' button will " +
                               "rapidly click. To cancel, click CANCEL at " +
                               "top left."))
        self.bind('<Button-1>', lambda x: self.clicked(x, controller))
            
    
class PageAutoWhack(CTkFrame):
    
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        self.pwhack = self.load_auto_whack()
        
        label = CTkLabel(self, text="Auto Whack",
                                       font=CTkFont(size=20, weight="bold"))
        label.pack(pady=10, padx=10)
        
        button_start = CTkButton(self, text="Start",
                                      command=self.start_auto_whack,
                                      fg_color="transparent", border_width=2,
                                          text_color=("gray10", "#DCE4EE"))
        button_start.pack(pady=3, padx=10)
        
        button_back = CTkButton(self, text="Main Menu",
                                      command=lambda: controller.show_frame(StartPage),
                                      fg_color="transparent", border_width=2,
                                          text_color=("gray10", "#DCE4EE"))
        button_back.pack(pady=10, padx=10)
        
    def start_auto_whack(self):
        try:
            self.pwhack = self.load_auto_whack()
            self.pwhack.start()
        except:
            print("Error (most likely due to unicolored screen) - Closing")
            self.pwhack.close()
            
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
    
    def showHelp(self):
        messagebox.showinfo("Information", ("When starting, a window will " +
                               "open with a picture, a portion of the screen, " +
                               "and lines drawn between the two. The lines " + 
                               "represent the closest matches between features. " +
                               "When all of the lines are close enough, the " +
                               "mouse will click in the general area. This " +
                               "will stop running after 80 seconds in case " +
                               "the mouse remains uncontrollable (which it " +
                               "shouldn't)."))
            
    def menubar(self, controller):
        menubar = Menu(controller)
        editMenu = Menu(menubar, tearoff=0)
        editMenu.add_command(label="Screen",underline=0,
                             command=lambda: controller.show_frame(PageEditScreen))
        helpMenu = Menu(menubar, tearoff=0)
        helpMenu.add_command(label="Info", underline=0,
                             command=self.showHelp)
        menubar.add_cascade(label="Edit", menu=editMenu)
        menubar.add_cascade(label="Help", menu=helpMenu)
        return menubar
    
    def on_focus(self, controller):
        controller.attributes('-alpha', controller.alpha_val)
        controller.attributes('-fullscreen', False)
        controller.geometry("200x140+0+0")
    
    
class PageEditScreen(CTkFrame):
    #!!KNOWN BUG: editing screen twice in one session does not work - have to restart.
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        self.numClicks = 0
        self.mousePos = []
        button_cancel = CTkButton(self, text="CANCEL",
                                      command=lambda: controller.show_frame(PageAutoWhack),
                                      fg_color="transparent", border_width=2,
                                          text_color=("gray10", "#DCE4EE"))
        button_cancel.grid(sticky = "s")
        
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
                               "top left. !!KNOWN BUG: editing screen twice " +
                               "in one session does not work - have to restart."))
        self.bind('<Button-1>', lambda x: self.clicked(x, controller))