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


def add_expenses(db, yr, vendor_id, amount=1.00, pay_mthd='cc'):
    for mo in range(1, 12+1):
        expense = (
            db.query(Expense)
            .filter(Expense.yr == yr)
            .filter(Expense.mo == mo)
            .filter(Expense.vend_id == vendor_id)
            .first()
        )
        if not expense:
            expense = Expense()
            expense.vend_id = vendor_id
            expense.amt = amount
            expense.mo = mo
            expense.yr = yr
            expense.pay_mthd = pay_mthd
            expense.cre_dt = expense.mod_dt = datetime.now()
            db.add(expense)
        db.commit()


if __name__ == "__main__":
    dburl = "mysql://root:chazak@localhost/billing"
    engine = create_engine(dburl)
    SessionFactory = sessionmaker(bind=engine)
    db = SessionFactory()

    year = 2022
    for vend_id in (7, 24, 69, 90, 9, 11, 73, 85, 89):
        add_expenses(db, year, vend_id)
