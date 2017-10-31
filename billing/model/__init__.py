# defines data model
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy import Table, Column, Integer, Boolean, String, Text, Date, Numeric
from sqlalchemy import ColumnDefault, ForeignKey
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.orm import relation
from sqlalchemy.ext.declarative import declarative_base
from billing.model import meta
from datetime import datetime


def init_model(engine):
    # must call this function before using any of the tables or classes in the model
    # reflected tables must be defined and mapped here

    # bind the engine (connection) to the session
    meta.Session.configure(bind=engine)
    meta.engine = engine


Base = declarative_base(metadata=meta.MetaData())


## non-reflected tables may be defined and mapped at module level
class Setting(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    field = Column(String(40))
    value = Column(String(40))

    def __repr__(self):
        return "<Setting(%s, %s, %s)>" % (self.id, self.field, self.value)


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    cust_id = Column(Integer)
    addr1 = Column(String(40))
    addr2 = Column(String(40))
    city = Column(String(40))
    state = Column(String(2))
    zipcode = Column(String(10))
    country = Column(String(10), default='US')
    addr_type = Column(String(1), default='B')
    status = Column(Boolean, default=True)
    cre_dt = Column(TIMESTAMP)
    mod_dt = Column(TIMESTAMP, default=datetime.now())

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<Address(%s, %s, %s)>" % (self.id, self.city, self.state)


class Bonus(Base):
    __tablename__ = 'bonuses'

    id = Column(Integer, primary_key=True)
    btype = Column(String(1), default='X')
    cust_id = Column(Integer)
    vol = Column(Numeric(10,2))
    amt = Column(Numeric(10,2))
    mo = Column(Integer)
    yr = Column(Integer)
    comment = Column(Text)
    cre_dt = Column(TIMESTAMP)
    mod_dt = Column(TIMESTAMP, default=datetime.now())

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<Bonus(%s, %s)>" % (self.id, self.cust_id)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    cat_nm = Column(String(20))
    status = Column(Boolean, default=True)
    cre_dt = Column(TIMESTAMP)
    mod_dt = Column(TIMESTAMP, default=datetime.now())

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<Category(%s, %s)>" % (self.id, self.cat_nm)


class CustomerType(Base):
    __tablename__ = 'customer_types'

    id = Column(Integer, primary_key=True)
    cust_type = Column(String(1))
    dscr = Column(String(40))

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<CustomerType(%s, %s, %s)>" % (self.id, self.cust_type, self.dscr)


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    account_id = Column(String(10))
    cust_nm = Column(String(40))
    legal_nm = Column(String(40))
    cust_type = Column(String(5))
    processor = Column(String(10))
    rate = Column(Numeric(10,2), nullable=True)
    abrv = Column(String(10), nullable=True)
    status = Column(Boolean, default=True)
    cre_dt = Column(TIMESTAMP)
    mod_dt = Column(TIMESTAMP, default=datetime.now())

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<Customer(%s, %s, %s)>" % (self.id, self.cust_nm, self.cust_type)


class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    vend_id = Column(Integer)
    amt = Column(Numeric(10,2))
    mo = Column(Integer)
    yr = Column(Integer)
    pay_mthd = Column(String(10))
    check_no = Column(Integer, default=None)
    comments = Column(Text)
    paid_dt = Column(TIMESTAMP)
    cre_dt = Column(TIMESTAMP)
    mod_dt = Column(TIMESTAMP, default=datetime.now())

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<Expense(%s, %s)>" % (self.vend_id, self.amt)


class Revenue(Base):
    __tablename__ = 'revenues'

    id = Column(Integer, primary_key=True)
    total = Column(Numeric(10,2))
    dep_dt = Column(Date)
    cre_dt = Column(TIMESTAMP)
    mod_dt = Column(TIMESTAMP, default=datetime.now())

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<Revenue(%s, %s, %s)>" % (self.id, self.cust_id, self.total)


class RevenueDetail(Base):
    __tablename__ = 'revenuedetails'

    id = Column(Integer, primary_key=True)
    cust_id = Column(Integer, ForeignKey('customers.id'))
    rev_id = Column(Integer, ForeignKey('revenues.id'))
    amt = Column(Numeric(10,2))
    rcv_dt = Column(Date)
    mod_dt = Column(TIMESTAMP, default=datetime.now())
    comments = Column(Text)

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<RevenueDetail(%s, %s)>" % (self.rev_id, self.amt)


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    cust_id = Column(Integer, ForeignKey('customers.id'))
    name = Column(String(40))
    status = Column(Boolean, default=True)
    cre_dt = Column(TIMESTAMP)
    mod_dt = Column(TIMESTAMP, default=datetime.now())
    comments = Column(Text)

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<Project(%s, %s, %s)>" % (self.cust_id, self.project_id, self.hrs)


class Hours(Base):
    __tablename__ = 'hours'

    id = Column(Integer, primary_key=True)
    cust_id = Column(Integer, ForeignKey('customers.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    hrs = Column(Numeric(10,3), nullable=True)
    billing_status = Column(String(1), default='U')
    performed = Column(Date)
    cre_dt = Column(TIMESTAMP)
    mod_dt = Column(TIMESTAMP, default=datetime.now())
    amt_exp = Column(Numeric(10,2), nullable=True)
    comments = Column(Text)

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<Hours(%s, %s, %s)>" % (self.cust_id, self.project_id, self.hrs)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    usrnam = Column(String(20))
    salutation = Column(String(10))
    first_name = Column(String(20))
    middle_name = Column(String(20))
    last_name = Column(String(20))
    email = Column(String(80))
    pwd = Column(String(20))
    status = Column(Boolean, default=True)
    cre_dt = Column(TIMESTAMP, default=datetime.now())
    login_dt = Column(TIMESTAMP)

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return "<User(%s %s)>" % (self.first_name, self.last_name)


class Vendor(Base):
    __tablename__ = 'vendors'

    id = Column(Integer, primary_key=True)
    cat_id = Column(Integer)
    vend_nm = Column(String(40))
    status = Column(Boolean, default=True)
    cre_dt = Column(TIMESTAMP)
    mod_dt = Column(TIMESTAMP, default=datetime.now())

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<Vendor('%s', '%s')>" % (self.cat_id, self.vend_nm)
