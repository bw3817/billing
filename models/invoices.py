"""Models to track printing of barcode labels."""

from sqlalchemy import (
    Column, ForeignKey,
    Integer, Numeric, Boolean, String, Text, DateTime, Date
)
from sqlalchemy.ext.hybrid import hybrid_property

from models import Base, NullableColumn, NotNullColumn


class Customer(Base):
    """Define a customer."""

    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = NotNullColumn(Text)
    legal_name = NullableColumn(Text)
    code = NotNullColumn(Text)
    rate = NotNullColumn(Numeric(10, 2))
    status = NotNullColumn(Integer, default=1)
    create_dt = NotNullColumn(DateTime)

    @hybrid_property
    def abbreviation(self):
        return self.name.split()[0].upper()

    def __str__(self):
        return self.name


class Hours(Base):
    """Define a customer."""

    __tablename__ = 'hours'

    id = NotNullColumn(Integer, primary_key=True, autoincrement=True)
    project_id = NotNullColumn(Integer)
    hrs = NullableColumn(Numeric(10, 2))
    status = NotNullColumn(Boolean, default=1)
    perform_date = NullableColumn(Date)
    comments = NullableColumn(Text)

    def __str__(self):
        return f'Hours({self.id}, {self.project_id}, {self.hrs})'

    def __repr__(self):
        return str(self)


class Project(Base):
    """Define a project."""

    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = NotNullColumn(Integer)
    name = NotNullColumn(String(40))

    def __str__(self):
        return f'Project({self.id}, {self.customer_id})'

    def __repr__(self):
        return str(self)
