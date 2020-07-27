## RESTAURANT DBMS

This project is a prototype for a restaurant management system. It is useful for the administrative team of the restaurant. The users can use the application to manage the orders received by the restaurant. They will be able to query the database to fetch the required information about any particular order. They can also make database transactions regarding employees.

### ENTITIES:
1. EMPLOYEES
2. ORDER
3. CUSTOMER
4. MENU
5. TABLE
6. PAYMENT
7. EMPLOYEE DEPENDENTS (*Weak Entity*)
8. ORDER ITEM (*Weak Entity*)

### RELATIONS:
1. HasPaid
2. HasOrdered
3. PaymentFor
4. IsPreparing
5. ItemInOrder
6. ItemInMenu
7. IsDependentOf
8. IsServing

### CLASSES
1. Employee
	1. Chef
	2. Waiter
