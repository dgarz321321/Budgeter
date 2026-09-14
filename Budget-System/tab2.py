from imports import *

connection = sqlite3.connect('data.db')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS userInfo(
    username text,
    password text,
    first_name text,
    last_name text,
    pronoun text,
    age integer,
    accountBalance real,
    savingBalance real,
    monthlyIncome real
    
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS user_goals (
    username text,
    goal text 
)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS subs (
    username text,
    subscription text,
    subscription_price real
)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS exp (
    username text,
    expense text,
    expense_price real
)""")
connection.commit()
connection.close()

appearance_window = "System"
isfs = True
slider = 1.0
theme  = "blue"

class HomeTab(CTk):
    def __init__(self,username):
        height = 500
        self.user = username
        super().__init__()
        self.title("Budget Home")
        self.geometry("1200x680")
        self.grid_columnconfigure((0,1,2,3), weight=1)
        self.grid_rowconfigure((1,3), weight=1)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

        # Home Tab Before Entering
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        # Left Frame
        self.userName = cursor.execute(f"SELECT first_name FROM userInfo WHERE username = '{self.user}';")
        self.userName = cursor.fetchone()[0]
        self.welcomeLabel = CTkLabel(master = self, text=f"Welcome To The Budgeter {self.userName}", font = CTkFont(size = 30, weight = "bold")).grid(row = 0, column = 1, sticky = "nsew")
        self.tabLeftFrame = CTkFrame(master = self, width = 250).grid(row = 1, column = 0, padx = (0,20), sticky = "nsew")
        self.tabView = LeftTabbing(master = self.tabLeftFrame, width= 300).grid(row = 1, column = 0, padx = (0,20), sticky = "nsew")
        
        # Mid Frame with Image
        self.midFrame = CTkFrame(master = self, width = 100,height = 100, fg_color="transparent").grid(row = 1, column = 2, padx = (0,20), sticky = "nsew")
        self.HomeImage = CTkImage(Image.open(os.path.join(image_path, "Budgeter.png")), size=(350, 350))
        self.HomeLabel = CTkLabel(master = self.midFrame, text="", image=self.HomeImage)
        self.HomeLabel.grid(row = 1, column = 1, padx = (70,0))

        # Right Frame
        self.tabRightFrame = CTkFrame(master = self, width = 250).grid(row = 1, column = 5, padx = (20,0), sticky = "nsew")
        self.tabView2 = RightTabbing(master = self.tabLeftFrame, width= 300).grid(row = 1, column = 5, padx = (20,0), sticky = "nsew")

        #Start Button  
        self.startImage = CTkImage(Image.open(os.path.join(image_path, "startButton.png")), size=(150, 150))
        self.startFrame = CTkFrame(master = self, width = 0, height = 50)
        self.startFrame.grid_columnconfigure(2, weight = 1)
        self.startFrame.grid(row = 2, column = 0, columnspan = 10, sticky = "NSEW")
        self.startButton = CTkButton(master = self.startFrame,text="",image=self.startImage, command = self.start, width=100, fg_color="transparent")
        self.startButton.grid(row = 0, column = 2, padx = 20, pady = 20)

    def start(self):
        user = self.user
        self.destroy()
        # isfs, theme, slider, appearance_window setup 
        page = MainPage(user = user, isfs=isfs, theme=theme, slider=slider, appearance_window=appearance_window)
        page.mainloop()

# Class which will hold tabs
class LeftTabbing(CTkTabview):
    def __init__(self, master, width, **kwargs):
        super().__init__(master, width, height = 500, **kwargs)

        # All tabs
        self.add("Home")
        self.add("Settings")

        #Home Configuration 
        self.textbox = CTkTextbox(master = self.tab("Home"), width=250, height = 350)
        
        self.textbox.grid(row=0, column = 0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        with open('Text/Home_Text.txt', 'r' ) as x:
            Text = x.read()
            self.textbox.insert("0.0",Text)
        self.textbox.configure(state = "disabled")

        # Settings Configuration
        CTkLabel(master = self.tab("Settings"), text = "Set Apperance Option", font = CTkFont(size = 15)).grid(row = 0, column = 0, padx = (50,0), pady = (20,0))
        self.appearance_option = CTkOptionMenu(master = self.tab("Settings"), values=["System Default", "Dark", "Light"], command=self.changeAppearance)
        self.appearance_option.grid(row = 1, column = 0, padx = (60,0), pady = (0,20))

        CTkLabel(master = self.tab("Settings"), text = "Fullscreen / Resizable", font = CTkFont(size = 15)).grid(row = 3, column = 0, padx = (50,0), pady =(20,0))
        self.color_theme = CTkOptionMenu(master = self.tab("Settings"), values = ["Yes","No"], command=self.isFullscreen)
        self.color_theme.grid(row = 4, column = 0, padx = (60,0), pady = (0,20))

        CTkLabel(master = self.tab("Settings"), text = "Color Theme", font = CTkFont(size = 15)).grid(row = 5, column = 0, padx = (50,0), pady = (20,0))
        self.color_theme = CTkOptionMenu(master = self.tab("Settings"), values = ["Blue","Green"], command=self.setTheme)
        self.color_theme.grid(row = 6, column = 0, padx = (60,0), pady = (0,20))

        CTkLabel(master = self.tab("Settings"), text = "Scaling", font = CTkFont(size = 15)).grid(row = 8, column = 0, padx = (50,0), pady = (20,0))
        self.slider_1 = CTkSlider(master = self.tab("Settings"), from_=0, to=3, number_of_steps=4, command=self.sliderVal)
        self.slider_1.grid(row = 9, column = 0, padx = (60,0), pady = (0,20))



    def changeAppearance (self, mode : str):
        global appearance_window
        if mode == "System Default":
            appearance_window = "System"
        else:
            appearance_window = mode
     
    def isFullscreen(self, mode : str):
        global isfs
        if mode == "Yes":
            isfs = True
        else:
            isfs = False
    def sliderVal(self, mode : int):
        global slider
        if mode == 0:
            slider = 0.8
        elif mode == 0.75:
            slider = 0.9
        elif mode == 1.5:
            slider = 1.0
        elif mode == 2.25:
            slider = 1.1
        elif mode == 3.0:
            slider = 1.2


    def setTheme(self, mode : str):
        global theme
        if mode == "Blue":
            theme = "blue"
        elif mode == "Green":
            theme =  "green"
        elif mode == "Dark Blue":
            theme = "dark_blue"
            

class RightTabbing(CTkTabview):
    def __init__(self, master, width, **kwargs):
        super().__init__(master, width, height = 500, **kwargs)

        #All tabs
        self.add("Purpose")
        self.add("More Info")

        
        # Purpose Configuration
        self.textbox = CTkTextbox(master = self.tab("Purpose"), width=250, height = 350)
        
        self.textbox.grid(row=0, column = 0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        with open('Text/Purpose_Text.txt', 'r' ) as x:
            Text = x.read()
            self.textbox.insert("0.0",Text)
        self.textbox.configure(state = "disabled")
        # More Info Configuration
        CTkLabel(master = self.tab("More Info"), text = "Contact Us", font = CTkFont(size = 15)).grid(row = 0, column = 1, padx = (0,75), pady = (20,0))

        CTkLabel(master = self.tab("More Info"), text = "Gael Galvan:", font = CTkFont(size = 15)).grid(row = 1, column = 0, padx = (40,0), pady = (20,0))
        CTkLabel(master = self.tab("More Info"), text="gaelgalvan12@gmail.com",font= CTkFont(size=15, underline=True)).grid(row = 1, column = 1, padx = (10,0), pady = (20,0))

        CTkLabel(master = self.tab("More Info"), text = "Angel Escobedo:", font = CTkFont(size = 15)).grid(row = 2, column = 0, padx = (40,0), pady = (20,0))
        CTkLabel(master = self.tab("More Info"), text="angel.escobedo03@utrgv.edu",font= CTkFont(size=15, underline=True)).grid(row = 2, column = 1, padx = (10,0), pady = (20,0))

        CTkLabel(master = self.tab("More Info"), text = "Diego Esparza:", font = CTkFont(size = 15)).grid(row = 3, column = 0, padx = (40,0), pady = (20,0))
        CTkLabel(master = self.tab("More Info"), text="testemail123@gmail.com",font= CTkFont(size=15, underline=True)).grid(row = 3, column = 1, padx = (10,0), pady = (20,0))

        CTkLabel(master = self.tab("More Info"), text = "David Garza:", font = CTkFont(size = 15)).grid(row = 4, column = 0, padx = (40,0), pady = (20,0))
        CTkLabel(master = self.tab("More Info"), text="dgarz321@gmail.com",font= CTkFont(size=15, underline=True)).grid(row = 4, column = 1, padx = (10,0), pady = (20,0))

class MyFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

class MainPage(CTk):
    def __init__(self, user,isfs, theme, slider, appearance_window):
        super().__init__()
        # Sets up what was previously set in settings
        set_appearance_mode(appearance_window)
        set_default_color_theme(theme)
        set_widget_scaling(slider)
        if (isfs):
            self.winWidth = str(int(self.winfo_screenwidth()))
            self.winHeight = str(int(self.winfo_screenheight()))
            self.geometry(f"{self.winWidth}x{self.winHeight}")
            self.span = int(self.winWidth)
            self.y = int(self.winHeight)
        else:
            self.span = 1200
            self.y = 680
            self.geometry("1200x680")
            self.resizable(False,False)

        #SQL connection
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Formatting Home Frame
        self.HbF = CTkScrollableFrame(master = self, corner_radius=0, fg_color="transparent", width = self.span, height=(self.y / slider), scrollbar_button_hover_color=theme)
        self.ebf = CTkScrollableFrame(master = self, corner_radius=0, fg_color="transparent", width = self.span, height=(self.y / slider), scrollbar_button_hover_color=theme)
        self.gbf = CTkScrollableFrame(master = self, corner_radius=0, fg_color="transparent", width = self.span, height=(self.y / slider), scrollbar_button_hover_color=theme)

        # Tabs
        self.user = user
        self.columnconfigure(0, weight = 1)

        self.topFrame = CTkScrollableFrame(master = self, height = 50, width = (self.span), orientation= "horizontal", scrollbar_button_hover_color=theme)
        self.topFrame.grid(row = 0, column = 0, columnspan = 3, sticky = "nsew")
        self.homeButton = CTkButton(self.topFrame, corner_radius=0, height=40,width = (self.span / (3*slider)), border_spacing=10, text="Home", 
                                    command= self.goHome, fg_color="transparent")
        self.homeButton.grid(row = 0, column = 0)

        self.ExpensesButton = CTkButton(self.topFrame, corner_radius=0, height=40, width = (self.span / (3*slider)),border_spacing=10, command = self.goExpenses, text="Change Values", fg_color="transparent")
        self.ExpensesButton.grid(row = 0, column = 1)

        self.graphButton = CTkButton(self.topFrame, corner_radius=0, height=40, width = (self.span / (3*slider)), border_spacing=10, command = self.goGraph, text="Graph", fg_color="transparent")
        self.graphButton.grid(row = 0 , column = 2)



        # Home Tab Formatting

        self.savingsFrame = CTkFrame(master = self.HbF, height = 50, width = (self.span),fg_color="transparent")
        self.savingsFrame.grid(row = 1, column = 0, columnspan = 3, sticky = "nsew")

        # Balance Frame
        self.balance = cursor.execute(f"SELECT accountBalance FROM userInfo WHERE username = '{self.user}';")
        self.balance = cursor.fetchone()[0]
        self.balanceLabel1 = CTkLabel(self.savingsFrame, corner_radius=0, text = "Balance:", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
        self.balanceLabel1.grid(row = 1, column = 0, sticky = "w")
        self.balanceLabel2 = CTkLabel(self.savingsFrame, corner_radius=0, text=f"${int(self.balance):,d}", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
        self.balanceLabel2.grid(row = 1, column = 2, padx = (100, 0), sticky = "e")

        # Savings Frame
        self.balance = cursor.execute(f"SELECT SavingBalance FROM userInfo WHERE username = '{self.user}';")
        self.balance = cursor.fetchone()[0]
        self.savingsLabel1 = CTkLabel(self.savingsFrame, corner_radius=0, text = "Savings:", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
        self.savingsLabel1.grid(row = 2, column = 0, sticky = "w")
        self.savingsLabel2 = CTkLabel(self.savingsFrame, corner_radius=0, text=f"${int(self.balance):,d}", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
        self.savingsLabel2.grid(row = 2, column = 2, padx = (100, 0), sticky = "e")

        self.balance = cursor.execute(f"SELECT monthlyIncome FROM userInfo WHERE username = '{self.user}';")
        self.balance = cursor.fetchone()[0]

        # Income Frame
        self.incomeLabel1 = CTkLabel(self.savingsFrame, corner_radius=0, text = "Income:", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
        self.incomeLabel1.grid(row = 3, column = 0, sticky = "w")
        self.incomeLabel2 = CTkLabel(self.savingsFrame, corner_radius=0, text=f"${int(self.balance):,d}", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
        self.incomeLabel2.grid(row = 3, column = 2, padx = (100, 0), sticky = "e")
        
        self.beginExpenseFrame = CTkFrame(master = self.HbF, height = 50, width = (self.span), fg_color="transparent")
        self.beginExpenseFrame.grid(row = 3, column = 0, pady = (50,0))
        self.ExpenseLabel = CTkLabel(self.beginExpenseFrame, corner_radius = 0, text="Expenses",  font=CTkFont(family = "bookman", size=20, weight="bold"), bg_color="transparent")
        self.ExpenseLabel.grid(row = 1, column = 1) 
        
        
        self.expenseFrame = CTkFrame(master = self.HbF, height = 50, width = (self.span),fg_color="transparent")
        self.expenseFrame.grid(row = 4, column = 0, columnspan = 3, sticky = "nsew")
        #iterating through expense SQL array
        self.expenseName = cursor.execute(f"SELECT expense FROM exp WHERE username = '{self.user}';")
        for i, name in enumerate(self.expenseName):
            self.expenseLabel1 = CTkLabel(self.expenseFrame, corner_radius=0, text = f"{name[0]}:", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
            self.expenseLabel1.grid(row = (i), column = 0, sticky = "w")

        self.balance = cursor.execute(f"SELECT expense_price FROM exp WHERE username = '{self.user}';")
        for x, money in enumerate(self.balance):
            self.expenseLabel2 = CTkLabel(self.expenseFrame, corner_radius=0, text=f"${int(money[0]):,d}", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
            self.expenseLabel2.grid(row = (x), column = 2, padx = (100, 0), sticky = "e")

        self.beginSubFrame = CTkFrame(master = self.HbF, height = 50, width = (self.span), bg_color="transparent")
        self.beginSubFrame.grid(row = 6, column = 0, pady = (50,0))
        self.subLabel = CTkLabel(self.beginSubFrame, corner_radius = 0, text="Subscriptions",  font=CTkFont(family = "bookman", size=20, weight="bold"), bg_color="transparent")
        self.subLabel.grid(row = 1, column = 1) 

        self.subFrame = CTkFrame(master = self.HbF, height = 50, width = (self.span),fg_color="transparent")
        self.subFrame.grid(row = 7, column = 0, columnspan = 3, sticky = "nsew")


        #Iterating through subscription SQL array
        self.expenseName = cursor.execute(f"SELECT subscription FROM subs WHERE username = '{self.user}';")
        for i, name in enumerate(self.expenseName):
            self.subLabel1 = CTkLabel(self.subFrame, corner_radius=0, text = f"{name[0]}:", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
            self.subLabel1.grid(row = (i), column = 0, sticky = "w")

        self.balance = cursor.execute(f"SELECT subscription_price FROM subs WHERE username = '{self.user}';")
        for x, money in enumerate(self.balance):
            self.subLabel2 = CTkLabel(self.subFrame, corner_radius=0, text=f"${int(money[0]):,d}", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
            self.subLabel2.grid(row = (x), column = 2, padx = (100, 0), sticky = "e")
        connection.close()
        self.TestFrame = CTkFrame(master = self.HbF, height = 50, width = 0,fg_color="transparent")
        self.TestFrame.grid(row = 8,column = 5, sticky = 'nsew', pady = (50,0))


        # Expenses Tab Formatting

        # Set Balance
        self.SetFrame = CTkFrame(master = self.ebf, height = 50, width = (self.span),fg_color="transparent")
        self.SetFrame.grid(row = 0, column = 0, sticky = 'nsew', pady = 10)

        self.SbalanceLabel = CTkLabel(master = self.SetFrame, corner_radius=0, text = "Set Balance:", text_color="white",font=CTkFont(family = "bookman", size=25, weight="bold"))
        self.SbalanceLabel.grid(row = 1, column = 0, sticky = 'nsew', pady = 20)
        self.SbalanceEntry = CTkEntry(master = self.SetFrame)
        self.SbalanceEntry.grid(row = 1, column = 2, padx = (20, 0), sticky = 'nsew', pady = 20)
        self.SbalanceButtom = CTkButton(master = self.SetFrame, text = "Submit", command = self.changeBal, width=100)
        self.SbalanceButtom.grid(row = 1, column = 3, padx = (20,0 ), pady = 20)
        
        # Set Savings
        self.savingsLabel = CTkLabel(master = self.SetFrame, corner_radius=0, text = "Set Savings:", text_color="white",font=CTkFont(family = "bookman", size=25, weight="bold"))
        self.savingsLabel.grid(row = 2, column = 0, sticky = "nsew", pady = 20)
        self.savingsEntry = CTkEntry(master = self.SetFrame)
        self.savingsEntry.grid(row = 2, column = 2, padx = (20, 0), sticky = 'nsew', pady = 20)
        self.savingsButtom = CTkButton(master = self.SetFrame, text = "Submit", command = self.changeSav, width=100)
        self.savingsButtom.grid(row = 2, column = 3, padx = (20,0 ), pady = 20)

        # Set Income
        self.IncomeLabel = CTkLabel(master = self.SetFrame, corner_radius=0, text = "Set Income:", text_color="white",font=CTkFont(family = "bookman", size=25, weight="bold"))
        self.IncomeLabel.grid(row = 3, column = 0, sticky = "w", pady = 20)
        self.IncomeEntry = CTkEntry(master = self.SetFrame)
        self.IncomeEntry.grid(row = 3, column = 2, padx = (20, 0), sticky = 'nsew', pady = 20)
        self.IncomeButtom = CTkButton(master = self.SetFrame, text = "Submit", command = self.changeInc, width=100)
        self.IncomeButtom.grid(row = 3, column = 3, padx = (20,0 ), pady = 20)

        # add Subscriptions
        self.InsertFrame = CTkFrame(master = self.ebf, height = 50, width = (self.span),fg_color="transparent")
        self.InsertFrame.grid(row = 2, column = 0, sticky = 'nsew', pady = (20,0))

        self.subLabel = CTkLabel(master = self.InsertFrame, corner_radius=0, text = "Insert Subscription (name / price)", text_color="white",font=CTkFont(family = "bookman", size=25, weight="bold"))
        self.subLabel.grid(row = 0, column = 2, sticky = 'nsew', pady = (0,20))
        self.nameEntry = CTkEntry(master = self.InsertFrame)
        self.nameEntry.grid(row = 1, column = 1, sticky = 'e')
        self.priceEntry = CTkEntry(master = self.InsertFrame)
        self.priceEntry.grid(row = 1, column = 3, sticky = 'w')
        self.SubButton = CTkButton(master = self.InsertFrame, text = "Submit", command = self.changeSub, width=100)
        self.SubButton.grid(row = 2 , column = 2)

        # add Expenses
        self.ExLabel = CTkLabel(master = self.InsertFrame, corner_radius=0, text = "Insert Expense (name / price)", text_color="white",font=CTkFont(family = "bookman", size=25, weight="bold"))
        self.ExLabel.grid(row = 3, column = 2, sticky = 'nsew', pady = (0,20))
        self.ExnameEntry = CTkEntry(master = self.InsertFrame)
        self.ExnameEntry.grid(row = 4, column = 1, sticky = 'e')
        self.ExpriceEntry = CTkEntry(master = self.InsertFrame)
        self.ExpriceEntry.grid(row = 4, column = 3, sticky = 'w')
        self.ExButton = CTkButton(master = self.InsertFrame, text = "Submit", command = self.changeEx, width=100)
        self.ExButton.grid(row = 5 , column = 2, pady = (0,20))

        # deletion 
        self.deleteFrame = CTkFrame(master = self.ebf, height = 50, width = (self.span),fg_color="transparent")
        self.deleteFrame.grid(row = 5,column = 0, sticky = 'nsew', pady = (20,0))
        self.delLabel = CTkLabel(master = self.deleteFrame, corner_radius=0, text = "Delete Items", text_color="white",font=CTkFont(family = "bookman", size=25, weight="bold"))
        self.delLabel.grid(row = 0, column = 2, sticky = 'nsew')

        self.subdelLabel = CTkLabel(master = self.deleteFrame, corner_radius=0, text = "Subscription Name:", text_color="white",font=CTkFont(family = "bookman", size=25, weight="bold"))
        self.subdelLabel.grid(row  = 1, column = 0, sticky = 'w', pady = 20)
        self.subdelEntry = CTkEntry(master = self.deleteFrame)
        self.subdelEntry.grid(row = 1, column = 2, padx = (20, 0), sticky = 'nsew', pady = 20)
        self.subdelButtom = CTkButton(master = self.deleteFrame, text = "Delete", command = self.rmSub, width=100)
        self.subdelButtom.grid(row = 1, column = 3, padx = (20,0 ), pady = 20)

        self.subdel2Label = CTkLabel(master = self.deleteFrame, corner_radius=0, text = "Expense Name:", text_color="white",font=CTkFont(family = "bookman", size=25, weight="bold"))
        self.subdel2Label.grid(row  = 2, column = 0, sticky = 'w', pady = 20)
        self.subdel2Entry = CTkEntry(master = self.deleteFrame)
        self.subdel2Entry.grid(row = 2, column = 2, padx = (20, 0), sticky = 'nsew', pady = 20)
        self.subdel2Buttom = CTkButton(master = self.deleteFrame, text = "Delete", command = self.rmExp, width=100)
        self.subdel2Buttom.grid(row = 2, column = 3, padx = (20,0 ), pady = 20)

        self.TestFrame = CTkFrame(master = self.ebf, height = 50, width = (self.span),fg_color="transparent")
        self.TestFrame.grid(row = 6,column = 0, sticky = 'nsew', pady = (50,0))


        # Graphs Tab Formatting
        self.graphTFrame = CTkFrame(master = self.gbf, height = 50, width = (self.span),fg_color="transparent")
        self.graphTFrame.grid(row = 0, column = 0, sticky = 'nsew', pady = 10)

        self.graphTitle = CTkLabel(master = self.graphTFrame, corner_radius=0, text = "Select A Graph To Observe", text_color="white",font=CTkFont(family = "bookman", size=25, weight="bold"))
        self.graphTitle.grid(row = 0, column = 5, sticky = 'nsew', pady = 20, padx = (self.span / 2.75))

        self.graphBFrame = CTkFrame(master = self.gbf, height = 50, width = (self.span),fg_color="transparent")
        self.graphBFrame.grid(row = 1, column = 0, sticky = 'nsew', pady = 10)

        self.graph1Label = CTkLabel(master = self.graphBFrame, corner_radius=0, text = "Income vs Expenses", text_color="white",font=CTkFont(family = "bookman", size=20, weight="bold"))
        self.graph1Label.grid(row = 0, column = 0, sticky = 'nsew', pady = (20,0) , padx = 100)
        self.graph2Label = CTkLabel(master = self.graphBFrame, corner_radius=0, text = "Overall Expenses", text_color="white",font=CTkFont(family = "bookman", size=20, weight="bold"))
        self.graph2Label.grid(row = 0, column = 1, sticky = 'nsew', pady = (20,0), padx = 100)
        self.graph3Label = CTkLabel(master = self.graphBFrame, corner_radius=0, text = "Budgeting Overview", text_color="white",font=CTkFont(family = "bookman", size=20, weight="bold"))
        self.graph3Label.grid(row = 0, column = 2, sticky = 'nsew', pady = (20,0), padx = 100)

        self.graph1Button = CTkButton(master = self.graphBFrame,command = self.graph1, text = "Select", width=100)
        self.graph1Button.grid(row = 1, column = 0, sticky = 'nsew', pady = 10, padx = 100)
        self.graph2Button = CTkButton(master = self.graphBFrame,command = self.graph2, text = "Select", width=100)
        self.graph2Button.grid(row = 1, column = 1, sticky = 'nsew', pady = 10, padx = 100)
        self.graph3Button = CTkButton(master = self.graphBFrame,command = self.graph3, text = "Select", width=100)
        self.graph3Button.grid(row = 1, column = 2, sticky = 'nsew', pady = 10, padx = 100)
        
    def selectFrame(self,name):
        self.homeButton.configure(fg_color=(theme) if name == "home" else "transparent")
        self.ExpensesButton.configure(fg_color=(theme) if name == "expenses" else "transparent")
        self.graphButton.configure(fg_color=(theme) if name == "graph" else "transparent")

                # show selected frame
        if name == "home":
            self.HbF.grid(row = 1, column = 0)
        else:
            self.HbF.grid_forget()
        if name == "expenses":
            self.ebf.grid(row=1, column=0)
        else:
            self.ebf.grid_forget()
        if name == "graph":
            self.gbf.grid(row=1, column=0)
        else:
            self.gbf.grid_forget()

    def goHome(self):
        self.selectFrame("home")
    def goExpenses(self):
        self.selectFrame("expenses")
    def goGraph(self):
        self.selectFrame("graph")

        
        # CTkLabel(master=self.myframe, text=f" Account balance \n ${'{:.2f}'.format(self.balance)}").grid(row=0, column=0)
    

    
        
        # CTkLabel(master=self.myframe, text=f" Savings balance \n ${'{:.2f}'.format(self.balance)}").grid(row=0, column=1)
        # CTkButton(master=self.myframe, text="Deposit",command=self.addFunds).grid(pady=25, row=1, column=0)
        # CTkButton(master=self.myframe, text="Withdrawl").grid(row=2, column=0)
        # CTkButton(master = self.myframe,text = "Transfer").grid(row= 1, column = 1)
        # self.goals_frame = MyFrame(master=self)
        # self.goals_frame.grid(row=0, column=1)
        # CTkLabel(master=self.goals_frame, text="Enter your goals:").grid(row=0, column=0)
        # self.goals_entry = CTkEntry(master=self.goals_frame)
        # self.goals_entry.grid(row=1, column=0)
        # CTkButton(master=self.goals_frame, text="Add Goal", command=self.save_goals).grid(row=2, column=0)
        
        # self.load_goals(user)
        
        # Retrieve expenses from the database'''
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        expenses = cursor.execute(f"SELECT expense FROM expenses WHERE username = '{self.user}';").fetchall()
        
        connection.close()
        # Format and display expenses
        CTkLabel(master=self.myframe, text=f"Expenses: \n").grid(pady = 25, row=4, column=0)
        for i , expense in enumerate(expenses, 4):
            CTkLabel(master = self.myframe, text = f"{expense}").grid(row = i, column = 0)'''
        
    def graph1(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        self.totalExPrice = 0
        self.subPrice = cursor.execute(f"SELECT subscription_price FROM subs WHERE username = '{self.user}';")
        for i, name in enumerate(self.subPrice):
            self.totalExPrice += name[0]
        self.expensePrice = cursor.execute(f"SELECT expense_price FROM exp WHERE username = '{self.user}';")
        for x, name in enumerate(self.expensePrice):
            self.totalExPrice += name[0]

        self.balance = cursor.execute(f"SELECT monthlyIncome FROM userInfo WHERE username = '{self.user}';")
        self.balance = self.balance = cursor.fetchone()[0]


        vals = np.array([float(self.balance), self.totalExPrice])
        labels = ["Monthly Income", "Total Expenses"]
        explosion = [0.3, 0]
        plt.pie(vals, labels = labels,explode = explosion, shadow = True, autopct='%1.1f%%')
        plt.show()
        connection.close()

    # Total Expenses Comparison 
    def graph2(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        tarr1 = []
        tarr2 = []
        explosion = []
        valCount = 0
        self.subPrice = cursor.execute(f"SELECT subscription_price FROM subs WHERE username = '{self.user}';")
        for i, name in enumerate(self.subPrice):
            tarr1.append(name[0])
            valCount += 1

        explosion.extend([0.45 for i in range(valCount)])
        valCount = 0
        self.expensePrice = cursor.execute(f"SELECT expense_price FROM exp WHERE username = '{self.user}';")
        for i, name in enumerate(self.expensePrice):
            tarr1.append(name[0])
            valCount += 1
        
        explosion.extend([0.3 for i in range(valCount)])
        self.subName = cursor.execute(f"SELECT subscription FROM subs WHERE username = '{self.user}';")
        for i, name in enumerate(self.subName):
            tarr2.append(name[0])
        
        self.expenseName = cursor.execute(f"SELECT expense FROM exp WHERE username = '{self.user}';")
        for i, name in enumerate(self.expenseName):
            tarr2.append(name[0])
    
        
        expPriceArray = np.array(tarr1)
        expNameArray = np.array(tarr2)
        plt.pie(expPriceArray, labels = expNameArray, explode=explosion, shadow = True, autopct='%1.1f%%')
        plt.show()

        connection.close()
            
    # 50 (expenses) , 30(subs / balance) , 20(savings) rule
    def graph3(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        self.expPrice = 0
        self.subs_balPrice = 0
        self.expensePrice = cursor.execute(f"SELECT expense_price FROM exp WHERE username = '{self.user}';")
        for i, name in enumerate(self.expensePrice):
             self.expPrice += name[0]

        self.subPrice = cursor.execute(f"SELECT subscription_price FROM subs WHERE username = '{self.user}';")
        for i, name in enumerate(self.subPrice):
            self.subs_balPrice += name[0]

        self.savings = cursor.execute(f"SELECT SavingBalance FROM userInfo WHERE username = '{self.user}';")
        self.savings = cursor.fetchone()[0]
        bal = cursor.execute(f"SELECT accountBalance FROM userInfo WHERE username = '{self.user}';")
        bal = cursor.fetchone()[0]
        self.subs_balPrice += bal

        self.pArr = np.array([self.expPrice, self.subs_balPrice,self.savings])
        self.nArr = np.array(["Needs","Wants","Savings"])


        fig, ax = plt.subplots()

        cmap = plt.colormaps["tab20c"]
        outer_colors = cmap(np.arange(3)*4)
        inner_colors = cmap(np.arange(3)*4)
        
        self.needarr = np.array([50,30,20])

        ax.pie(self.pArr, labels = self.nArr, pctdistance=0.85, radius = 1, colors=outer_colors, wedgeprops=dict(width = 0.3, edgecolor = 'w'), autopct='%1.1f%%')
        ax.pie(self.needarr, colors=inner_colors, autopct='%1.1f%%', pctdistance=0.75,radius = 1 - 0.3, wedgeprops=dict(width = 0.3, edgecolor = 'w'))
        
        ax.set(aspect = "equal", title = "50/30/20 Budget Rule")
        plt.show()

        connection.close()




    def refreshSubs(self):
        self.subLabel1.destroy()
        self.subLabel2.destroy()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        self.expenseName = cursor.execute(f"SELECT subscription FROM subs WHERE username = '{self.user}';")
        for i, name in enumerate(self.expenseName):
            self.subLabel1 = CTkLabel(self.subFrame, corner_radius=0, text = f"{name[0]}:", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
            self.subLabel1.grid(row = (i), column = 0, sticky = "w")

        self.balance = cursor.execute(f"SELECT subscription_price FROM subs WHERE username = '{self.user}';")
        for x, money in enumerate(self.balance):
            self.subLabel2 = CTkLabel(self.subFrame, corner_radius=0, text=f"${int(money[0]):,d}", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
            self.subLabel2.grid(row = (x), column = 2, padx = (100, 0), sticky = "e")
        connection.close()
    def refreshExp(self):

        self.expenseLabel1.destroy()
        self.expenseLabel2.destroy()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        self.expenseName = cursor.execute(f"SELECT expense FROM exp WHERE username = '{self.user}';")
        for i, name in enumerate(self.expenseName):
            self.expenseLabel1 = CTkLabel(self.expenseFrame, corner_radius=0, text = f"{name[0]}:", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
            self.expenseLabel1.grid(row = (i), column = 0, sticky = "w")

        self.balance = cursor.execute(f"SELECT expense_price FROM exp WHERE username = '{self.user}';")
        for x, money in enumerate(self.balance):
            self.expenseLabel2 = CTkLabel(self.expenseFrame, corner_radius=0, text=f"${int(money[0]):,d}", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
            self.expenseLabel2.grid(row = (x), column = 2, padx = (100, 0), sticky = "e")
        connection.close

    def rmSub(self):
        bal = self.subdelEntry.get()
        self.subdelEntry.delete(0, 'end')
        if bal:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM subs WHERE subscription = ? and username =?", (bal,self.user))
            connection.commit()
            connection.close()
        self.refreshSubs()
    
    def rmExp(self):
        bal = self.subdel2Entry.get()
        self.subdel2Entry.delete(0, 'end')
        if bal:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("DELETE FROM exp WHERE expense=? and username =?", (bal,self.user))
            connection.commit()
            connection.close()
        self.refreshExp()
        
    def changeSub(self):
        price = self.priceEntry.get()
        name = self.nameEntry.get()
        self.priceEntry.delete(0, 'end')
        self.nameEntry.delete(0,'end')
        if price:
            self.subLabel1.destroy()
            self.subLabel2.destroy()
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()    
            cursor.execute("INSERT INTO subs (username, subscription, subscription_price) VALUES (?, ?, ?) ", (self.user, name, price))

            self.expenseName = cursor.execute(f"SELECT subscription FROM subs WHERE username = '{self.user}';")
            for i, name in enumerate(self.expenseName):
                self.subLabel1 = CTkLabel(self.subFrame, corner_radius=0, text = f"{name[0]}:", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
                self.subLabel1.grid(row = (i), column = 0, sticky = "w")

            self.balance = cursor.execute(f"SELECT subscription_price FROM subs WHERE username = '{self.user}';")
            for x, money in enumerate(self.balance):
                self.subLabel2 = CTkLabel(self.subFrame, corner_radius=0, text=f"${int(money[0]):,d}", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
                self.subLabel2.grid(row = (x), column = 2, padx = (100, 0), sticky = "e")
            connection.commit()
            connection.close


    def changeEx(self):
        price = self.ExpriceEntry.get()
        name = self.ExnameEntry.get()
        self.ExpriceEntry.delete(0, 'end')
        self.ExnameEntry.delete(0,'end')
        if price:
            self.expenseLabel1.destroy()
            self.expenseLabel2.destroy()
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()    
            cursor.execute("INSERT INTO exp (username, expense, expense_price) VALUES (?, ?, ?) ", (self.user, name, price))
            self.expenseName = cursor.execute(f"SELECT expense FROM exp WHERE username = '{self.user}';")
            for i, name in enumerate(self.expenseName):
                self.expenseLabel1 = CTkLabel(self.expenseFrame, corner_radius=0, text = f"{name[0]}:", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
                self.expenseLabel1.grid(row = (i), column = 0, sticky = "w")

            self.balance = cursor.execute(f"SELECT expense_price FROM exp WHERE username = '{self.user}';")
            for x, money in enumerate(self.balance):
                self.expenseLabel2 = CTkLabel(self.expenseFrame, corner_radius=0, text=f"${int(money[0]):,d}", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
                self.expenseLabel2.grid(row = (x), column = 2, padx = (100, 0), sticky = "e")
            connection.commit()
            connection.close()
           

    def changeInc(self):
        bal = self.IncomeEntry.get()
        self.IncomeEntry.delete(0, 'end')
        if bal:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("UPDATE userInfo SET monthlyIncome=? WHERE username =?", (bal,self.user))
            self.balance = cursor.execute(f"SELECT monthlyIncome FROM userInfo WHERE username = '{self.user}';")
            self.balance = cursor.fetchone()[0]
            self.incomeLabel2.destroy()
            self.incomeLabel2 = CTkLabel(self.savingsFrame, corner_radius=0, text=f"${int(self.balance):,d}", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
            self.incomeLabel2.grid(row = 3, column = 2, padx = (100, 0), sticky = "e")
            connection.commit()
            connection.close()       

    def changeSav(self):
        bal = self.savingsEntry.get()
        self.savingsEntry.delete(0, 'end')
        if bal:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("UPDATE userInfo SET savingBalance=? WHERE username =?", (bal,self.user))
            self.balance = cursor.execute(f"SELECT SavingBalance FROM userInfo WHERE username = '{self.user}';")
            self.balance = cursor.fetchone()[0]
            self.savingsLabel2.destroy()
            self.savingsLabel2 = CTkLabel(self.savingsFrame, corner_radius=0, text=f"${int(self.balance):,d}", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
            self.savingsLabel2.grid(row = 2, column = 2, padx = (100, 0), sticky = "e")
            connection.commit()
            connection.close()        

    def changeBal(self):
        bal = self.SbalanceEntry.get()
        self.SbalanceEntry.delete(0, 'end')
        if bal:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("UPDATE userInfo SET accountBalance=? WHERE username =?", (bal,self.user))
            self.balance = cursor.execute(f"SELECT accountBalance FROM userInfo WHERE username = '{self.user}';")
            self.balance = cursor.fetchone()[0]
            self.balanceLabel2.destroy()
            self.balanceLabel2 = CTkLabel(self.savingsFrame, corner_radius=0, text=f"${int(self.balance):,d}", text_color="white",font=CTkFont(family = "bookman", size=35, weight="bold"))
            self.balanceLabel2.grid(row = 1, column = 2, padx = (100, 0), sticky = "e")
            connection.commit()
            connection.close()

    def save_goals(self):
        goal = self.goals_entry.get()
        if goal:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("INSERT INTO user_goals (username, goal) VALUES (?, ?)", (self.user, goal))
            connection.commit()
            connection.close()
            self.load_goals(self.user)
            self.goals_entry.delete(0, 'end')
        
    def load_goals(self, user):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        goals = cursor.execute(f"SELECT goal FROM user_goals WHERE username = '{user}';").fetchall()
        connection.close()
        for i, goal in enumerate(goals):
            CTkLabel(master=self.goals_frame, text=f"{i+1}. {goal[0]}").grid(row=i+3, column=0)

    def addFunds(self):
        win = CTkToplevel(self)
        win.geometry("300x300")
        
        CTkLabel(master = win, text = "How much would you like to deposit? ").pack()
        deposit = CTkEntry(master = win)
        deposit.pack()
        
        
        def help():
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()    
            amount = deposit.get()
            current_balance = cursor.execute(f"SELECT accountBalance FROM userInfo WHERE username = '{self.user}").fetchone()
            new_balance = current_balance+amount
            cursor.execute(f"UPDATE userInfo SET accountBalance = {new_balance} WHERE username = '{self.user}';")
            connection.close()
            
        CTkButton(master = win , text = "Deposit", command = help).pack()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        self.balance = cursor.execute(f"SELECT accountBalance FROM userInfo WHERE username = '{self.user}';")
        self.balance = cursor.fetchone()[0]
        
        CTkLabel(master=self.myframe, text=f" Account balance \n ${'{:.2f}'.format(self.balance)}").grid(row=0, column=0)
        
        connection.close()

