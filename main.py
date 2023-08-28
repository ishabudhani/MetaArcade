
import mysql.connector

x = mysql.connector.connect(host='localhost', user='root', passwd='admin')
y = x.cursor()

try:
    y.execute('create database nft')
    y.execute('use nft')
    y.execute('create table buy(event varchar(10), owner_address varchar(15),img_name varchar(40), price varchar(10))')
    y.execute("insert into buy values ('Listed','XCTR12','Crown the Brown.jpg','29.11 E')")
    y.execute("insert into buy values ('Listed','ASFV45','Eric Pause.jpg','31.09 E')")
    y.execute("insert into buy values ('Listed','ZJDO45','Amoureux.jpg','23.01 E')" )
    y.execute("insert into buy values ('Listed','VJIS09','Macaco.jpg','39.99 E')")
    y.execute("insert into buy values ('Listed','NVHI87','Margarita.jpg','45.92 E')")
    y.execute("insert into buy values ('Listed','MNOQ91','X.jpg','47.09 E')")
    y.execute("insert into buy values ('Listed','CDOS34','Sotheby.png','27.87 E')")

    x.commit()
except:
    y.execute('use nft')
    y.execute('select * from buy')
    allrec = y.fetchall()
    img_name = []
    for i in allrec:
        img_name += [i[2]]


from tkinter import *
from tkinter import ttk
import tkinter
from PIL import ImageTk, Image

root = Tk()
root.title('Meta Arcade')
root.geometry("1000x500")
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)
sec = Frame(main_frame)
sec.pack(fill=X, side=BOTTOM)
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
y_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
y_scrollbar.pack(side=RIGHT, fill=Y)
my_canvas.configure(yscrollcommand=y_scrollbar.set)
my_canvas.bind("<Configure>", lambda e: my_canvas.config(scrollregion=my_canvas.bbox(ALL)))
second_frame = Frame(my_canvas)
my_canvas.create_window((0, 0), window=second_frame, anchor="nw")


def buy(pc):
    def ask():
        name = e.get()
        if len(name) != 6:
            text = Label(win2, text='Address should have exactly 6 characters.Click on back and Try Again',
                         font=("Times New Roman", 15, "bold"), fg='blue')
            text.place(x=1, y=30)
        else:
            text = Label(win2, text='YAY!YOU HAVE BROUGHT THIS ', font=("Times New Roman", 20, "bold"), fg='black')
            text.place(x=1, y=200)
            y.execute("update buy set event='unlisted' where img_name='{}'".format(pc))
            x.commit()
            y.execute("update buy set owner_address='{}'".format(name) + " where img_name='{}'".format(pc))
            x.commit()

    win2 = Toplevel(root)
    win2.geometry("1000x500")
    back = Button(win2, text='BACK', command=win2.destroy)
    back.pack(side='bottom', anchor='sw')
    l = Label(win2, text='Enter your address', font=("Arial", 10, "bold"))
    l.place(x=5, y=5)
    e = Entry(win2, width=20, font=("Arial", 10, "bold"))
    e.place(x=150, y=5)
    b = Button(win2, text='BUY', command=ask)
    b.pack(side='bottom')
    win2.mainloop()


def image(n):
    global img_name
    image = img_name[n]
    y.execute("select event from buy where img_name= '{}'".format(image))
    rec = y.fetchone()
    for i in rec:
        l = i
    win = Toplevel(root)
    win.geometry("1000x500")
    if l == 'Listed':
        btn = Button(win, text='BUY ', command=lambda: buy(image))
        btn.pack(side='bottom')
    else:
        p = Label(win, text='THIS NFT IS ALREADY SOLD', padx=20, pady=20)
        p.pack()

    back = Button(win, text='BACK', command=win.destroy)
    back.pack(side='bottom', anchor='sw')
    frame = Frame(win, width=600, height=400)
    frame.pack()
    frame.place(anchor='center', relx=0.5, rely=0.5)
    img = ImageTk.PhotoImage(Image.open(image))
    label = Label(frame, image=img)
    label.pack()
    y.execute("select owner_address from buy where img_name='{}'".format(image))
    rec = y.fetchone()
    for i in rec:
        owner_address = i
    y.execute("Select price from buy where img_name= '{}'".format(image))
    rec2 = y.fetchone()
    for i in rec2:
        price = i
    p = Label(win, text='IMAGE NAME= ' + img_name[
        n] + '                                    ' + 'PRICE=' + price + '                          ' + ' OWNER_ADDRESS =                  ' + owner_address,
              padx=20, pady=20)
    p.pack()
    win.mainloop()


def topnft():
    win = Toplevel(root)
    win.geometry("700x500")
    win.resizable(False, False)
    frm = Frame(win)
    frm.pack()
    tab = ttk.Treeview(frm, column=(1, 2), show='headings', height=20)
    tab.pack()
    tab.heading(1, text='NFT Name')
    tab.heading(2, text='Price')
    y.execute('select img_name,price from buy order by price desc ')
    for i in y:
        tab.insert('', 'end', values=i)
    back = Button(win, text='BACK', command=win.destroy)
    back.pack(side='bottom', anchor='sw')
    win.mainloop()


btn = Button(root, text="TOP NFT PRICES", command=topnft, font=('Times New Roman', 20), bg='white', fg='black').place(
    x=400, y=200)


def listed():
    win = Toplevel(root)
    win.geometry("700x500")
    win.resizable(False, False)
    frm = Frame(win)
    frm.pack()


tab = ttk.Treeview(frm, column=(1, 2), show='headings', height=20)
tab.pack()
tab.heading(1, text='NFT Name')
tab.heading(2, text='Price')
y.execute("select img_name,price from buy where event='Listed'")
for i in y:
    tab.insert('', 'end', values=i)
back = Button(win, text='BACK', command=win.destroy)
back.pack(side='bottom', anchor='sw')
win.mainloop()

bbtn = Button(root, text="LISTED NFT'S", command=listed, font=('Times New Roman', 20), bg='white', fg='black').place(
    x=400, y=300)


def unlisted():
    win = Toplevel(root)
    win.geometry("700x500")
    win.resizable(False, False)
    frm = Frame(win)


frm.pack()

tab = ttk.Treeview(frm, column=(1, 2), show='headings', height=20)
tab.pack()
tab.heading(1, text='NFT Name')
tab.heading(2, text='Price')
sql = 'select img_name,price from buy where event= "unlisted"'
y.execute(sql)
rec = y.fetchall()
for i in rec:
    tab.insert('', 'end', values=i)
back = Button(win, text='BACK', command=win.destroy)
back.pack(side='bottom', anchor='sw')
win.mainloop()
bbtn = Button(root, text="UNLISTED NFT'S", command=unlisted, font=('Times New Roman', 20), bg='white',
              fg='black').place(x=400, y=400)


def sell():
    def search():
        name = e.get()
        y.execute("select img_name from buy where owner_address='{}'".format(name))
        rec = y.fetchall()
        if len(rec) > 0:
            def change():
                found = 0
                nft = e2.get()
                y.execute('select img_name from buy')
                rec = y.fetchall()
                for i in rec:
                    for j in i:
                        if nft.lower() == j.lower():
                            found = 1
                price = e3.get()
                if found == 1:
                    y.execute("update buy set event='Listed' where img_name='{}'".format(nft))
                    y.execute("update buy set price='{}'".format(price + 'E') + " where img_name='{}' ".format(nft))
                    L = Label(win, text='This NFT is put on sale.Go and check it out now', font=('Arial', 15),
                              bg='white').place(x=10, y=450)
                    x.commit()
                else:
                    L = Label(win, text='This NFT does not exist in records.Try Again', font=('Arial', 15),
                              bg='white').place(x=10, y=450)

            t = Label(win, text='You own the following NFTs-', font=('Times New Roman', 20)).place(x=10, y=40)
            frm = Frame(win)
            frm.pack()
            frm.place(anchor='center', relx=0.2, rely=0.2)
            tab = ttk.Treeview(frm, column=(1), show='headings', height=5)
        tab.pack()
        tab.heading(1, text='NFT Name')
        for i in rec:
            tab.insert('', 'end', values=i)

        t2 = Label(win, text='Enter the name of the NFT name you want to Sell', font=('Arial', 15), fg='red').place(
            x=10, y=250)
        e2 = Entry(win, width=20, font=("Arial", 10, "bold"))
        e2.place(x=10, y=300)
        t3 = Label(win, text='Enter the price in Ethereum', font=('Arial', 15), fg='red').place(x=10, y=350)
        e3 = Entry(win, width=20, font=("Arial", 10, "bold"))
        e3.place(x=10, y=400)
        btn = Button(win, text='SELL', command=change).place



back = Button(win, text='BACK', command=win.destroy)
back.pack(side='bottom', anchor='sw')
t = Label(win, text="You don't own any NFT.Buy one NFT and try again", font=('Times New Roman', 15), fg='blue').place(
    x=5, y=40)

win = Toplevel(root)
win.geometry('800x700')
win.resizable(False, False)
t = Label(win, text='Note-You can only sell the NFTs that you have brought', font=('Times New Roman', 15)).place(x=0,
                                                                                                                 y=10)
l = Label(win, text='Enter your address', font=("Arial", 10, "bold")).place(x=5, y=40)
e = Entry(win, width=15, font=("Arial", 10, "bold"))
e.place(x=130, y=40)
okay_btn = Button(win, text='OK', command=search, width=2, height=1).place(x=240, y=40)

sell_btn = Button(root, text="SELL NFT", command=sell, font=('Times New Roman', 20), bg='white', fg='black').place(
    x=400, y=500)

second_frame.configure(bg='white')
l = tkinter.Label(root, text='Welcome to Meta Arcade', font=("Times New Roman", 50), fg="black").place(x=300, y=5)
l = tkinter.Label(root, text='Click On The NFT To View It', font=("Times New Roman", 35)).place(x=325, y=90)


btn = Button(second_frame, text=f"Crown The Brown", command=lambda: image(1)).grid(row=20, column=10, pady=20, padx=20)

btn = Button(second_frame, text=f"Eric Pause", command=lambda: image(2)).grid(row=30, column=10, pady=20, padx=20)

btn = Button(second_frame, text=f"Amoureux", command=lambda: image(3)).grid(row=40, column=10, pady=20, padx=20)
btn = Button(second_frame, text=f"Macaco", command=lambda: image(4)).grid(row=50, column=10, pady=20, padx=20)

btn = Button(second_frame, text=f"Margarita", command=lambda: image(5)).grid(row=60, column=10, pady=20, padx=20)

btn = Button(second_frame, text=f"X", command=lambda: image(6)).grid(row=70, column=10, pady=20, padx=20)

btn = Button(second_frame, text=f"Sotheby", command=lambda: image(7)).grid(row=80, column=10, pady=20, padx=20)

exit_button = Button(root, text='EXIT', command=root.destroy)
exit_button.pack(side='bottom', anchor='se', pady=10, padx=10)

root.mainloop()
