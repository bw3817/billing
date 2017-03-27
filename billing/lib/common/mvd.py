#!/usr/local/bin/python

#----------------------------------------------------------------------
# Author:            Brian Wolf
# Date:              2012.04.03
# Module:            mvd.py
# Description:       Import merchant volume data (mvd) from a spreadsheet
#                    in a designated directory
#
# Modifications:
#
#
#----------------------------------------------------------------------


import sys
import os
import glob
import xlrd
from decimal import Decimal

parent_dir = '/home/brian/projects/billing'
sys.path.append(parent_dir)
from billing.model import *
from ..common.utils import Utils

u = Utils()
billing_xcharge_commissions_dir = u.get_value(os.path.join(parent_dir, 'development.ini'), 'billing.xcharge_commissions_dir')


class MerchantVolumeData:
    def __init__(self, db):
        self.db = db


    def process(self, yr, filespec):
        if not os.path.exists(filespec):
            if not filespec.endswith('.xls'):
                filespec += '.xls'
            filespec = os.path.join(billing_xcharge_commissions_dir, str(yr), filespec)
        path, filename = os.path.split(filespec)
        fn, ext = os.path.splitext(filename)
        yr, mo = fn.split("-")
        book = xlrd.open_workbook(filespec)
        sheet = book.sheet_by_index(0)
        b_is_ready = False
        ACCOUNT_PREFIX = 'PA-'
        MERCHANT_ID = 0
        #MERCHANT_NAME = 1
        VOLUME = 9 #13
        COMMISION = 13 #25
        #PROCESSOR = 3 #19

        for row in range(2, sheet.nrows):
            if not b_is_ready:
                if str(sheet.cell_value(rowx=row, colx=0)).strip() in ('Account', 'Reseller Accounts'):
                    b_is_ready = True
                continue
            volume_str = str(sheet.cell_value(rowx=row, colx=VOLUME)).strip()
            if volume_str == '': continue
            # raw data
            volume = Decimal(volume_str)
            merchant_id = str(sheet.cell_value(rowx=row, colx=MERCHANT_ID)).strip()
            if merchant_id.lower().startswith('total'): break
            if merchant_id.startswith('PA-'):
                merchant_id = merchant_id[len(ACCOUNT_PREFIX):]
            commission_str = str(sheet.cell_value(rowx=row, colx=COMMISION)).strip()
            commission = Decimal(commission_str)
            # get customer from ID
            customer = self.db.query(Customer).filter(Customer.account_id == merchant_id).first()
            if customer is None: continue

            # 2013.06.18 bw
            # update if already exists; add otherwise
            qry = self.db.query(Bonus)
            qry = qry.filter(Bonus.cust_id == customer.id)
            qry = qry.filter(Bonus.yr == int(yr))
            qry = qry.filter(Bonus.mo == int(mo))
            qry = qry.filter(Bonus.btype == 'X')
            bonus = qry.first()
            if bonus is None:
            # record commission
                bonus = Bonus()
                bonus.btype = 'X'
                bonus.cust_id = customer.id
                bonus.vol = volume
                bonus.amt = commission
                bonus.yr = int(yr)
                bonus.mo = int(mo)
                bonus.cre_dt = bonus.mod_dt = datetime.now()
                self.db.add(bonus)
            else:
                bonus.vol = volume
                bonus.amt = commission
                bonus.mod_dt = datetime.now()
        self.db.commit()


    def process_all(self, yr=datetime.year):
        yr = str(yr)
        path = os.path.join(billing_xcharge_commissions_dir, yr)
        if not os.path.isdir(path):
            return 0
        for filename in glob.glob(os.path.join(path, '*.xls')):
            self.process(filename)


    #def read(self, filename):
    #    path = os.path.join(billing_xcharge_commissions_dir, 'spreadsheets', filename)
    #    if not os.path.exists(path):
    #        return 0
    #    self.process(path)
    #    return 1


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    dburl = "mysql://root:chazak@localhost/billing"
    engine = create_engine(dburl)
    Session = sessionmaker(bind=engine)
    db = Session()
    mvd = MerchantVolumeData(db)
    mo = raw_input("Month >> ")
    yr = raw_input("Year >> ")
    mvd.read('{1}-{0}.xls'.format(mo,yr))
