import webbrowser
from fpdf import FPDF

class Bill:
    """
    Object that contains data about a bill one must pay.
    Data includes:
        - amount
        - period
    """

    def __init__(self, amount, period):
        self.amount = amount
        self.period = period


class Roommate:
    """
    Creates a roommate person who lives in the apartment
    and pays a share of the bill.
    """

    def __init__(self, name, days_in_house):
        self.name = name
        self.days_in_house = days_in_house

    def pays(self, bill, other_roommate):
        """
        Calculates this roommate's share of the bill based on time spent in the house.
        Args:
            bill (Bill): The bill to be split.
            other_roommate (Roommate): The other roommate sharing the bill.
        Returns:
            float: The amount this roommate needs to pay.
        Notes:
            The bill is split proportionally based on the number of days
            each roommate stayed in the house.
        Raises:
            ZeroDivisionError: If both roommates have zero days in the house.
        """
        if self.days_in_house == 0 and other_roommate.days_in_house == 0:
            raise ZeroDivisionError("Both roommate have zero days in the house.")

        weight = self.days_in_house / (self.days_in_house + other_roommate.days_in_house)
        amount_to_pay = weight * bill.amount
        return amount_to_pay


class PDFReport:
    """
    Creates a PDF file that contains data about
    the roommates such as their names, their amount due,
    and the period of the bill.
    """

    def __init__(self, filename):
        self.filename = filename

    def generate_pdf(self, roommate1, roommate2, bill):
        roommate1_payment = f'${roommate1.pays(bill=bill, other_roommate=roommate2):.2f}'
        roommate2_payment = f'${roommate2.pays(bill=bill, other_roommate=roommate1):.2f}'

        # PDF parameters:
        # - 'P' = portrait mode
        # - 'pt' = unit of measurement, point (1/72 inch), i.e. 12pt font for PDF
        # - 'A4' = standard international paper size

        # Create instance of PDF
        pdf = FPDF(orientation="P", unit="pt", format='A4')

        # Add a page to PDF
        pdf.add_page()

        # Add house icon
        pdf.image(name="house.png", w=30, h=30)

        # Set font for title section of the PDF and insert title
        pdf.set_font("Arial", size=24, style='B')
        pdf.cell(w=0, h=80, txt="Roommates Bill", border=0, align='C', ln=1)

        # Set font for period section of PDF and insert period label and value
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(w=100, h=40, txt="Period:", border=0)
        pdf.cell(w=150, h=40, txt=bill.period, border=0, ln=1)

        # Set font for this section of PDF and insert name and amount to pay for roommate1 and roommate 2
        pdf.set_font("Arial", size=12)
        # roommate1 section
        pdf.cell(w=100, h=25, txt=roommate1.name, border=0)
        pdf.cell(w=150, h=25, txt=roommate1_payment, border=0, ln=1)

        # roommate2 section
        pdf.cell(w=100, h=25, txt=roommate2.name, border=0)
        pdf.cell(w=150, h=25, txt=roommate2_payment, border=0)

        pdf.output(self.filename)

        webbrowser.open(self.filename)

# Testing what is implemented so far
the_bill = Bill(amount=120, period="March 2022")
roommate1 = Roommate(name="John", days_in_house=20)
roommate2 = Roommate(name="Mary", days_in_house=25)
roommate1_payment = roommate1.pays(bill=the_bill, other_roommate=roommate2)
roommate2_payment = roommate2.pays(bill=the_bill, other_roommate=roommate1)

assert round(roommate1_payment + roommate2_payment) == the_bill.amount

print(f'{roommate1.name} pays: ${roommate1_payment:.2f}')
print(f'{roommate2.name} pays: ${roommate2_payment:.2f}')

pdf_report = PDFReport(filename="Report1.pdf")
pdf_report.generate_pdf(roommate1=roommate1, roommate2=roommate2, bill=the_bill)