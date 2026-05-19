import mysql.connector
import hashlib


db  = mysql.connector.connect(
    user = "root",
    password = "root",
    host = "localhost" ,
    port = "3306",
    database = "bank"
)

cursor = db.cursor()

while True:
    print("1. Увійти\n2. Зареєструватись")
    c = int(input())

    if c == 1:
        l = str(input("Введіть логін :"))
        p = str(input("Введіть пароль : "))
        s = hashlib.sha256(p.encode()).hexdigest()
        cursor.execute("SELECT * FROM usert WHERE usert.login = %s" , (l , ))
        a = cursor.fetchone()
        if a is None:
            print("Користувача не знайдено!")
        elif a[2] == s:

            print("\nВхід успішний!\n")
           
            import oper.py
            break
        else:
            print("Ви десь неправильно вказали пароль або логін!")
    elif c ==2 :
        print("------------")
        i = str(input("Введіть своє Ім\'я і Прізвище\n"))
        passwor = str(input("Створіть свій пароль\n "))
        s = hashlib.sha256(passwor.encode()).hexdigest()
        cursor.execute("INSERT INTO usert(login , password) VALUES(%s , %s)" , (i , s))
        db.commit()
        print(f"Ваш логін : ", i , "\nВаш пароль : " , passwor)
        
        