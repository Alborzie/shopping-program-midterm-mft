from sqlite3 import *
from tkinter import *

#this is the python project  i preseted as my term project :)#

try:
    dbcnt = connect("shopping.db")
except:
    print("ERROR ; couldn't connect to data base, please re-download the program files")

user_loggen_in_ID = False
#-------------------------------------starting data base's health--------------------------------------#
number_of_tables = 0
try:
    query_ceate_table_users = '''
    CREATE TABLE Users(
    id INTEGER PRIMARY KEY,
    username CHAR(25) NOT NULL,
    password CHAR(25) NOT NULL,
    address CHAR(75) NOT NULL,
    comment CHAR(100))'''

    dbcnt.execute(query_ceate_table_users)
except OperationalError:
    number_of_tables += 1

try:
    query_ceate_table_products = '''
    CREATE TABLE Products(
    id INTEGER PRIMARY KEY,
    ProductName CHAR(25) NOT NULL,
    ProductPrice INTEGER NOT NULL,
    ProductQuantitty INTEGER NOT NULL)'''

    dbcnt.execute(query_ceate_table_products)
except OperationalError:
    number_of_tables += 1

try:
    query_ceate_table_final_shops = '''
    CREATE TABLE FinalShops(
    id INTEGER PRIMARY KEY,
    userID INTEGER NOT NULL,
    productID INTEGER NOT NULL,
    boughtQNT INTEGER NOT NULL,
    totalPrice INTEGER NOT NULL)'''

    dbcnt.execute(query_ceate_table_final_shops)
except OperationalError:
    number_of_tables += 1

if number_of_tables == 3:
    print("SUCSESS ; all the needed information needed to use the program are available")
else:
    print("ERROR ; the files for this program are damaged, please re-download them for the program to work")

###################################################################################################

#---------------------------------------------function---------------------------------------------#
def validation(username:str, passw:str, confirmation_passw:str, info:list):
        if passw != confirmation_passw:
            sbmt_submition_state_lbl.configure(text="ERROR:Your password and confirmation don't match!", fg="red")
            return False
        
        if len(passw) < 8:
            sbmt_submition_state_lbl.configure(text="ERROR:Password needs to be t least 8 characters!", fg="red")
            return False
        
        if (username,) in info:
            sbmt_submition_state_lbl.configure(text="ERROR:Username already picked!", fg="red")
            return False

        
        special_character_lst = ["!","@","#","$","%","^","&","*","~","/",]
        numbers_lst = ["1","2","3",'4','5','6',"7","8","9","0"]
        password_has_letters = False
        password_has_special = False
        password_has_number = False
        
        for item in special_character_lst:
            if item in passw:
                password_has_special = True
                break
        
        for i in range(65,91):
            if chr(i) in passw.upper():
                password_has_letters = True
                break
        
        for item in numbers_lst:
            if item in passw:
                password_has_number = True
                break
        
        if not password_has_letters:
            sbmt_submition_state_lbl.configure(text="ERROR:password has to contain letters!!", fg="red")
            return False
        
        if not password_has_special:
            sbmt_submition_state_lbl.configure(text="ERROR:password has to have at least one special character!", fg="red")
            return False
        
        if not password_has_number:
            sbmt_submition_state_lbl.configure(text="ERROR:password has to have numbers!", fg="red")
            return False
        
        return True

def submit_new_user():
    
    username = sbmt_username_entry.get()
    password = sbmt_password_entry.get()
    confirmation_password = sbmt_confirmation_password_entry.get()
    address = sbmt_address_entry.get()

    if username == "" or password == "" or confirmation_password == "" or address == "":
        sbmt_submition_state_lbl.configure("ERROR ; all fields have to be filled!", fg="red")
        return

    query_select_username = '''SELECT username FROM Users'''
    all_usernames = dbcnt.execute(query_select_username)

    is_validated = validation(username, password, confirmation_password, all_usernames)

    if is_validated:
        query_insert = '''INSERT INTO Users(username, password, address)
                        VALUES(?,?,?)'''
        dbcnt.execute(query_insert, (username, password, address))
        dbcnt.commit()

        sbmt_submition_state_lbl.configure(text="SUCCESS ; new user added succesfully", fg="green")

    sbmt_username_entry.delete(0, "end")
    sbmt_password_entry.delete(0, "end")
    sbmt_confirmation_password_entry.delete(0, "end")
    sbmt_address_entry.delete(0, "end")

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        login_state_lbl.configure(text="ERROR ; all fields have to be filled!", fg="red")

    query_select_id = '''SELECT id,username FROM Users WHERE username=? and password=?'''
    result_query_select_all = dbcnt.execute(query_select_id, (username, password)).fetchall()
    
    if result_query_select_all == []:
        login_state_lbl.configure(text="ERROR ; wrong username or password!", fg="red")
        return
    else:
        login_state_lbl.configure(text="SUCCESS ; logged in ", fg="green")

        global user_loggen_in_ID
        user_loggen_in_ID = result_query_select_all[0][0]
        
        btn_logout.configure(state=ACTIVE)
        btn_shop.configure(state=ACTIVE)
        btn_myshop.configure(state=ACTIVE)
        btn_login.configure(state=DISABLED)

        
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        username_entry.configure(state=DISABLED)
        password_entry.configure(state=DISABLED)

        if result_query_select_all[0][1] == "admin":
            btn_admin_pannel.configure(state=ACTIVE)
        
def logout():
    global user_loggen_in_ID
    if user_loggen_in_ID == 1 :
        btn_admin_pannel.configure(state=DISABLED)
    
    user_loggen_in_ID = FALSE

    login_state_lbl.configure(text="SUCCESS ; logged out ", fg="green")

    btn_logout.configure(state=DISABLED)
    btn_shop.configure(state=DISABLED)
    btn_myshop.configure(state=DISABLED)
    btn_login.configure(state=ACTIVE)

    username_entry.configure(state=NORMAL)
    password_entry.configure(state=NORMAL)

def submit():
    submit_tplvl = Toplevel(win)
    submit_tplvl.geometry("250x600")

    sbmt_username_lbl = Label(submit_tplvl, text="username :")
    sbmt_username_lbl.pack(pady=5)

    global sbmt_username_entry
    sbmt_username_entry = Entry(submit_tplvl, width=25)
    sbmt_username_entry.pack(pady=5)

    sbmt_password_lbl = Label(submit_tplvl, text="password :")
    sbmt_password_lbl.pack(pady=5)

    global sbmt_password_entry
    sbmt_password_entry = Entry(submit_tplvl, width=25)
    sbmt_password_entry.pack(pady=5)

    sbmt_confirmation_password_lbl = Label(submit_tplvl, text="confirmation password :")
    sbmt_confirmation_password_lbl.pack(pady=5)

    global sbmt_confirmation_password_entry
    sbmt_confirmation_password_entry = Entry(submit_tplvl, width=25)
    sbmt_confirmation_password_entry.pack(pady=5)

    sbmt_address_lbl = Label(submit_tplvl, text="address :")
    sbmt_address_lbl.pack(pady=5)

    global sbmt_address_entry
    sbmt_address_entry = Entry(submit_tplvl, width=25)
    sbmt_address_entry.pack(pady=5)

    sbmt_submit_new_user_btn = Button(submit_tplvl, text="submit submit new user", command=submit_new_user)
    sbmt_submit_new_user_btn.pack(pady=5)

    global sbmt_submition_state_lbl
    sbmt_submition_state_lbl = Label(submit_tplvl, text="")
    sbmt_submition_state_lbl.pack(pady=5)

    submit_tplvl.mainloop()

def update_shopping_info(lst_box:Listbox):
    lst_box.delete(0,"end")
    query = '''SELECT * FROM Products'''
    result = dbcnt.execute(query)
    rows = result.fetchall()
    for item in rows:
        info = f"id:{item[0]}, name:{item[1]}, price(per1):{item[2]}, quantity:{item[3]}"
        lst_box.insert("end", info)

def finalShop():
    id = shop_productID_entry.get()
    qnt = shop_productQNT_entry.get()
    
    if id == "" or qnt == "":
        final_shop_state_lbl.configure(text="ERROR ; all fields have to be filled", fg="red")
        return
    
    query = '''SELECT id,ProductQuantitty,ProductPrice FROM products where id==?'''
    result = dbcnt.execute(query, (id,))
    rows = result.fetchall()
    
    if rows == []:
        final_shop_state_lbl.configure(text="ERROR:such id does not exist", fg="red")
        return
    
    real_qnt = int(rows[0][1])

    if int(qnt) > real_qnt:
        final_shop_state_lbl.configure(text="ERROR:this item isnt available for such amounts", fg="red")
        return
    
    total_price = int(qnt)*int(rows[0][2])
    
    query2 = '''INSERT INTO FinalShops(userID,ProductID,boughtQNT,totalPrice) VALUES(?,?,?,?)'''
    dbcnt.execute(query2, (user_loggen_in_ID, id, qnt,total_price))
    dbcnt.commit()
    
    #========================== update products table =======================#
    newqnt = real_qnt - int(qnt)

    query3 = '''UPDATE products SET ProductQuantitty=? WHERE id=?'''
    dbcnt.execute(query3, (newqnt, id))
    dbcnt.commit()

    shop_productID_entry.delete(0, "end")
    shop_productQNT_entry.delete(0, "end")

    update_shopping_info(sh_lstbox)
    final_shop_state_lbl.configure(text="SUCCES ; ordered product succesfully", fg="green")

def shop():
    shop_tplvl = Toplevel(win)
    shop_tplvl.geometry("500x500")

    global sh_lstbox
    sh_lstbox = Listbox(shop_tplvl, width=400)
    sh_lstbox.pack()
    update_shopping_info(sh_lstbox)

    shop_productID_lbl = Label(shop_tplvl, text="Product ID :")
    shop_productID_lbl.pack(pady=5)

    global shop_productID_entry
    shop_productID_entry = Entry(shop_tplvl, width=10 )
    shop_productID_entry.pack(pady=5)

    shop_productQNT_lbl = Label(shop_tplvl, text="Product QNT :")
    shop_productQNT_lbl.pack(pady=5)
    
    global shop_productQNT_entry
    shop_productQNT_entry = Entry(shop_tplvl, width=15 )
    shop_productQNT_entry.pack(pady=5)

    global final_shop_state_lbl
    final_shop_state_lbl = Label(shop_tplvl, text="")
    final_shop_state_lbl.pack(pady=5)

    btn_finalShop = Button(shop_tplvl, text="finallize this order", command=finalShop)
    btn_finalShop.pack(pady=5)

    shop_tplvl.mainloop()

def myshop():
    myshop_tplvl = Toplevel(win)
    myshop_lstbox = Listbox(myshop_tplvl, width=100)
    myshop_lstbox.pack()
    query = '''SELECT * FROM FinalShops WHERE UserID = ?'''
    result = dbcnt.execute(query, (user_loggen_in_ID,)).fetchall()

    for item in result:
        info = f"order id:{item[0]}, user id:{item[1]}, product id:{item[2]}, quantity:{item[3]}, total price:{item[4]}"
        myshop_lstbox.insert("end", info)

    myshop_tplvl.mainloop()

def add_products_to_db():
    name = admin_tplvl_product_name_entry.get()
    price = admin_tplvl_product_price_entry.get()
    qnt = admin_tplvl_productQNT_entry.get()
    if name == "" or price == "" or qnt == "":
        admin_tplvl_adding_products_state_lbl.configure(text="ERROR ; all fields have to be filled!", fg="red")
        return
    else:
        query_insert_product = '''INSERT INTO products(ProductName, ProductPrice, ProductQuantitty)
                                VALUES(?,?,?)'''
        dbcnt.execute(query_insert_product, (name,price,qnt))
        dbcnt.commit()
        admin_tplvl_adding_products_state_lbl.configure(text="SUCCESS ; product data added to data base!", fg="green")

        
def admin_pannel():
    admin_tplvl = Toplevel(win)
    admin_tplvl.geometry("350x500")

    admin_tplvl_product_name_lbl = Label(admin_tplvl, text="Product name :")
    admin_tplvl_product_name_lbl.pack(pady=5)
    
    global admin_tplvl_product_name_entry
    admin_tplvl_product_name_entry = Entry(admin_tplvl, width=10 )
    admin_tplvl_product_name_entry.pack(pady=5)

    admin_tplvl_productQNT_lbl = Label(admin_tplvl, text="Product QNT :")
    admin_tplvl_productQNT_lbl.pack(pady=5)

    global admin_tplvl_productQNT_entry
    admin_tplvl_productQNT_entry = Entry(admin_tplvl, width=10 )
    admin_tplvl_productQNT_entry.pack(pady=5)

    admin_tplvl_product_price_lbl = Label(admin_tplvl, text="Product price(per1) :")
    admin_tplvl_product_price_lbl.pack(pady=5)

    global admin_tplvl_product_price_entry
    admin_tplvl_product_price_entry = Entry(admin_tplvl, width=10 )
    admin_tplvl_product_price_entry.pack(pady=5)

    global admin_tplvl_adding_products_state_lbl
    admin_tplvl_adding_products_state_lbl = Label(admin_tplvl, text="")
    admin_tplvl_adding_products_state_lbl.pack(pady=5)

    btn_admin_add_products_to_db = Button(admin_tplvl, text="add products to database", command=add_products_to_db)
    btn_admin_add_products_to_db.pack(pady=5)




    admin_tplvl.mainloop()


###################################################################################################

##########------------------------------------visual-------------------------------------##########
win = Tk()
win.geometry("300x600")

username_msg_lbl = Label(win, text="username :")
username_msg_lbl.pack(pady=5)

username_entry = Entry(win, width=25)
username_entry.pack(pady=5)

password_msg_lbl = Label(win, text="password :")
password_msg_lbl.pack(pady=5)

password_entry = Entry(win, width=25)
password_entry.pack(pady=5)

login_state_lbl = Label(win, text="")
login_state_lbl.pack(pady=5)

btn_login = Button(win, text="login", command=login)
btn_login.pack(pady=5)

btn_logout = Button(win, text="logout", command=logout, state=DISABLED)
btn_logout.pack(pady=5)

btn_submit = Button(win, text="submit", command=submit)
btn_submit.pack(pady=5)

btn_shop = Button(win, text="shop", command=shop, state=DISABLED)
btn_shop.pack(pady=5)

btn_myshop = Button(win, text="myshop", command=myshop, state=DISABLED)
btn_myshop.pack(pady=5)

btn_admin_pannel = Button(win, text="admin pannel", command=admin_pannel, state=DISABLED)
btn_admin_pannel.pack(pady=5)

win.mainloop()