from reports import PDFReport
from roommate import Bill, Roommate

# CLI - COMMAND LINE (USER) INTERFACE IMPLEMENTATION
bill_amount = float(input("Please enter the bill's amount: "))
period = input("Please is the billing period? E.g. Feb. 2021: ")
name_roommate1 = input("Please enter the name of roommate1: ")
name_roommate2 = input("Please enter the name of roommate2: ")
roommate1_days_in_house = int(input(f"Please enter the number of days {name_roommate1} stayed in the house for {period}: "))
roommate2_days_in_house = int(input(f"Please enter the number of days {name_roommate2} stayed in the house for {period}: "))

# INSTANTIATION AND PDF GENERATION
the_bill = Bill(bill_amount, period)
roommate1 = Roommate(name_roommate1, roommate1_days_in_house)
roommate2 = Roommate(name_roommate2, roommate2_days_in_house)
roommate1_payment = roommate1.pays(the_bill, roommate2)
roommate2_payment = roommate2.pays(the_bill, roommate1)

# Confirm payment ratios for roommate 1 and 2 are correct and == total bill amount
assert round(roommate1_payment + roommate2_payment) == the_bill.amount

# Output to console command line
print(f'{roommate1.name} pays: ${roommate1_payment:.2f}')
print(f'{roommate2.name} pays: ${roommate2_payment:.2f}')

# Generate PDF Report
pdf_report = PDFReport(filename=f"Report {the_bill.period}.pdf")
pdf_report.generate_pdf(roommate1, roommate2, the_bill)