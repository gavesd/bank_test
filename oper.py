import mysql.connector 
import random

db  = mysql.connector.connect(
    user = "root",
    password = "root",
    host = "localhost" ,
    port = "3306",
    database = "bank"
)

cursor = db.cursor()

while True:
    print ("1. Створити рахунок\n2. Показати всі рахунки\n3. Поповнити рахунок\n4. Зняти кошти\n5. Переказ між рахунками\n6. Історія транзакцій\n7. Вихід")
    c = int(input())
    
    if c == 1 :
        print("___________________")
        i = str(input("Ведіть своє ім\'я і прізвище : "))
        b = int(input("Введіть свій депозит : "))
        if b > 0 :
            fas =''
            for x in range(5):
                fas = fas + random.choice(list('1234567890'))
                print("Ваш код для внесення депозиту :" , fas)
                
            else :
                print("Ваш депозит додано!")
                
        cursor.execute("INSERT INTO accounts( owner, balance) VALUES (%s , %s)" , (i , b ))
        db.commit()
        break
    elif c == 2:
        i = str(input("Ведіть своє ім\'я і прізвище : "))
        cursor.execute("SELECT accounts.id ,accounts.owner , accounts.balance  FROM accounts WHERE accounts.owner = %s" , (i ,))
        rows = cursor.fetchall()
        for row in rows:
            print (f"Ваші рахунки : {row[0]}\nБаланс рахунку- {row[2]}")
            
    elif c == 3:
      d = int(input("Введіть номер рахуку : ")) 
      b_n = int(input("Сума поповнення : "))
      r1 = 'Поповнення'
      cursor.execute("UPDATE accounts SET accounts.balance = accounts.balance +%s WHERE accounts.id =%s  " , (b_n , d))
      f1 = cursor.fetchall()
      for row in f1 :
        print (f"Номер рахунку : {row[0]}\nБаланс - {row[2]}")
        print ("Рахунок поповнено ")
        db.commit()

    elif c == 4:
        d1 = int(input("Введіть номер рахуку : "))
        b_n1 = int(input("Сума зняти : "))
        m1 = 'Знятя'
        poh = 'Повернення'
        #cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (%s , %s ,%s)" , (d1,m1 , b_n1))
        cursor.execute("UPDATE accounts SET accounts.balance = accounts.balance -%s WHERE accounts.id =%s  " , (b_n1 , d1))
        f = cursor.fetchall()
        for row in f :
            print (f"Номер рахунку : {row[0]}\nБаланс - {row[2]}")
        print ("З рахунку зняті гроші ")
        db.commit()
        print("---------------------")
        print ("Якщо це не ви зняли гроші\nВведіть цифру - 1\nЯкщо це ви\nВведіть цифру - 0\n")
        a = int(input())
        if a == 0:
             print("Дякую що ви зреагували!")
            
        elif a == 1 :
            db.rollback()
            print("Вам зараз згенерується код ведіть в поле!")
            pof =''
            for x in range(5):
                pof = pof + random.choice(list('1234567890'))
                print("Ваш код для пітведження рахунку :" , pof)

            kod = str(input("Введіть код :"))
            if pof == kod :
                print("Ваші кошти повернуться зараз!")
                cursor.execute("UPDATE accounts SET accounts.balance = accounts.balance +%s WHERE accounts.id =%s  " , (b_n1 , d1))
                #cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (%s , %s ,%s)" , (d1,poh , b_n1))
        db.commit()

    elif c == 5:
        print("Виберіть ID рахунку свого , з якого будуть зняті гроші ")
        n_im = int(input())
        im = int(input("Введіть ID отримувача : "))
        q = int(input("Введіть суму : "))
        m = 'Знятя'
        r = 'Поповнення'
        try :
            db.autocommit = False
            cursor.execute("UPDATE accounts SET accounts.balance = accounts.balance -%s WHERE accounts.id =%s" , (q,n_im ))
            cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (%s , %s ,%s)" , (n_im ,m , q))
            
            cursor.execute("UPDATE accounts SET accounts.balance = accounts.balance +%s WHERE accounts.id =%s" , (q,im ))
            cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (%s , %s ,%s)" , (im ,r , q))
            print("Транзакцію було успішно реалізовано")
            db.commit()
        except mysql.connector.Error as error :
            print("Транзакцію було скасовано ")
            db.rollback()
    elif c == 6:
        t = int(input("Введіть номер рахунку (ID) :"))
        cursor.execute("SELECT * FROM transactions WHERE transactions.account_id=%s " ,(t , ))
        f1 = cursor.fetchall()
        for row in f1 :
            print (f" {row[0]}. {row[2]} Сума - {row[3]} Дата - {row[4]}")