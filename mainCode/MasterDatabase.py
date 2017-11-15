import sqlite3


def createDatabase():
	conn=sqlite3.connect('/home/pi/Documents/PeopleTracker-C4C/HTML/mainDatabase.db')
	
	curs=conn.cursor()
	curs.execute('''CREATE TABLE Persian (date text, curr, Total)''')
	curs.execute('''CREATE TABLE Asian (date text, currn, Total)''')
	curs.execute('''CREATE TABLE American (date text, currn, Total)''')
	curs.execute('''CREATE TABLE Latin (date text, currn, Total)''' )
	curs.execute('''CREATE TABLE Italian (date text, currn, Total)''' )

	conn.commit()
	conn.close()

createDatabase()
