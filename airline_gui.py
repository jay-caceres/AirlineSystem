import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication,QMainWindow, QDialog, QLabel, QLineEdit,QMessageBox
from PyQt5.uic import loadUi
import psycopg2
from ast import literal_eval
import string
import random
import datetime


#maybe put #ofpassengers in the beginning to calculate cost

def print_psycopg2_exception(err):
	# get details about the exception
	err_type, err_obj, traceback = sys.exc_info()

	# get the line number when exception occured
	line_num = traceback.tb_lineno
	# print the connect() error
	print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
	print ("psycopg2 traceback:", traceback, "-- type:", err_type)

	# psycopg2 extensions.Diagnostics object attribute
	print ("\nextensions.Diagnostics:", err.diag)

	# print the pgcode and pgerror exceptions
	print ("pgerror:", err.pgerror)
	print ("pgcode:", err.pgcode, "\n")

class main(QMainWindow):
	def __init__(self):
		super(main,self).__init__()
		loadUi("form.ui", self)
		self.searchButton.clicked.connect(self.searchfunction)
		self.searchButton.clicked.connect(self.gotoflights)
		self.checkin.clicked.connect(self.gotocheckin)
		self.clerk.clicked.connect(self.gotoclerkside)
		self.dialog = flights_lists()
		self.departure.currentTextChanged.connect(self._updateCombo2)
	def _updateCombo2(self, text):
		self.arrival.clear()
		if text == "JFK":
			self.arrival.addItems(("HOU", "ORD", "LAX", "MIA"))
		elif text == "LAX":
			self.arrival.addItems(("HOU", "ORD", "MIA","JFK"))
		elif text == "ORD":
			self.arrival.addItems(("HOU", "MIA", "LAX","JFK"))
		elif text == "MIA":
			self.arrival.addItems(("HOU", "ORD", "LAX","JFK"))
		elif text == "HOU":
			self.arrival.addItems(("ORD", "LAX","JFK","MIA"))
	def gotocheckin(self):
		f=checkin()
		widget.addWidget(f)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def searchfunction(self):
		departure_airport = str(self.departure.currentText())
		arrival_airport = str(self.arrival.currentText())
		passenger_nums = str(self.pass_num.currentText())
		month = str(self.month.currentText())
		self.dialog.setValue(departure_airport,arrival_airport,month)
		self.dialog.setPass(passenger_nums)
		#self.dialog.show()

	def gotoflights(self):
		f=flights_lists()
		widget.addWidget(f)
		widget.setCurrentIndex(widget.currentIndex()+1)
	def gotoclerkside(self):
		f=clerkside()
		widget.addWidget(f)
		widget.setCurrentIndex(widget.currentIndex()+1)

class checkin(QMainWindow):
	def __init__(self):
		super(checkin,self).__init__()
		loadUi("checkin.ui", self)
		self.load.clicked.connect(self.loadDatas)
		self.backbutton.clicked.connect(self.gotomain)
		self.checkinFinal.clicked.connect(self.que)

		self.cancelBtn.clicked.connect(self.cancel)
	def cancel(self):
		tid = self.cancelEdit.text()
		cancel1 = """
DELETE FROM ticket WHERE ticket_no = '{a}';
""".format(a=tid)
		with open('password.txt') as f:
			lines = [line.rstrip() for line in f]
		username = lines[0]
		pg_password = lines[1]
		conn = psycopg2.connect(database = "COSC3380", user = username, password = pg_password, host="code.cs.uh.edu")
		cursor = conn.cursor()
		cursor.execute(cancel1)
		if(cursor.rowcount>0):
			error_dialog = QtWidgets.QErrorMessage()
			error_dialog.showMessage('Succesfully Cancelled')
			error_dialog.exec_()

			

		else:			
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText('Please Recheck Ticket No.')
			msg.setWindowTitle("Error")
			msg.exec_()


		conn.commit()
		cursor.close()
		conn.close()
		transaction_queries.write(cancel1)

	def que(self):
		ticket1 = self.ticketnum.text()

		confirm = """UPDATE boarding_passes
SET confirmed = 'Confirmed' WHERE ticket_no = '{a}'""".format(a=ticket1)
		with open('password.txt') as f:
			lines = [line.rstrip() for line in f]
		username = lines[0]
		pg_password = lines[1]
		conn = psycopg2.connect(database = "COSC3380", user = username, password = pg_password, host="code.cs.uh.edu")
		cursor = conn.cursor()
		cursor.execute(confirm)
		if(cursor.rowcount>0):
			error_dialog = QtWidgets.QErrorMessage()
			error_dialog.showMessage('Succesfully Checked In!')
			error_dialog.exec_()

			

		else:			
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText('Please Recheck Ticket No.')
			msg.setWindowTitle("Error")
			msg.exec_()
		conn.commit()
		cursor.close()
		conn.close()
		sql.write(confirm)

	def gotocheckinFinal(self):
		f=finalcheckin()
		widget.addWidget(f)
		widget.setCurrentIndex(widget.currentIndex()+1)
	def loadDatas(self):
		ticket = self.ticketnum.text()

		clerk_query = """SELECT * FROM boarding_passes WHERE ticket_no = '{a}';""".format(a=ticket)
		sql.write(clerk_query)
		with open('password.txt') as f:
			lines = [line.rstrip() for line in f]
		username = lines[0]
		pg_password = lines[1]
		conn = psycopg2.connect(database = "COSC3380", user = username, password = pg_password, host="code.cs.uh.edu")
		cursor = conn.cursor()
		try:
			cursor.execute(clerk_query)
		except Exception as err:
			print_psycopg2_exception(err)
		data = cursor.fetchall()
		self.table.setRowCount(0)

		for row_number, row_data in enumerate(data):
			self.table.insertRow(row_number)
			for column_number, datas in enumerate(row_data):
				self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(datas)))

	def gotomain(self):
		f=main()
		widget.addWidget(f)
		widget.setCurrentIndex(widget.currentIndex()+1)

class finalcheckin(QMainWindow):
	def __init__(self):
		super(finalcheckin,self).__init__()
		loadUi("finalcheckin.ui", self)
		self.backbutton1.clicked.connect(self.gotomain)

	def gotomain(self):
		f=main()
		widget.addWidget(f)
		widget.setCurrentIndex(widget.currentIndex()+1)



class clerkside(QMainWindow):
	def __init__(self):
		super(clerkside,self).__init__()
		loadUi("clerk.ui", self)
		self.load_clerk.clicked.connect(self.loadData)
		self.insert.clicked.connect(self.search)
		self.insert_1.clicked.connect(self.search_1)
		self.backs.clicked.connect(self.gotomain3)



	def loadData(self):
		clerk_query = """SELECT * FROM flight_leg WHERE seats_available > 0;"""
		sql.write(clerk_query)
		with open('password.txt') as f:
			lines = [line.rstrip() for line in f]
		username = lines[0]
		pg_password = lines[1]
		conn = psycopg2.connect(database = "COSC3380", user = username, password = pg_password, host="code.cs.uh.edu")
		cursor = conn.cursor()
		try:
			cursor.execute(clerk_query)
		except Exception as err:
			print_psycopg2_exception(err)
		data = cursor.fetchall()
		self.tableWidget1.setRowCount(0)

		for row_number, row_data in enumerate(data):
			self.tableWidget1.insertRow(row_number)
			for column_number, datas in enumerate(row_data):
				self.tableWidget1.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(datas)))
	def search(self):
		flight_id = self.fid.text()
		air_name = self.air_name.text()
		day = self.day.text()


		with open('password.txt') as f:
			lines = [line.rstrip() for line in f]
		username = lines[0]
		pg_password = lines[1]
		conn = psycopg2.connect(database = "COSC3380", user = username, password = pg_password, host="code.cs.uh.edu")
		cursor1 = conn.cursor()

		insert_query = """INSERT INTO flights VALUES({a},'{b}','{c}');""".format(a=int(flight_id), b=air_name,c=day)
		sql.write(insert_query)
		try:
			if(cursor1.execute(insert_query) == None):
				error_dialog = QtWidgets.QErrorMessage()
				error_dialog.showMessage('Succesfully Inserted Flight')
				error_dialog.exec_()

			

		except psycopg2.Error as err:
			
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText('Invalid Flight Insertion')
			msg.setWindowTitle("Error")
			msg.exec_()


			#FIX THIS TO WORK
		

		conn.commit()
		cursor1.close()
		conn.close()


		
		

	def search_1(self):
		flight_id = self.fid_1.text()
		leg_no = self.leg_no.text()
		dt = self.depar.dateTime()
		dt_string = dt.toString(self.depar.displayFormat())
		at = self.arriv.dateTime()
		ar_string = at.toString(self.arriv.displayFormat())
		departure_airport = str(self.froms.currentText())
		arrival_airport = str(self.to.currentText())
		status = self.status.text()
		seats = self.seats.value()

		inserts = """INSERT INTO FLIGHT_LEG VALUES({a}, {b}, '{c}', '{d}', '{e}', '{f}', '{g}', {h}, 0);""".format(a=flight_id,b=leg_no,c=dt_string,d=ar_string,e=departure_airport,f=arrival_airport,g=status,h=seats)
		sql.write(inserts)
		with open('password.txt') as f:
			lines = [line.rstrip() for line in f]
		username = lines[0]
		pg_password = lines[1]
		conn = psycopg2.connect(database = "COSC3380", user = username, password = pg_password, host="code.cs.uh.edu")
		cursor1 = conn.cursor()
		try:
			if(cursor1.execute(inserts) == None):
				error_dialog = QtWidgets.QErrorMessage()
				error_dialog.showMessage('Succesfully Inserted Flight Leg')
				error_dialog.exec_()
		except psycopg2.Error as err:
			
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText('Invalid Flight Leg Insertion')
			msg.setWindowTitle("Error")
			msg.exec_()

		conn.commit()
		cursor1.close()
		conn.close()


	def gotomain3(self):
		f=main()
		widget.addWidget(f)
		widget.setCurrentIndex(widget.currentIndex()+1)






class inserted(QMainWindow):
	def __init__(self):
		super(inserted,self).__init__()
		loadUi("inserted.ui", self)
		self.main.clicked.connect(self.gotomain)
	def gotomain(self):
		f=main()
		widget.addWidget(f)
		widget.setCurrentIndex(widget.currentIndex()+1)




class flights_lists(QMainWindow):
	def __init__(self):
		super(flights_lists,self).__init__()
		loadUi("flights_list.ui", self)
		self.btn_load.clicked.connect(self.loadData)
		self.dialogs = reserve()
		self.back.clicked.connect(self.gotomain2)
		#self.searchButton.clicked.connect(self.searchfunction)
	def setValue(self, item1, item2,item3):
		global ones
		ones = item1
		global twos 
		twos = item2
		global month
		month = item3
		#print(one, two)
	def setPass(self, item1):
		global passen 
		passen = item1

	def gotomain2(self):
		f=main()
		widget.addWidget(f)
		widget.setCurrentIndex(widget.currentIndex()+1)


		
	def loadData(self):
		v = ones
		q = twos
		with open('password.txt') as f:
			lines = [line.rstrip() for line in f]
		username = lines[0]
		pg_password = lines[1]
		conn = psycopg2.connect(database = "COSC3380", user = username, password = pg_password, host="code.cs.uh.edu")
		cursor = conn.cursor()
		temp_query = """WITH RECURSIVE flight_paths (flight_id,leg_no,departure_airport,path,path_id,arrival_airport,scheduled_departure, scheduled_arrival) AS (
SELECT
flight_id,
leg_no,
departure_airport,
ARRAY[departure_airport],
ARRAY[flight_id,leg_no],
arrival_airport,
scheduled_departure, 
scheduled_arrival
FROM flight_leg
UNION ALL
SELECT
fp.flight_id,
fp.leg_no,
fp.departure_airport,
fp.path || f.departure_airport,
fp.path_id || f.flight_id || f.leg_no,
f.arrival_airport,
fp.scheduled_departure,
f.scheduled_arrival
FROM flight_leg f
JOIN flight_paths fp ON f.departure_airport = fp.arrival_airport
WHERE NOT f.departure_airport = ANY(fp.path)
  AND NOT '{z}' = ANY(fp.path) 
    -- (2) this new predicate stop iteration when the destination is reached

  AND f.scheduled_departure > fp.scheduled_arrival
    -- (3) this new predicate only proceeds the iteration if the connecting flights are valid

)
SELECT departure_airport,path,path_id,arrival_airport,scheduled_departure, scheduled_arrival
FROM flight_paths
WHERE departure_airport = '{x}' AND arrival_airport = '{y}' AND scheduled_departure like '%-{mo}-%'""".format(x = ones, y = twos, z = twos, mo = month)
		

		sql.write(temp_query)
		cursor.execute(temp_query)
		data = cursor.fetchall()
		self.tableWidget.setRowCount(0)

		for row_number, row_data in enumerate(data):
			self.tableWidget.insertRow(row_number)
			for column_number, datas in enumerate(row_data):
				self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(datas)))
		self.tableWidget.cellClicked.connect(self.cell_was_clicked)
		self.tableWidget.cellClicked.connect(self.gotoreserve)


	def cell_was_clicked(self, row, column):
		item = self.tableWidget.item(row, column+1)
		self.ID = item.text() #array of flight id and legs
		temp_arr = self.ID
		x = literal_eval(temp_arr)
		#print(x)
		self.dialogs.setValues(x)
		length = len(x)/2
		self.dialogs.set_surface(str(length*150*int(passen))) #ADDED THIS???
		self.dialogs.set_pass(str(passen))
		#print(self.ID)
	def gotoreserve(self):
		f=reserve()
		widget.addWidget(f)
		widget.setCurrentIndex(widget.currentIndex()+1)

	#def flight_function(self):

class reserve(QMainWindow):
	surface = None
	@classmethod
	def set_surface(cls,surface):
		cls.surface = surface
		
	p = 0
	@classmethod
	def set_pass(cls,p):
		cls.p = p
	def __init__(self):
		super(reserve,self).__init__()
		loadUi("reserve.ui", self)
		self.label_cost.setText(self.surface)#SET price here somehow

		self.submit_button.clicked.connect(self.getvalues)
		self.back1.clicked.connect(self.gotomain4)
		

		#self.submit_button.clicked.connect(self.gotofinal)	
		temp_p = int(self.p)

		for p in range(temp_p):
			scale = 60
			
			self.name = QLabel(self)
			self.name.setText('Name:')
			self.name.move(20, (420+(scale*p)))
			self.name.resize(60, 41)


			self.em = QLabel(self)
			self.em.setText('Email:')
			self.em.move(280, (420+(scale*p)))
			self.em.resize(60, 41)

			self.ph = QLabel(self)
			self.ph.setText('Phone:')
			self.ph.move(540, (420+(scale*p)))
			self.ph.resize(60, 41)

			self.name1 = QLineEdit(self)
			self.name1.move(100, (430+(scale*p)))
			self.name1.resize(141, 31)
			self.name1.setObjectName("name1_{0}".format(p))


			self.name2 = QLineEdit(self)
			self.name2.move(360, (430+(scale*p)))
			self.name2.resize(141, 31)
			self.name2.setObjectName("name2_{0}".format(p))

	
			self.name3 = QLineEdit(self)
			self.name3.move(690, (430+(scale*p)))
			self.name3.resize(141, 31)
			self.name3.setObjectName("name3_{0}".format(p))


		#self.btn_load.clicked.connect(self.loadData)
	def setValues(self, item1):
		global arr
		arr = item1
		#print("here:" ,arr)
	def gotomain4(self):
		f=main()
		widget.addWidget(f)
		widget.setCurrentIndex(widget.currentIndex()+1)

	

	def getvalues(self):
		customer_name = self.input_name.text()
		customer_email = self.input_email.text()
		customer_number = self.input_phone.text()
		customer_id_tag = self.input_id.text()
		customer_card = self.input_cardnum.text()
		f_id1= ""
		book_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
		customer_id = ''.join(random.choices(string.digits, k=4))

		

		passenger_arr = []

		for child in self.findChildren(QLineEdit, QtCore.QRegExp("name1_(\d)+")): #names
			passenger_arr.append(child.text())
		for child in self.findChildren(QLineEdit, QtCore.QRegExp("name2_(\d)+")): #emails
			passenger_arr.append(child.text())
		for child in self.findChildren(QLineEdit, QtCore.QRegExp("name3_(\d)+")): #phones
			passenger_arr.append(child.text())
		#for loop through ids in arr
		#for ids in arr:

		#do transaction block here send to database
		#unique ticket, customerid...etc
		#use string and append blocks for transaction query
		ct = str(datetime.datetime.now())
		new_ct = ct[:19] #current time for bookings
		#get every flightid and legid and make query for ticket_flights
		#ticket contains different ticket_flights with leg id
		#f is int
		#need passenger email, name, and phone for each passenger
		#check seats available for each flight leg 
		
		#for p in range(passen): #get passenger information
		#need to do for loop of FLIGHT IDS AND LEG IDS FIRST THEN INSIDE DO TICKET QUERY
		dad_query_flightids = """ """
		dad_query = """ """
		dad_boarding = """ """
		ticket_ids_arr = []

		#"AND flight_id = {m}"
		first = """SELECT * FROM flight_leg WHERE """
		for a in range(int(len(arr)/2)):
			if(a == int(len(arr)/2)-1):
				inside = """flight_id = {m} AND leg_no = {no} """.format(m = arr[a*2], no = arr[(a*2)+1])

			inside = """flight_id = {m} AND leg_no = {no} UNION SELECT * FROM flight_leg WHERE """.format(m = arr[a*2], no = arr[(a*2)+1])
			first+=inside

		sql.write(first)


		for q in range(int(passen)):
			if(int(passen)==1):
				ticket_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
				ticket_ids_arr.append(ticket_no)
				passenger_id_unique = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

				child_query = """INSERT INTO ticket(ticket_no ,book_ref,passenger_id,passenger_name,email,phone)
SELECT '{k}','{a}','{l}', '{e}', '{c}', '{g}' 
WHERE EXISTS({temp} seats_available > 0);""".format(a=book_ref,k=ticket_no,e = passenger_arr[q],l=passenger_id_unique,c = passenger_arr[q+1],temp = first,g=passenger_arr[q+2])
				dad_query+=child_query
				continue


			ticket_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
			ticket_ids_arr.append(ticket_no)
			passenger_id_unique = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

			child_query = """INSERT INTO ticket(ticket_no ,book_ref,passenger_id,passenger_name,email,phone)
SELECT '{k}','{a}','{l}', '{e}', '{c}', '{g}' 
WHERE EXISTS({temp} seats_available > 0);""".format(a=book_ref,k=ticket_no,e = passenger_arr[q],l=passenger_id_unique,c = passenger_arr[q+int(passen)],temp = first,g=passenger_arr[q+(int(passen)*2)])
			dad_query+=child_query


		sql.write(dad_query)
		for o in range(len(ticket_ids_arr)):
			for t in range(int(len(arr)/2)):
				boarding_no = ''.join(random.choices(string.digits, k=3))
				seat_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
				gate_number = '1A'

				child_query_flights = """INSERT INTO ticket_flights(ticket_no,flight_id,leg_no,fare_conditions,amount) 
SELECT '{k}',{m},{n},'Economy',150
WHERE EXISTS(SELECT * FROM flight_leg WHERE flight_id = {m} and leg_no = {n} and seats_available > 0);""".format(k=ticket_ids_arr[o],m=arr[t*2],n=arr[(t*2)+1])
				dad_query_flightids+=child_query_flights

				q12 = """SELECT scheduled_departure FROM flight_leg WHERE flight_id={a} AND leg_no = {b};""".format(a=arr[t*2],b=arr[(t*2)+1])
				with open('password.txt') as f:
					lines = [line.rstrip() for line in f]
				username = lines[0]
				pg_password = lines[1]
				conn = psycopg2.connect(database = "COSC3380", user = username, password = pg_password, host="code.cs.uh.edu")
				cursor1 = conn.cursor()
				cursor1.execute(q12)
				data = cursor1.fetchone()
				sql.write(q12)
				tp = data[0]
				date_time_obj = datetime.datetime.strptime(tp, '%Y-%m-%d %H:%M:%S')
				new_t = date_time_obj + datetime.timedelta(hours=1)













				child_board = """INSERT INTO boarding_passes(ticket_no,flight_id,leg_no, boarding_no,seat_no, boarding_time,gate_number, checked_bags, confirmed) 
SELECT '{k}',{m},{n},{a},'{b}','{c}',{d},'T','NULL'
WHERE EXISTS(SELECT * FROM flight_leg WHERE flight_id = {m} and leg_no = {n} and seats_available > 0);""".format(k=ticket_ids_arr[o],m=arr[t*2],n=arr[(t*2)+1], a=boarding_no,b=seat_no,c=str(new_t),d=gate_number)
				dad_boarding+=child_board
				#insert into boarding passes here

		fquery = """ """
		sql.write(dad_query_flightids)
		for fl in range(int(len(arr)/2)):
			q = """UPDATE flight_leg
SET seats_booked = seats_booked + {z1} 
WHERE flight_id = {m} AND leg_no = {t} AND seats_available > 0;""".format(z1 = int(passen),m = int(arr[fl*2]),t = int(arr[(fl*2)+1]))
			fquery+=q
		sql.write(fquery)
		for fl in range(int(len(arr)/2)):
			q1 = """UPDATE flight_leg
SET seats_available = seats_available - {z1} 
WHERE flight_id = {m} AND leg_no = {t} AND seats_available > 0; """.format(z1 = int(passen),m = int(arr[fl*2]),t = int(arr[(fl*2)+1]))
			fquery+=q1
		sql.write(fquery)
		payment_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))








		trans_query = """START TRANSACTION; 


INSERT INTO customer(customer_email,customer_name,customer_id,customer_phone,id_type)
SELECT '{c}', '{e}', {f}, '{g}', '{h}'
WHERE NOT EXISTS(SELECT * FROM customer WHERE customer_email = '{c}'); 

INSERT INTO payment
values('{pp}','{i}', {j});

INSERT INTO bookings 
VALUES('{a}','{c}','{b}','{z}');

INSERT INTO customer_entity
VALUES('{c}','{pp}');






{dad}

{dad2}


{dad3}

{dad4}



COMMIT;""".format(pp=payment_id,a=book_ref, b = new_ct, c = customer_email, e = customer_name, f= customer_id, g=customer_number,h=customer_id_tag, i = customer_card, j = self.surface, k=ticket_no,l=passenger_id_unique, m=arr[0],n=arr[1], z=passen,z1=int(passen),dad=dad_query, dad2 = dad_query_flightids, dad3 = fquery,dad4=dad_boarding)

		transaction_queries.write(trans_query)
		with open('password.txt') as f:
			lines = [line.rstrip() for line in f]
		username = lines[0]
		pg_password = lines[1]
		conn = psycopg2.connect(database = "COSC3380", user = username, password = pg_password, host="code.cs.uh.edu")
		cursor = conn.cursor()
		try:
			if(cursor.execute(trans_query) == None):
				error_dialog = QtWidgets.QErrorMessage()
				error_dialog.showMessage('Reservation Successfull!')
				error_dialog.exec_()
		except psycopg2.Error as err:
			
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Reservation was not succesful")
			msg.setInformativeText('Please make sure information is correct')
			msg.setWindowTitle("Error")
			msg.exec_()




	def gotofinal(self):
		f=final()
		widget.addWidget(f)
		widget.setCurrentIndex(widget.currentIndex()+1)


class final(QMainWindow):
	def __init__(self):
		super(final,self).__init__()
		loadUi("final.ui", self)
		self.main.clicked.connect(self.gotomain1)


		#self.btn_load.clicked.connect(self.loadData)
	def setValues(self, item1):
		global arr
		arr = item1
		#print("here:" ,arr)

	#def getvalues(self):
	def gotomain1(self):
		f=main()
		widget.addWidget(f)
		widget.setCurrentIndex(widget.currentIndex()+1)

if __name__ == '__main__':		
	sql = open("query.sql",'w')
	transaction_queries = open("transaction.sql","w")
	
	app = QApplication(sys.argv)
	mainwindow = main()
	widget=QtWidgets.QStackedWidget()
	widget.addWidget(mainwindow)
	widget.setFixedWidth(1050)
	widget.setFixedHeight(800)
	widget.show()
	app.exec_()
	

