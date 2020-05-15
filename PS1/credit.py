import math

# Problem Set 1: Calculating Credit Card Debt

# Problem 1. Write a program to calculate the credit card balance after one year 
# if a person only pays the minimum monthly payment required by the credit card company 
# each month. 

def endBalance():
	"""
    Test Case 1, use balance 4800, interest rate 0.2, min monthly payment 0.02
    RESULT:	Total amount paid: $1131.12; Remaining balance: $4611.46

    Test Case 2, use balance 4800, interest rate 0.2, min monthly payment 0.04
    RESULT:	Total amount paid: $2030.15; Remaining balance: $3615.74
    """
	balance = float(input("Enter the outstanding balance on your credit card:"))
	rate = float(input("Enter the annual credit card interest rate as a decimal:"))
	payment = float(input("Enter the minimum monthly payment rate as a decimal:"))
	total = 0

	for i in range(1, 13):
		min_payment = payment * balance
		interest = rate/12 * balance
		principal = min_payment - interest
		total = total + min_payment
		balance = balance - principal

		print("Month " + str(i))
		print("Minimum monthly payment: $%.2f" %(min_payment))
		print("Principal Paid: $%.2f" %(principal))
		print("Remaining balnce: $%.2f" %(balance))

	print("RESULT")
	print("Total amount paid: $%.2f" %(total))
	print("Remaining balance: $%.2f" %(balance))

# endBalance()

# Problem 2. Write a program that calculates the minimum fixed monthly payment needed
# in order pay off a credit card balance within 12 months. We will not be dealing
# with a minimum monthly payment rate. This version will use a brute force approach,
# incrementing the monthly payment by $10 for each cycle until a solution is found.

def minPayment1():
	"""
	Test Case 1, use balance 1200 and interest rate 0.18
	RESULT: Monthly payment: 120; Number of months needed: 11; Balance: -10.05

	Test Case 2, use balance 32000  and interest rate 0.2
	RESULT:	Monthly payment: 2970; Number of months needed: 12; Balance: -74.98
	"""
	balance = float(input("Enter the outstanding balance on your credit card:"))
	rate = float(input("Enter the annual credit card interest rate as a decimal:"))
	monthly_rate = rate / 12
	payment = 0
	test_balance = balance

	while test_balance > 0:
		test_balance = balance
		payment += 10
		#print("Payment: $%.2f" % (payment))

		for month in range(1, 13):

			interest = round((monthly_rate * test_balance), 2)
			principal = payment - interest
			test_balance = test_balance - principal
			# print("    Month " + str(month))
			# print("        Principal Paid: $%.2f" % (principal))
			# print("        Remaining balnce: $%.2f" % (test_balance))

			# If remaining balance is <= 0 before moth 12, break
			if test_balance <= 0:
				break



	print("RESULT")
	print("Monthly payment to pay off debt in 1 year:$%.2f" % (payment))
	print("Number of months needed: " + str(month))
	print("Balance: %.2f" % (test_balance))

#minPayment1()

# Problem 3. Write a program that calculates the minimum fixed monthly payment needed
# in order pay off a credit card balance within 12 months. We will not be dealing with
# a minimum monthly payment rate. This version will find the minimum payment to the nearest
# cent using a bisection search.


def minPayment2():
	"""
	Test Case 1, use balance 320000 and interest rate 0.2
	RESULT: Monthly payment: 29643.05; Number of months needed: 12; Balance: -0.1
				
	Test Case 2, use balance 999999  and interest rate 0.18
	RESULT:	Monthly payment: 91679.91; Number of months needed: 12; Balance: -.128
	"""
	balance = float(input("Enter the outstanding balance on your credit card:"))
	rate = float(input("Enter the annual credit card interest rate as a decimal:"))
	monthly_rate = rate/12
	# Initialize starting values for variables
	low_bound = balance/12
	high_bound = (balance * (1 + monthly_rate)**12)/12
	payment = round(((high_bound+low_bound)/2), 2)
	test_balance = balance

	# Loop until a solution is found with remaining balance <= 0
	while True:
		test_balance = balance
		print("Payment: $%.2f" %(payment))
		print("Low Bound: $%.2f" %(low_bound))
		print("High Bound: $%.2f" %(high_bound))

		for month in range(1,13):
			interest = round((monthly_rate * test_balance), 2)
			principal = payment - interest
			test_balance = test_balance - principal
			print("    Month " + str(month))
			print("        Principal Paid: $%.2f" %(principal))
			print("        Remaining balnce: $%.2f" %(test_balance))

			# If remaining balance <= 0 before month 12, break
			if test_balance <= 0:
				break

		# Test answer and adjust bounds as needed
		if (test_balance <= 0) and (payment - low_bound < 0.03):
			print("RESULT")
			print("Monthly payment to pay off debt in 1 year:$%.2f" %(payment))
			print("Number of months needed: " + str(month))
			print("Balance: %.2f" %(test_balance))
			break
		elif test_balance > 0:
			low_bound = payment
			payment = round(((high_bound+payment)/2), 2)
		elif test_balance < 0:
			high_bound = payment
			payment = round(((low_bound+payment)/2), 2)

minPayment2()
