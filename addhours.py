"""Add billable hours. Defaults to Bacon Sails & Marine Supplies"""

import sys
import decimal
from datetime import datetime, date

from sqlalchemy  import create_engine, func
from sqlalchemy.orm import sessionmaker

from models.invoices import Hours
from instance.development import SQLALCHEMY_DATABASE_URI


DEFAULT_CUSTOMER_ID = 2


def get_hours():
    prompt = 'Enter hours: '
    while True:
        response = input(prompt)
        try:
            return decimal.Decimal(response)
        except decimal.InvalidOperation:
            pass


def get_date():
    prompt = f'Enter date [{date.today()}]: '
    while True:
        response = input(prompt).strip()
        if response == '':
            return date.today()

        try:
            return date.fromisoformat(response)
        except ValueError:
            pass


def add_hours(db, cust_id=2, project_id=22):
    hrs = get_hours()
    performed = get_date()
    new_hours = Hours()
    new_hours.cust_id = cust_id
    new_hours.project_id = project_id
    new_hours.hrs = hrs
    new_hours.performed = performed
    new_hours.billing_status = 'U'
    new_hours.cre_dt = datetime.now()
    new_hours.mod_dt = datetime.now()
    db.add(new_hours)
    db.commit()
    return new_hours


def get_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    SessionFactory = sessionmaker(bind=engine)
    return SessionFactory()


if __name__ == '__main__':
    args = sys.argv[1:]
    customer_id = DEFAULT_CUSTOMER_ID
    if args:
        # assume first argument is customer ID
        try:
            customer_id = int(args.pop())
        except ValueError as e:
            print(e)
            sys.exit(0)

    db_session = get_session()
    hours = add_hours(db_session, cust_id=customer_id)
    print(hours)
