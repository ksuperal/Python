import tkinter
import pickle
from tkinter import *
import random
from tkinter import messagebox
from tkinter import filedialog
import webbrowser

trial ={}
class Main(Frame):
    def __init__(self, master, days):
        Frame.__init__(self, master, bg="lightblue")
        self.balance = int(input("Enter your balance(at least 1000): "))
        self.grid(sticky=N + S + E + W)
        self.days = days + 1
        self.money = self.balance
        self.normFont = ("Courier New", 12)
        self.createWidgets()
        self.updateDay()

    def createWidgets(self):
        if self.balance <1000:
            print("You cannot enter the Store with current balance.")
            quit()
        else:pass
        self.tFrame = Frame(self, bg="lightblue")
        self.tFrame.grid(columnspan=2, sticky=N, pady=15)
        self.title = Label(self.tFrame, text="U market", font=("Courier New", 24, "bold"),bg="lightblue")
        self.title.grid(row=0, column=1,sticky=W + E, padx=30, pady=20)
        self.mLabel = Label(self.tFrame, text="Money: {}".format(self.money), font=self.normFont, bg="lightblue")
        self.mLabel.grid(row=1, column=1,sticky=W + E)
        self.daysLabel = Label(self.tFrame, font=self.normFont, bg="lightblue")
        self.daysLabel.grid(row=2, column=1,sticky=W + E)
        self.nextDay = Button(self.tFrame, text="Next Day", command=self.updateDay, font=("Mesquite Std", 12, "bold"),bg="yellow")
        self.nextDay.grid(row=3, column=0, pady=15, sticky=E + W + N + S)
        self.history = Button(self.tFrame, text="History", command=self.show, font=("Mesquite Std", 12, "bold"),bg="yellow")
        self.history.grid(row=3, column=1, pady=15, sticky=E + W + N + S)
        self.ready = Button(self.tFrame, text="Ready to Invest", command=self.browse, font=("Mesquite Std", 12, "bold"),bg="pink")
        self.ready.grid(row=3, column=2, pady=15, sticky=E + W + N + S)
        self.menu = BuyMenu(self)
        self.menu.grid(row=2, column=0, pady=15, sticky=E + W + N + S)

        self.inv = Inventory(self)
        self.inv.grid(row=2, column=1, pady=15, sticky=E + W + N + S )

    def updateDay(self):


        self.days -= 1

        if self.days == 1:
            messagebox.showwarning(title="Message", message="You 1 day left!")

        elif self.days == 0:
            messagebox.showinfo(title="Congratulations!",message="Profit: {} dollars".format(self.money - self.balance))
            trial["Attemp"]=(self.money - self.balance)
            filepath = filedialog.asksaveasfile(filetypes=[('All Files', '*.*')], title="Profit")
            if filepath is None:
                print("\nFile not saved\n")
            else:
                f = open(filepath.name, 'wb')
                pickle.dump(trial, f)
                f.close()
                print("\nHistory has been saved\n")
            self.deactivate()

        if self.menu.stockMenu.curselection():
            i = self.menu.stockMenu.curselection()[0]
            self.menu.stockMenu.selection_clear(first=i)
        elif self.inv.inventory.curselection():
            i = self.inv.inventory.curselection()[0]
            self.inv.inventory.selection_clear(first=i)

        self.daysLabel['text'] = "Days Left: {}".format(self.days)
        self.menu.updateVal()
    def show(self):
        filename = filedialog.askopenfile(filetypes=[('All Files', '*.*')], title="Profit")
        file = open(filename.name, "rb")
        load = pickle.load(file)

        for name, number in load.items():
            print(f"{name}: {number}")
            trial[name] = number

            print("\nAttemp loaded\n")
    def browse(self):
        webbrowser.open_new('https://www.binance.com/en')

    def purchase(self, stockI, amount, cost):
        self.inv.userInv[stockI] += amount
        self.money -= cost

        self.mLabel['text'] = "Your money: {}".format(self.money)
        self.inv.amounts.delete(stockI)
        self.inv.amounts.insert(stockI, self.inv.userInv[stockI])

    def sell(self, stockI, amount):
        cost = self.menu.prices[stockI] * amount
        self.money += cost
        self.mLabel['text'] = "Your money: {}".format(self.money)

    def deactivate(self):
        self.menu.buy['state'] = DISABLED
        self.inv.sell['state'] = DISABLED
        self.nextDay['state'] = DISABLED


class BuyMenu(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="lightblue")
        self.master = master
        self.grid(padx=60)
        self.stockList = ["Bitcoin", "Apple", "Microsoft", "ShibaCoin", "Google", "Facebook", "BinanceCoin", "Etherium"]
        self.createWidgets()
    def createWidgets(self):

        self.menuFont = ("Courier New", 10)
        self.menuTitle = Label(self, text="In U Stock", font=("Courier New", 12, "underline"),
                           bg="lightblue")
        self.menuTitle.grid(row=0, column=0)

        self.stockMenu = Listbox(self, height=8, selectmode=SINGLE, activestyle="none", font=self.menuFont, width=17)
        self.stockMenu.grid(row=1, column=0, padx=5, pady=(3, 10))

        for d in self.stockList:
            self.stockMenu.insert(END, d)

        self.pTitle = Label(self, text="Prices", font=("Courier New", 12, "underline"),
                           bg="lightblue")
        self.pTitle.grid(row=0, column=1)

        self.priceList = Listbox(self, activestyle="none", height=8, selectbackground="#ffffff",
                                 selectforeground="black", takefocus=0,
                                 font=self.menuFont, width=10)
        self.priceList.grid(row=1, column=1, pady=(3, 10))

        self.buy = Button(self, text="Buy it!", command=self.buystocks)
        self.buy.grid(row=2, column=0, columnspan=2)

    def updateVal(self):
        self.prices = self.generatePrices()
        for i in range(len(self.prices)):
            self.priceList.insert(i, self.prices[i])

    def generatePrices(self):

        a = random.randint(10, 1430)
        b = random.randint(400, 1000)
        c = random.randint(2013, 7692)
        d = random.randint(1034, 18290)
        e = random.randint(3500, 23010)
        f = random.randint(567, 2203)
        g = random.randint(1050, 7882)
        h = random.randint(1007, 4000)

        return [a, b, c, d, e, f, g, h]

    def buystocks(self):
        try:
            stockI = self.stockMenu.curselection()[0]
        except:
            messagebox.showwarning(title="Error", message="Please select a stock to buy")
            return

        w = PopupInput(self.master, money=self.master.money, stock=self.stockList[stockI],
                       stockPrice=self.prices[stockI], buy=True, )
        self.master.wait_window(w.top)
        try:
            amount = w.amount
            cost = amount * self.prices[stockI]
            self.master.purchase(stockI, amount, cost)
        except:
            return


class Inventory(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="lightblue")
        self.grid(padx=60)

        self.stockList = ["Bitcoin", "Apple", "Microsoft", "ShibaCoin", "Google", "Facebook", "BinanceCoin", "Etherium"]
        self.userInv = [0 for i in range(8)]

        self.menuFont = ("Courier New", 10)
        self.createWidgets()


    def createWidgets(self):

        Label(self, text="In Ur Stock", font=("Courier New", 12, "underline"),
                           bg="lightblue").grid()

        self.inventory = Listbox(self, height=0, font=self.menuFont, width=18, activestyle="none")
        self.inventory.grid(row=1, column=0, padx=5, pady=(3, 10))

        for i in self.stockList:
            self.inventory.insert(END, i)

        Label(self, text="Amounts", font=("Courier New", 12, "underline"),
                           bg="lightblue").grid(row=0, column=1)

        self.amounts = Listbox(self, height=0, font=self.menuFont, width=10, activestyle='none',
                               selectbackground="#ffffff", selectforeground="black")
        self.amounts.grid(row=1, column=1, pady=(3, 10))
        for i in range(8):
            self.amounts.insert(END, 0)

        self.sell = Button(self, text="Sell it!", command=self.sellstocks)
        self.sell.grid(row=2, column=0, columnspan=2)

    def sellstocks(self):
        try:
            stockI = self.inventory.curselection()[0]
        except:
            messagebox.showerror(title="Error", message="Please select a stock to sell")
            return

        w = PopupInput(self.master, self.master.money, self.stockList[stockI], self.master.menu.prices[stockI],
                       buy=False, stockI=stockI)
        self.master.wait_window(w.top)
        try:
            numSell = w.amount
            self.master.sell(stockI, numSell)

            self.userInv[stockI] -= numSell
            self.amounts.delete(stockI)
            self.amounts.insert(stockI, self.userInv[stockI])

        except:
            return


class PopupInput(Frame):
    def __init__(self, master, money, stock, stockPrice, buy=True, stockI=None):
        Frame.__init__(self, master)
        self.grid()
        self.master = master

        okayCommand = (self.register(self.isOkay), "%S")
        self.stockI = stockI

        self.money = money
        self.stock = stock
        self.stockPrice = stockPrice
        self.defFont = ("Courier New", 12)
        self.choice = "buy" if buy else "sell"
        self.top = Toplevel(master)
        self.howMuch = Label(self.top, text="How much {} stock would you like to {}?".format(stock, self.choice),
                             font=self.defFont)
        self.howMuch.grid(padx=20, pady=(5, 0), columnspan=2)

        self.userInp = Entry(self.top, font=self.defFont, validate='key', validatecommand=okayCommand)

        self.userInp.grid(columnspan=2)

        if buy:
            self.userInp.insert(0, self.money // self.stockPrice)
        elif not buy:
            self.userInp.insert(0, self.master.inv.userInv[stockI])

        self.ok = Button(self.top, text="Ok", font=self.defFont, command=self.confirmOrder)
        self.ok.grid(ipadx=25)

        self.cancel = Button(self.top, text="Cancel", font=self.defFont, command=self.destroy)
        self.cancel.grid(row=2, column=1, )

    def confirmOrder(self):
        if self.choice == "buy":
            if int(self.userInp.get()) * self.stockPrice > self.master.money:
                messagebox.showerror(title="Error!",
                                     message="You do not have enough money to buy that much {} stock".format(
                                         self.stock))

            else:
                self.amount = int(self.userInp.get())
                if messagebox.askokcancel(title="Are you sure?",message="Do you want to buy {} {} stock for {} dollars?".format(self.amount,self.stock,self.amount * self.stockPrice)):
                    self.destroy()

        elif self.choice == "sell":
            if int(self.userInp.get()) > self.master.inv.userInv[self.stockI]:
                messagebox.showerror(title="Error", message="You do not have that much of {} stock".format(self.stock))

            else:
                self.amount = int(self.userInp.get())
                if messagebox.askokcancel(title="Are you sure?",message="Do you want to sell {} {} stock for {} dollars?".format(self.amount,self.stock,self.amount * self.stockPrice)):
                    self.destroy()

    def isOkay(self, what):
        try:
            int(what)
            return True
        except:
            self.bell()
            return False

    def destroy(self):
        self.top.destroy()


root = tkinter.Tk()
root.title("U Store")
root.resizable(width=False, height=False)
days = int(input("Enter the day in market:  "))
if days <=0:
    print("Error! Please Enter Number of day.")
    quit()
else: pass
app = Main(root, days)
app.mainloop()