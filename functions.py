import MySQLdb
import datetime

db = MySQLdb.connect('localhost','root', '12345678', 'RESTAURANT')
cursor = db.cursor()

cursor.execute("""SELECT MAX(EMPLOYEE_ID) FROM EMPLOYEES;""")
resp = cursor.fetchone()
employeeID = resp[0] + 1

cursor.execute("""SELECT MAX(FOOD_ID) FROM MENU;""")
resp = cursor.fetchone()
foodID = resp[0] + 1

cursor.execute("""SELECT MAX(CUSTOMER_ID) FROM CUSTOMER;""")
resp = cursor.fetchone()
if resp[0] is None:
	customerID = 1;
else:
	customerID = resp[0] + 1

cursor.execute("""SELECT MAX(ORDER_ID) FROM `ORDER`;""")
resp = cursor.fetchone()
if resp[0] is None:
	orderID = 1
else:
	orderID = resp[0] + 1

cursor.execute("""SELECT MAX(PAYMENT_ID) FROM PAYMENT;""")
resp = cursor.fetchone()
if resp[0] is None:
	paymentID = 1
else:
	paymentID = resp[0] + 1


def hireNewEmployee():
	global employeeID
	try:
		Fname = raw_input('Enter first name of employee: ')
		Lname = raw_input('Enter last name of employee: ')
		contactNumber = raw_input('Enter contact number of employee: ')
		employeeType = int(raw_input('Enter employee type (0 for chef, 1 for waiter): '))
		salary = int(raw_input('Enter salary of employee: '))
		if len(contactNumber) != 10:
			print 
			print "Invalid contact number"
			return
		contactNumber = int(contactNumber)
		if employeeType != 0 and employeeType != 1:
			print 
			print 'Invalid employee type'
			print
			return 
	except:
		print "Invalid input(s)"
		return

	
	try:		
		mySql_insert_query = """INSERT INTO EMPLOYEES (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, CONTACT_NUMBER, SALARY) VALUES (%s, %s, %s, %s, %s)"""
		cursor.execute(mySql_insert_query, (employeeID, Fname, Lname, contactNumber, salary))
		db.commit()
		# cursor.close()
		employeeID = employeeID + 1	
	
	except :
		print "Error"
		db.rollback()

	try:
		# cursor = db.cursor()
		if employeeType == 0:
			mySql_insert_query = """INSERT INTO CHEF (EMPLOYEE_ID, ORDER_ID) VALUES (%s, %s)"""
			cursor.execute(mySql_insert_query, (employeeID - 1, None))
		else:
			mySql_insert_query = """INSERT INTO WAITER (EMPLOYEE_ID, CUSTOMER_ID, ORDER_ID, TABLE_ID) VALUES (%s, %s, %s, %s)"""
			cursor.execute(mySql_insert_query, (employeeID - 1, None, None, None))
		db.commit()			
		# cursor.close()

	except:
		print "Error"
		db.rollback()

	# db.close() 

def fireAnEmployee():
	try:
		empID = int(raw_input('Enter employee ID of employee you want to fire: '))
	except:
		print "Invalid input"
		return
	cursor.execute("""SELECT * from EMPLOYEES WHERE EMPLOYEE_ID = %s;""", (empID,))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print
		print 'Invalid employee ID'
		return

	try:
		cursor.execute("""SELECT * from CHEF WHERE EMPLOYEE_ID = %s;""", (empID,))
		rowcount = cursor.rowcount
		if rowcount !=0:
			resp = cursor.fetchone()
			if resp[1] is not None:
				print 'Cannot fire employee as the employee is working on an order'
				return
			cursor.execute("""DELETE from CHEF WHERE EMPLOYEE_ID = %s;""", (empID,))
			cursor.execute("""DELETE from EMPLOYEES WHERE EMPLOYEE_ID = %s;""", (empID,))
			db.commit()

		else:
			cursor.execute("""SELECT * from WAITER WHERE EMPLOYEE_ID = %s;""", (empID,))
			resp = cursor.fetchone()
			if resp[1] is not None:
				print 'Cannot fire employee as the employee is working on an order'
				return
			cursor.execute("""DELETE from WAITER WHERE EMPLOYEE_ID = %s;""", (empID,))
			cursor.execute("""DELETE from EMPLOYEES WHERE EMPLOYEE_ID = %s;""", (empID,))
			db.commit()
	except:
		print "Error!"
		return
	return		

def addMenuItem():
	global foodID
	# db = MySQLdb.connect('localhost','root', '12345678', 'RESTAURANT')
	item=raw_input("Enter the name of food item: ")
	
	# cursor = db.cursor()
	cursor.execute("""SELECT COUNT(*) FROM MENU WHERE FOOD_ITEM = %s;""",(item,))
	exists = cursor.fetchone()
	# cursor.close()
	if exists[0] != 0:
		print
		print "Item already exists"
		return
	
	try:
		price=int(raw_input("Enter its price: "))
	except:
		print "Invalid input"
		return
	
	try:
		# cursor = db.cursor()
		cursor.execute("""INSERT INTO MENU VALUES (%s,%s, %s);""",(foodID,item,price))
	   	db.commit()
		print "added new menu item"
		foodID=foodID+1
		# cursor.close()
	except:
	   	db.rollback()
	# db.close()

def removeMenuItem():
	item = raw_input('Enter name of item you want to remove from menu: ')
	# db = MySQLdb.connect('localhost','root', '12345678', 'RESTAURANT')

	try:	
		# cursor = db.cursor()
		cursor.execute("""SELECT COUNT(*) FROM MENU WHERE FOOD_ITEM = %s;""",(item,))
		exists = cursor.fetchone()
		
		if exists[0] == 0:
			print
			print "Item does not exist in the Menu"
			return

		cursor.execute("""DELETE FROM MENU WHERE FOOD_ITEM = %s;""",(item,))
		db.commit()
		# cursor.close()
		print
		print "Item deleted from Menu"
	
	except:
		print "Error"
		db.rollback()	
	# db.close()

def changePrice():
	# db = MySQLdb.connect('localhost','root', '12345678', 'RESTAURANT')
	item =  raw_input('Enter name of item whose price you want to change: ')
	# cursor = db.cursor()
	cursor.execute("""SELECT COUNT(*) FROM MENU WHERE FOOD_ITEM = %s;""",(item,))
	exists = cursor.fetchone()
	if exists[0] == 0:
		print
		print "Item does not exist in the Menu"
		return

	try:
		price = int(raw_input('Enter new price: '))
	except:
		print "Invalid input"
		return

	try:	
		cursor.execute("""UPDATE MENU SET PRICE = %s WHERE FOOD_ITEM = %s;""", (price, item,))
		db.commit()
		print
		print "Price changed"

	except:
		print "Error"
		db.rollback()

	# cursor.close()
	# db.close()

def addCustomer():
	global customerID
	# db = MySQLdb.connect('localhost','root', '12345678', 'RESTAURANT')
	# cursor = db.cursor()

	cursor.execute("""SELECT * FROM `TABLE` WHERE CUSTOMER_ID IS NULL;""")
	rowcount = cursor.rowcount
	if rowcount == 0:
		print
		print "Cannot add a new customer as no table is free"
		return
	
	Fname = raw_input('Enter first name of customer: ')
	Lname = raw_input('Enter last name of customer: ')

	table = cursor.fetchone()
	try:	
		mySql_insert_query = """INSERT INTO CUSTOMER (CUSTOMER_ID, FIRST_NAME, LAST_NAME, PAYMENT_ID, ORDER_ID, TABLE_ID) VALUES (%s, %s, %s, %s, %s, %s)"""
		cursor.execute(mySql_insert_query, (customerID, Fname, Lname, None, None, table[0]))
		cursor.execute("""UPDATE `TABLE` SET CUSTOMER_ID = %s WHERE TABLE_ID = %s;""", (customerID, table[0],))
		db.commit()
		customerID = customerID + 1

	except:
		print "Error"
		db.rollback()

	# cursor.close()
	# db.close()

def makeOrder():
	global orderID
	global paymentID
	# db = MySQLdb.connect('localhost','root', '12345678', 'RESTAURANT')
	# cursor = db.cursor()

	cursor.execute("""SELECT * FROM CHEF WHERE ORDER_ID IS NULL;""")
	rowcount = cursor.rowcount
	if rowcount == 0:
		print
		print "Cannot make a new order as no chef is currently free"
		return
	chef = cursor.fetchone()

	cursor.execute("""SELECT * FROM WAITER WHERE TABLE_ID IS NULL;""")
	rowcount = cursor.rowcount
	if rowcount == 0:
		print
		print "Cannot make a new order as no waiter is currently free"
		return
	waiter = cursor.fetchone()

	try:
		custID = int(raw_input('Enter customer ID: '))
	except:
		print "Invalid input"
		return

	cursor.execute("""SELECT * FROM CUSTOMER WHERE CUSTOMER_ID = %s;""", (custID,))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print
		print "Invalid customerID"
		return

	customer = cursor.fetchone();
	if customer[4] is not None:
		print 
		print "Customer can't have multiple orders"
		return	

	food_ids = []
	quantities = []
	while True:
		try:
			food_id  = int(raw_input("Enter food ID of food item: "))
			quantity = int(raw_input('Enter its quantity: '))
		except:
			print "Invalid input"
			return
		
		cursor.execute("""SELECT * FROM MENU WHERE FOOD_ID = %s;""", (food_id,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print
			print "Invalid food_id"
			return
		
		try:
			index = food_ids.index(food_id)
			quantities[index] = quantities[index] + quantity
		except:
			food_ids.append(food_id)
			quantities.append(quantity)


		flag = raw_input(("Do you want to add more items ?(enter Y for Yes)"))	
		if flag != 'Y' and flag != 'y':
			break;

	try:
		cursor.execute("""UPDATE CUSTOMER SET ORDER_ID = %s, PAYMENT_ID = %s WHERE CUSTOMER_ID = %s;""", (orderID, paymentID, custID,))		
		cursor.execute("""UPDATE WAITER SET CUSTOMER_ID = %s, ORDER_ID = %s, TABLE_ID = %s WHERE EMPLOYEE_ID = %s;""", (custID, orderID, customer[5], waiter[0]))		
		cursor.execute("""UPDATE CHEF SET ORDER_ID = %s WHERE EMPLOYEE_ID = %s;""", (orderID, chef[0],))		
		
		date=datetime.datetime.now()
		date=str(date.year)+'.'+str(date.month)+'.'+str(date.day)
		mySql_insert_query = """INSERT INTO `ORDER` (ORDER_ID, CUSTOMER_ID, ORDER_DATE, STATUS, PAYMENT_ID) VALUES (%s, %s, %s, %s, %s)"""
		cursor.execute(mySql_insert_query, (orderID, custID, date, "PENDING", paymentID))
		amount=0
		for i in range(len(food_ids)):
			cursor.execute("""SELECT PRICE FROM MENU WHERE FOOD_ID=%s;""",(food_ids[i],))
			res=cursor.fetchone()
			amount=quantities[i]*int(res[0])+amount
			mySql_insert_query = """INSERT INTO ORDER_ITEM (ORDER_ID, FOOD_ID, QUANTITY, ORDER_DATE, UNIT_PRICE, CHEF_ID, STATUS) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
			cursor.execute(mySql_insert_query,(orderID, food_ids[i], quantities[i], date, res[0], chef[0], "PENDING"))
			mySql_insert_query = """INSERT INTO FOOD_IDS (FOOD_ID, ORDER_ID) VALUES (%s, %s)"""
			cursor.execute(mySql_insert_query,(food_ids[i], orderID))
		
		mySql_insert_query= """INSERT INTO PAYMENT(PAYMENT_ID, CUSTOMER_ID, ORDER_ID, AMOUNT, PAYMENT_DATE, STATUS) VALUES (%s, %s, %s, %s, %s, %s);"""
		cursor.execute(mySql_insert_query, (paymentID, custID, orderID, amount, None, "PENDING"))

		cursor.execute("""UPDATE `TABLE` SET ORDER_ID = %s WHERE TABLE_ID = %s;""", (orderID, customer[5],))
		mySql_insert_query= """INSERT INTO IS_SERVING(EMPLOYEE_ID, TABLE_ID, CUSTOMER_ID) VALUES (%s, %s, %s);"""
		cursor.execute(mySql_insert_query, (waiter[0], customer[5], custID,))	
		db.commit()

		orderID = orderID + 1
		paymentID = paymentID + 1
	except:
		db.rollback()
		print "Error with database"
		return 			

def modifyItemStatus():
	# db = MySQLdb.connect('localhost','root', '12345678', 'RESTAURANT')
	# cursor = db.cursor()
	
	try:
		order_id = int(raw_input('Enter order id: '))
		food_id = int(raw_input('Enter food id: ')) 
	except:
		print "Invalid input"
		return

	cursor.execute("""SELECT * FROM ORDER_ITEM WHERE FOOD_ID = %s and ORDER_ID = %s;""",(food_id, order_id,))
	
	rowcount = cursor.rowcount
	if rowcount == 0:
		print "Invalid combination"
		return

	order_item = cursor.fetchone()
	if order_item[6] != 'PENDING':
		print
		print "Item already prepared"
		return

	try:
		flag = 1
		cursor.execute("""UPDATE ORDER_ITEM SET STATUS = %s WHERE ORDER_ID = %s and FOOD_ID = %s;""", ("PREPARED", order_id, food_id))
		db.commit()
		cursor.execute("""SELECT STATUS FROM ORDER_ITEM WHERE ORDER_ID = %s;""",(order_id,))
		response = cursor.fetchall()
		
		for res in response:
			if res[0] == 'PENDING':
				flag = 0
				break

		if flag:
			cursor.execute("""UPDATE `ORDER` SET STATUS = %s WHERE ORDER_ID = %s;""", ("SERVED", order_id))
			cursor.execute("""UPDATE CHEF SET ORDER_ID = %s WHERE ORDER_ID = %s;""", (None, order_id))
			db.commit()
	except:
		print "Error"
		db.rollback()

def makePayment():		
	# db = MySQLdb.connect('localhost','root', '12345678', 'RESTAURANT')
	# cursor = db.cursor()
	date=datetime.datetime.now()
	date=str(date.year)+'.'+str(date.month)+'.'+str(date.day)

	try:
		payment_id=int(raw_input("Enter the payment id: "))
		payment_type=raw_input("Enter the payment type (CASH/CARD/UPI): ")
	except:
		print "Invalid input"
		return

	cursor.execute("""SELECT STATUS FROM PAYMENT WHERE PAYMENT_ID = %s;""",(payment_id,))
	rowcount=cursor.rowcount
	if rowcount==0:
		print "Invalid payment id"
		return

	response = cursor.fetchone()
	if response[0]=='PAID':
		print "Customer had already paid."
		return
	cursor.execute("""SELECT ORDER_ID FROM PAYMENT WHERE PAYMENT_ID = %s;""",(payment_id,))
	response = cursor.fetchone()

	cursor.execute("""SELECT STATUS FROM `ORDER` WHERE ORDER_ID = %s;""",(response[0],))
	response=cursor.fetchone()
	if response[0] == 'PENDING':
		print"Customer is not yet served his order. Do payment later."
		return

	cursor.execute("""SELECT CUSTOMER_ID FROM PAYMENT WHERE PAYMENT_ID = %s;""",(payment_id,))
	customer = cursor.fetchone()

	cursor.execute("""UPDATE PAYMENT SET PAYMENT_TYPE = %s, STATUS = %s, PAYMENT_DATE = %s WHERE PAYMENT_ID = %s;""",(payment_type,"PAID",date, payment_id,))
	cursor.execute("""UPDATE WAITER SET ORDER_ID = %s, CUSTOMER_ID = %s, TABLE_ID = %s WHERE CUSTOMER_ID = %s;""",(None,None,None,customer[0],))
	cursor.execute("""UPDATE `TABLE` SET CUSTOMER_ID = %s, ORDER_ID = %s WHERE CUSTOMER_ID = %s;""",(None,None,customer[0],))
	cursor.execute("""DELETE FROM IS_SERVING WHERE CUSTOMER_ID = %s;""",(customer[0],))
	db.commit()

def showMostOrderedItem():
	# db = MySQLdb.connect('localhost','root', '12345678', 'RESTAURANT')
	# cursor = db.cursor()

	cursor.execute("""SELECT FOOD_ID, QUANTITY FROM ORDER_ITEM;""")
	rowcount = cursor.rowcount
	if rowcount == 0:
		print 'Nothing ordered yet!'
		return

	food_id = {}
	response = cursor.fetchall()
	max_ordered = -1
	max_id = -1
	for resp in response:
		if int(resp[0]) in food_id.keys():
			food_id[int(resp[0])] = food_id[int(resp[0])] + int(resp[1])
		else:
			food_id[int(resp[0])] = int(resp[1])
		if max_ordered < food_id[resp[0]]:
			max_ordered = food_id[resp[0]]
			max_id = resp[0]

	cursor.execute("""SELECT FOOD_ITEM FROM MENU WHERE FOOD_ID = %s;""", (max_id,))
	response = cursor.fetchone()
	print response[0], " was ordered most number of times"
	# cursor.close()
	# db.close()
	return

def addEmployeeDependent():
	try:
		eid=int(raw_input("Enter the employee id: "))
	except:
		print "Invalid input"
		return

	cursor.execute("""SELECT * FROM EMPLOYEES WHERE EMPLOYEE_ID = %s;""",(eid,))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print "Invalid employee id"
		return

	emp=cursor.fetchone()
	edfname = raw_input("Enter dependent's first name: ")
	edlname = raw_input("Enter dependent's last name: ")
	try:
		cursor.execute("""SELECT * FROM EMPLOYEE_DEPENDENTS WHERE EMPLOYEE_ID = %s AND FIRST_NAME = %s AND LAST_NAME = %s;""",(eid,edfname,edlname))
		rowcount = cursor.rowcount
		if rowcount != 0:
			print "Dependent information already present"
			return

		mySql_insert_query = """INSERT INTO EMPLOYEE_DEPENDENTS (EMPLOYEE_ID, FIRST_NAME, LAST_NAME) VALUES (%s,%s,%s);"""
		cursor.execute(mySql_insert_query,(eid,edfname,edlname,))
		db.commit()
	except :
		print "Error"
		db.rollback()

while True:
	print("1: Hire new employee")
	print("2: Fire an employee")
	print("3: Add new menu item")
	print("4: Remove a menu item")
	print("5: Change price of menu item")
	print("6: Add new customer")
	print("7: Make an order")
	print("8: Modify order item status")
	print("9: Make payment")
	print("10: Show most ordered item")
	print("11: Add employee dependent")
	print("12: exit")
	choice = int(input("Enter your choice: "))

	if choice == 1:
		hireNewEmployee()
	
	elif choice == 2:
		fireAnEmployee()

	elif choice == 3:
		addMenuItem()

	elif choice == 4:
		removeMenuItem()

	elif choice == 5:
		changePrice()

	elif choice == 6:
		addCustomer()

	elif choice == 7:
		makeOrder()

	elif choice == 8:
		modifyItemStatus()

	elif choice == 9:
		makePayment()

	elif choice == 10:
		showMostOrderedItem()

	elif choice == 11:
		addEmployeeDependent()

	elif choice == 12:
		break

	else:
		print "Enter a valid choice!!!"

	print 
	print "------------------------------------------------------------------------------------------------------------------------------------------------------"
	print

cursor.close()
db.close()
print 'Ba Bye!'