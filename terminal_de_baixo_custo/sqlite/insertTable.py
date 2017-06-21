#!/usr/bin/python

import sqlite3 as lite
import sys

con = lite.connect('server.db')

with con:
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS Bitcoin_Adresses")
	cur.execute("DROP TABLE IF EXISTS Transaction_Info")
	cur.execute("CREATE TABLE Bitcoin_Adresses(id INTEGER PRIMARY KEY, private_address TEXT, display_address TEXT, time_added TEXT)")
	cur.execute("CREATE TABLE Transaction_Info(id INTEGER PRIMARY KEY, transaction_text TEXT NOT NULL UNIQUE, verified TEXT, time_added TEXT)")