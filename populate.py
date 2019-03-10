from datetime import datetime, date, timedelta
from billing.model import Expense
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#import billing.model.meta as meta


def first_working_day(mo, yr):
    d = date(yr, mo, 1)
    while d.weekday() > 4:
        d += timedelta(days=1)
    return d


def last_working_day(mo, yr):
    next_month = lambda m,y: date(y, m+1, 1) if m < 12 else date(yr+1, 1, 1)
    d = next_month(mo, yr)
    d -= timedelta(days=1)
    while d.weekday() > 4:
        d -= timedelta(days=1)
    return d


def add_expenses(db, yr, vendor_id, amt):
    for mo in range(1, 12+1):
        expense = Expense()
        expense.vend_id = vendor_id
        expense.amt = amt
        expense.mo = mo
        expense.yr = yr
        expense.pay_mthd = 'cc'
        if vendor_id == 85:
            expense.paid_dt = last_working_day(mo, yr)
        elif vendor_id == 89:
            expense.paid_dt = first_working_day(mo, yr)
        #print expense.mo, expense.yr, vendor_id, expense.amt, expense.paid_dt
        expense.cre_dt = expense.mod_dt = datetime.now()
        db.add(expense)
    db.commit()


if __name__ == "__main__":
    dburl = "mysql://root:chazak@localhost/billing"
    engine = create_engine(dburl)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    #db_session = meta.Session()

    current_date = date.today()
    current_year = current_date.year if current_date.month == 1 else current_date.year + 1

    for vend_id, amt in ((85, 7), (89, 12)):
        add_expenses(db_session, current_year, vend_id, amt)
