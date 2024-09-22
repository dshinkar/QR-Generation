import mysql.connector 
#step1 connect()
x=mysql.connector.connect(host='localhost',
                        username='root',
                        password='yourpassword',
                        database='database name')
if x:
    print("Database created successfully")
else:
    print("Please try again")
#step 2 cursor()
y=x.cursor()
#step 3 execute() sql query
def create_table():
    y.execute("create table if not exists qrtable(person_name Text,address Text,course Text,course_date Date)")
def add_record(a,b,c,d):
    y.execute("insert into qrtable(person_name,address,course,course_date) values(%s,%s,%s,%s)",(a,b,c,d))
    #step 4 :commit()
    x.commit()
def read_data():
    y.execute("select * from qrtable")
    data=y.fetchall()
    return data
def delete(person):
    y.execute('delete from qrtable where person_name="{}"'.format(person))
    #step 4 :commit()
    x.commit()
def filter_person():
    y.execute("select distinct person_name from qrtable")
    data=y.fetchall()
    return data
def update(a,b,z,n):
    y.execute('update qrtable set address=%s,course=%s,course_date=%s where person_name=%s'
                ,(a,b,z,n))
    x.commit()
    data=y.fetchall()
    return data
def get_person(x):
    y.execute('select * from qrtable where person_name="{}"'.format(x))
    data = y.fetchall()
    return data
