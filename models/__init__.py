"""
This module is the package constructor which creates a declarative base
and a handful of useful column types.
"""

from functools import partial

from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# usable column types
NullableColumn = partial(Column, nullable=True, default=None)
NotNullColumn = partial(Column, nullable=False)
NameColumn = partial(Column, String(100), nullable=False)
TextColumn = partial(Column, Text, nullable=True)
