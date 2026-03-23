import webbrowser
from fpdf import FPDF
import os   # used to manipulate directories and files
from filestack import Client
from dotenv import load_dotenv

load_dotenv() # loads variables from .env
FILESTACK_API_KEY = os.getenv("FILESTACK_API_KEY")


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

        # Get page width and height for layout calculations
        page_width = pdf.w
        page_height = pdf.h

        # Define consistent layout margins for content placement
        outer_margin = 30
        inner_margin = 40
        content_left = 70
        content_right = page_width - 70
        label_width = 170
        value_width = 220
        table_name_width = 260
        table_amount_width = 180

        # Create an outer border around the page
        pdf.set_draw_color(180, 0, 0)  # darker red
        pdf.set_line_width(1.5)
        pdf.rect(x=outer_margin, y=outer_margin, w=page_width - (2 * outer_margin), h=page_height - (2 * outer_margin))

        # Create a lighter inner border for a polished business-report appearance
        pdf.set_draw_color(160, 160, 160)
        pdf.set_line_width(0.8)
        pdf.rect(x=inner_margin, y=inner_margin, w=page_width - (2 * inner_margin), h=page_height - (2 * inner_margin))

        # Add house icon
        pdf.image(name="resource_files/house.png", x=content_left, y=55, w=30, h=30)

        # Set font for title section of the PDF and insert title
        pdf.set_xy(0, 50)
        pdf.set_font("Arial", size=24, style='B')
        pdf.cell(w=0, h=40, txt="Roommates Bill", border=0, align='C', ln=1)

        # Add subtitle for a more polished report design
        pdf.set_font("Arial", size=11, style='I')
        pdf.set_text_color(90, 90, 90)
        pdf.cell(w=0, h=18, txt="Shared Expense Breakdown Report", border=0, align='C', ln=1)

        # Reset text color to black for body content
        pdf.set_text_color(0, 0, 0)

        # Add a horizontal divider line below title section
        pdf.set_draw_color(120, 120, 120)
        pdf.set_line_width(1)
        pdf.line(x1=content_left, y1=125, x2=content_right, y2=125)

        # Move cursor below title area and shift content block right
        pdf.set_y(145)
        pdf.set_x(content_left)

        # Set font for period section of PDF and insert period label and value
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(w=label_width, h=30, txt="Period:", border=0)
        pdf.set_font("Arial", size=14)
        pdf.cell(w=value_width, h=30, txt=str(bill.period), border=0, ln=1)

        # Move cursor to left content boundary for next row
        pdf.set_x(content_left)

        # Add total bill section for a more complete business summary
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(w=label_width, h=30, txt="Total Bill:", border=0)
        pdf.set_font("Arial", size=14)
        pdf.cell(w=value_width, h=30, txt=f'${bill.amount:.2f}', border=0, ln=1)

        # Add spacing before roommate payment section
        pdf.ln(20)
        pdf.set_x(content_left)

        # Add section heading for roommate breakdown
        pdf.set_font("Arial", size=16, style='B')
        pdf.cell(w=0, h=25, txt="Payment Breakdown", border=0, ln=1)

        # Add a small divider line under section heading
        current_y = pdf.get_y()
        pdf.set_draw_color(180, 180, 180)
        pdf.set_line_width(0.8)
        pdf.line(x1=content_left, y1=current_y + 3, x2=content_right, y2=current_y + 3)
        pdf.ln(12)
        pdf.set_x(content_left)

        # Set font for this section of PDF and insert column headings
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(w=table_name_width, h=25, txt="Roommate", border=0)
        pdf.cell(w=table_amount_width, h=25, txt="Amount Due", border=0, ln=1)

        # Move cursor to left content boundary for table rows
        pdf.set_x(content_left)

        # Add roommate payment information
        pdf.set_font("Arial", size=12)

        # roommate1 section
        pdf.cell(w=table_name_width, h=30, txt=roommate1.name, border=0)
        pdf.cell(w=table_amount_width, h=30, txt=roommate1_payment, border=0, ln=1)

        # Add light divider line between roommates
        current_y = pdf.get_y()
        pdf.set_draw_color(220, 220, 220)
        pdf.set_line_width(0.5)
        pdf.line(x1=content_left, y1=current_y, x2=content_right, y2=current_y)
        pdf.ln(5)
        pdf.set_x(content_left)

        # roommate2 section
        pdf.cell(w=table_name_width, h=30, txt=roommate2.name, border=0)
        pdf.cell(w=table_amount_width, h=30, txt=roommate2_payment, border=0, ln=1)

        # Disable auto page break so footer stays on current page
        pdf.set_auto_page_break(auto=False)

        pdf.set_y(page_height - 70)
        pdf.set_font("Arial", size=10, style='I')
        pdf.set_text_color(100, 100, 100)
        pdf.cell(
            w=0,
            h=15,
            txt="This report was automatically generated by the Roommate Billing App.",
            border=0,
            align='C'
        )

        # use os, (office standard) library to change directory to generated_pdf_reports
        # to output the generated PDFs there and open the PDF
        os.chdir('generated_pdf_reports')
        pdf.output(self.filename)
        webbrowser.open(self.filename)


class FileSharer:
    """
    Uploads a file to Filestack and returns a shareable URL.
    """


    def __init__(self, filepath, api_key=None):
        self.filepath = filepath
        self.api_key = api_key or FILESTACK_API_KEY

        if not self.api_key:
            raise ValueError("Filestack API key not found. Check your .env file.")
    def share(self):
        client = Client(self.api_key)
        new_file_link = client.upload(filepath=self.filepath)
        return new_file_link.url
