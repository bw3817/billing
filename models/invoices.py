"""Models to track printing of barcode labels."""

from sqlalchemy import (
    Column, ForeignKey,
    Integer, Numeric, Boolean, String, Text, DateTime, Date
)

from models import Base, NullableColumn, NotNullColumn


class Customer(Base):
    """Define a customer."""

    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = NotNullColumn(String(10))
    cust_nm = NotNullColumn(String(40))
    legal_nm = NullableColumn(String(40))
    cust_type = NullableColumn(String(5))
    processor = NullableColumn(String(10))
    acct_type = NullableColumn(String(1))
    rate = NullableColumn(Numeric(10, 2))
    abrv = NullableColumn(String(10))
    status = NotNullColumn(Boolean, default=1)
    cre_dt = NullableColumn(DateTime)
    mod_dt = NullableColumn(DateTime)


class Hours(Base):
    """Define a customer."""

    __tablename__ = 'hours'

    id = NotNullColumn(Integer, primary_key=True, autoincrement=True)
    cust_id = NotNullColumn(Integer)
    project_id = NotNullColumn(Integer)
    hrs = NullableColumn(Numeric(10, 2))
    billing_status = NotNullColumn(String(1))
    performed = NullableColumn(Date)
    cre_dt = NullableColumn(DateTime)
    mod_dt = NullableColumn(DateTime)
    amt_exp = NullableColumn(Numeric(10, 2))
    comments = NullableColumn(Text)

    def __str__(self):
        return f'Hours({self.id}, {self.cust_id}, {self.project_id}, {self.hrs})'

    def __repr__(self):
        return str(self)


class Project(Base):
    """Define a customer."""

    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cust_id = NotNullColumn(Integer)
    name = NotNullColumn(String(40))
    status = NotNullColumn(Boolean, default=1)
    cre_dt = NullableColumn(DateTime)
    mod_dt = NullableColumn(DateTime)
    comments = NullableColumn(Text)

    def __str__(self):
        return f'Project({self.id}, {self.cust_id})'

    def __repr__(self):
        return str(self)
