"""
Author:  Brian Wolf
Company:   Activus Technologies
Date:  2014.02.21
Module:  geninvoice.py
Description:  Generates an invoice
Modifications:
2020.11.19  keyword arguments
"""

import sys
import os
from configparser import ConfigParser
from datetime import datetime, date
from decimal import Decimal

from sqlalchemy  import create_engine, func
from sqlalchemy.orm import sessionmaker

from reportlab.platypus import SimpleDocTemplate, Table, Spacer
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

from instance.development import SQLALCHEMY_DATABASE_URI
from models.invoices import Customer, Hours, Project

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionFactory = sessionmaker(bind=engine)
db = SessionFactory()


CUSTOMER_ID = 2
PROJECT_ID = 30


class GenInvoice(object):
    def __init__(self, customer, hours, **kwargs):
        current_time = datetime.now()
        self.day_of_year = current_time.strftime('%y%j')
        self.PAGE_HEIGHT = defaultPageSize[1]
        self.PAGE_WIDTH = defaultPageSize[0]
        self.styles = getSampleStyleSheet()
        self.customer = customer
        self.hours = hours
        self.invoice_no = self.gen_invoice_number()
        for k,v in kwargs.items():
            setattr(self, k, v)
        self.logo_dir = '/home/bw/Documents/logo/activus'
        self.logo_fn = 'activus_logo_2011.png'
        self.pageinfo = f'Cognify Solutions Invoice {self.day_of_year} for {self.customer}'

    def first_page(self, canvas, doc):
        canvas.setAuthor = 'Cognify Solutions'
        canvas.setTitle = 'Cognify Solutions Invoice'
        canvas.setSubject = 'Cognify Solutions Invoice'
        canvas.saveState()
        canvas.setFont('Helvetica', 16)
        width = self.PAGE_WIDTH / 2.0
        height = self.PAGE_HEIGHT - 1.7 * inch
        canvas.drawCentredString(width, height, 'COGNIFY SOLUTIONS')
        canvas.drawImage(os.path.join(self.logo_dir, self.logo_fn), width - 1.7*inch, height)
        canvas.setFont('Helvetica', 11)
        line_height = 0.25 * inch
        for a, t in enumerate(('3817 Menlo Drive', 'Baltimore, MD 21215', '443-938-8127')):
            height -= line_height
            canvas.drawCentredString(width, height, t)
        height -= line_height
        canvas.drawCentredString(width, height, f'Invoice for {self.customer}')
        canvas.drawString(inch, 0.75 * inch, "Page 1: %s" % self.pageinfo)
        canvas.restoreState()

    def later_pages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 11)
        canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, self.pageinfo))
        canvas.restoreState()

    def gen_invoice_number(self):
        abbreviation = self.customer.abrv.upper()
        return f'{self.day_of_year}{abbreviation}'

    def make(self):
        filename = f"{self.invoice_no}.pdf"
        config = ConfigParser()
        config.read('development.ini')
        billing_dir = config.get('app:main', 'billing.invoices_dir')
        path = os.path.join(billing_dir, filename)
        doc = SimpleDocTemplate(path)

        # initial space from top of page
        story = [Spacer(1,2*inch)]

        # spacer used going forward
        spacer = Spacer(1,0.3*inch)

        # set colors
        HEADER_COLOR = '#E9F0F7'
        PRIMARY_COLOR = '#FFFFFF'
        ALT_COLOR = '#F1F1F1'
        BOX_COLOR = '#111'
        COLORS = [ALT_COLOR, PRIMARY_COLOR]

        # customer
        customer_style = [
            ('BACKGROUND', (1, 0), (1, 0), HEADER_COLOR),
            ('BACKGROUND', (3, 0), (3, 0), HEADER_COLOR),
            ('BACKGROUND', (5, 0), (5, 0), HEADER_COLOR),
            ('BOX', (0, 0), (-1, -1), 0.25, BOX_COLOR)
        ]
        customer_data = [
            (
                'Rate:', '{0:.2f}'.format(self.customer.rate),
                'Invoice:', self.invoice_no,
                'Date:', date.today().strftime('%b %-d, %Y')
            )
        ]
        t = Table(customer_data, style=customer_style)
        story.append(t)
        story.append(spacer)

        # summary
        total_hours = sum([h.Hours.hrs or 0 for h in self.hours])
        total_expenses = sum([h.Hours.amt_exp or 0 for h in self.hours])
        if self.maximum:
            total_amount = Decimal(self.maximum)
        else:
            total_amount = sum(
                [self.customer.rate * (h.Hours.hrs or 0) for h in self.hours]
            )
            total_amount += total_expenses
            if self.discount:
                total_amount -= Decimal(self.discount)
        summary = [
            ('Hours', 'Amount Due'),
            (total_hours, '{0:.2f} USD'.format(total_amount))
        ]
        summary_style = [
            ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
            ('BACKGROUND', (0, 0), (1, 0), HEADER_COLOR),
            ('BOX', (0, 0), (-1, -1), 0.25, BOX_COLOR)
        ]
        t = Table(summary, style=summary_style)
        story.append(t)
        story.append(spacer)

        # details
        data_style = [
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
            ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
            ('BOX', (0, 0), (-1, -1), 0.25, BOX_COLOR)
        ]

        data = []
        for n, h in enumerate(self.hours):
            # positive hours means use hours, not expense
            if h.Hours.hrs and h.Hours.hrs != 0:
                data.append((
                    h.Hours.performed.strftime('%m/%d/%Y'),
                    Paragraph(
                        self._combine(h.Project.name, h.Hours.comments), self.styles["BodyText"]),
                        '{0:.2f}'.format(h.Hours.hrs),
                        '{0:.2f}'.format(self.customer.rate * h.Hours.hrs or h.Hours.amt_exp)
                    )
                )
            # no hours implies an expense rather than hours
            else:
                data.append((
                    h.performed.strftime('%m/%d/%Y'),
                    Paragraph(
                    self._combine(h.project_name, h.Hours.comments), self.styles["BodyText"]),
                    '',
                    '{0:.2f}'.format(h.Hours.amt_exp),
                ))
            # set background color for alternating rows
            if n > 0:
                data_style.append(('BACKGROUND', (0, n), (-1, n), COLORS[n % 2]))

        if self.discount:
            discount = (
                datetime.now().strftime('%m/%d/%Y'),
                Paragraph('Courtesy Discount', self.styles["BodyText"]),
                '',
                '({0:.2f})'.format(Decimal(self.discount)))
            data.append(discount)
            # set background color for alternating rows
            data_style.append(('BACKGROUND', (0, len(data)), (-1, len(data)), COLORS[len(data) % 2]))

        data.insert(0, ('Date','Description','Hours','Amount'))
        col_widths = (0.8 * inch, 3.9 * inch, 0.8 * inch, 1.0 * inch)
        t = Table(data, style=data_style, colWidths=col_widths)
        story.append(t)

        # build PDF
        doc.build(story, onFirstPage=self.first_page, onLaterPages=self.later_pages)
        return path

    @staticmethod
    def _combine(project, comments=None):
        return project if (comments or '').strip() == '' else f'{project}: {comments}'


def get_customer(cust_id=2):
    return db.query(Customer).filter(Customer.id == cust_id).first()


def get_hours_months(cust_id=2, project_id=30, status='U'):
    current_month = date.today().month

    return (
        db.query(Hours, Project)
        .join(Project, Project.id == Hours.project_id)
        .filter(Hours.cust_id == cust_id)
        .filter(Hours.project_id == project_id)
        .filter(Hours.billing_status == status)
        .filter(func.month(Hours.performed) != current_month)
        .order_by(Hours.performed, Hours.id)
        .all()
    )


def get_hours(cust_id=2, project_id=30, status='U'):
    """
    Return a list of hours to be billed.
    :param cust_id: int
    :param project_id: int
    :param status: one character (U=unbilled, B=billed, P=paid)
    :return:
    """
    #today = date.today()
    #years_performed = (today.year, today.year - 1) if today.month == 1 else (today.year,)

    return (
        db.query(Hours, Project)
        .join(Project, Project.id == Hours.project_id)
        .filter(Hours.cust_id == cust_id)
        .filter(Hours.project_id == project_id)
        .filter(Hours.billing_status == status)
        #.filter(func.year(Hours.performed).in_(years_performed))
        .order_by(Hours.performed, Hours.id)
        .all()
    )


def get_extra_hours(cust_id=2, project_id=30, status='U'):
    class Data:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    extra_hours = Hours()
    extra_hours.cust_id = cust_id
    extra_hours.project_id = project_id
    extra_hours.hrs = Decimal('0.6')
    extra_hours.billing_status = status
    extra_hours.performed = date(2021, 12, 30)
    extra_hours.comments = "end of year; not billed until now"
    extra_hours.cre_dt = datetime.now()
    extra_hours.mod_dt = datetime.now()

    return [Data(Hours=extra_hours, Project=Data(name='Bacon Sails'))]


def get_month_performed():
    current_date = date.today()
    prev_month = lambda d: (d.year - 1, 12, d.day) if d.month == 1 else (d.year, d.month -1, d.day)
    last_month = current_date.replace(*prev_month(current_date))
    prompt = f'Enter month performed [{last_month}]: '
    while True:
        response = input(prompt).strip()
        if response == '':
            return last_month

        try:
            return date.fromisoformat(f'{response}-01')
        except ValueError:
            pass


def generate_invoice(cust_id, project_id, discount=0, status='U'):
    """
    Generate an invoice as a PDF document.
    :param cust_id: int
    :param project_id: int
    :param discount: numeric
    :return: None
    """
    customer = get_customer(cust_id)
    hours = get_hours(cust_id, project_id, status)
    maximum = 0
    invoice = GenInvoice(customer, hours, maximum=maximum, discount=discount)
    full_path = invoice.make()
    print(full_path)


if __name__ == '__main__':
    cust_proj_map = {CUSTOMER_ID: 22, 3: 30, 65:55, 68:60}
    customer_id = int(sys.argv[1]) if len(sys.argv) > 1 else CUSTOMER_ID
    try:
        project_id = int(sys.argv[2]) if len(sys.argv) > 2 else cust_proj_map.get(customer_id, PROJECT_ID)
    except ValueError:
        project_id = cust_proj_map.get(customer_id, PROJECT_ID)

    try:
        amount = int(sys.argv[3])
        generate_invoice_with_amount(customer_id, project_id, amount)
    except (ValueError, IndexError):
        pass

    status = sys.argv[-1] if sys.argv[-1] in ('U', 'B', 'P') else 'U'
    generate_invoice(cust_id=customer_id, project_id=project_id, discount=0, status=status)
