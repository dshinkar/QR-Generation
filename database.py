# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 13:23:07 2022

@author: Deepali
"""


import sqlite3
conn = sqlite3.connect("C:\\Users\\Sevenmentor\\sqlite\\pythonsqlite.db",check_same_thread=False)
c = conn.cursor()
#c.execute("DROP TABLE persontable;")
# Functions
def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS persontable(person_id INTEGER  PRIMARY KEY,person_name TEXT,person_no INTEGER,person_dept TEXT,person_record_date DATE)')
def add_data(person_id,person_name,person_no,person_dept,person_record_date):
	c.execute('INSERT INTO persontable(person_id,person_name,person_no,person_dept,person_record_date) VALUES (?,?,?,?,?)',(person_id,person_name,person_no,person_dept,person_record_date))
	conn.commit()

def view_all_persons():
	c.execute('SELECT * FROM persontable')
	data = c.fetchall()
	return data
def view_update():
    c.execute('select distinct person_dept from persontable')
    data = c.fetchall()
    return data

def get_department(person_dept):
    c.execute('select * from persontable where person_dept="{}"'.format(person_dept))
    data = c.fetchall()
    return data
def update(new_person_dept,new_person_record_date,person_id):
    c.execute('update persontable set person_dept=?,person_record_date=? where person_id=?',(new_person_dept,new_person_record_date,person_id))
    conn.commit()
    data=c.fetchall()
    return data
def delete(person_dept):
    c.execute('delete from persontable where person_dept="{}"'.format(person_dept))
    conn.commit()
    