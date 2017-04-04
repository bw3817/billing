# controller: customers
from pylons import config, url, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from billing.lib.baseplus import BasePlusController, render
import billing.model as model
import billing.lib.helpers as h
from datetime import datetime,date
from decimal import Decimal

# SQL functios
from sqlalchemy import or_, and_, not_, func
from sqlalchemy.sql.functions import coalesce, concat, sum
from sqlalchemy.sql.expression import distinct


class CustomersController(BasePlusController):
    def index(self):
        return render('/customers/index.mako')


    def _getLetters(self):
        # get distinct first letter of customer names
        sql = """select distinct left(cust_nm,1) as letter
        from customers
        where status = 1
        order by left(cust_nm,1)
        """
        conn = self.db.connection()
        letters = conn.execute(sql).fetchall()
        return letters


    def find(self, letter=None):
        if letter is None:
            customers = []
        else:
            letter += '%'
            customers = self.db.query(model.Customer).filter(model.Customer.cust_nm.like(letter)).order_by(model.Customer.cust_nm).all()
        return render('/customers/find.mako', extra_vars={'letters':self._getLetters(), 'customers':customers})


    def all(self):
        customers = self.db.query(model.Customer).order_by(model.Customer.cust_nm).all()
        return render('/customers/find.mako', extra_vars={'letters':self._getLetters(), 'customers':customers})


    def xcharge(self, xaction=None, id=None):
        if xaction == 'view':
            qry = self.db.query(model.Customer)
            qry = qry.filter(model.Customer.cust_type.like('%X%'))
            #qry = qry.filter(model.Customer.status == True)
            #qry = qry.filter(or_(model.Customer.status == True, 
            #                     and_(model.Customer.status == False, model.Customer.amt > 0)))
            qry = qry.order_by(model.Customer.cust_nm)
            customers = qry.all()
            for customer in customers:
                yr = session.get('yr', date.today().year)
                mo = session.get('mo', date.today().month)
                qry = self.db.query(model.Bonus)
                qry = qry.filter(model.Bonus.cust_id == customer.id)
                qry = qry.filter(model.Bonus.yr == yr)
                qry = qry.filter(model.Bonus.mo == mo)
                bonus = qry.first()
                customer.bonus = bonus
            return render('/customers/xcharge.mako', extra_vars={'customers':customers})

        elif xaction == 'setmonth':
            return render('/customers/setmonth.mako')

        elif xaction == 'add':
            bonus = model.Bonus()
            customer = self.db.query(model.Customer).filter(model.Customer.id == id).first()
            return render('/customers/xcharge_commissions.mako', extra_vars={'customer':customer, 'bonus':bonus})

        elif xaction == 'edit':
            bonus = self.db.query(model.Bonus).filter(model.Bonus.id == id).first()
            customer = self.db.query(model.Customer).filter(model.Customer.id == bonus.cust_id).first()
            return render('/customers/xcharge_commissions.mako', extra_vars={'customer':customer, 'bonus':bonus})

        elif xaction == 'report':
            sql = """
            select
                yr,
                sum(amt) as sum_amt, sum(vol) as sum_vol,
                avg(amt) as avg_amt, avg(vol) as avg_vol,
                count(*) as cnt
            from bonuses
            group by yr
            order by yr
            """
            conn = self.db.connection()
            bonuses = conn.execute(sql).fetchall()
            return render('/customers/xcharge_report.mako', extra_vars={'bonuses':bonuses})

        elif xaction == 'mvd':
            return render('/customers/mvd.mako')

        return render('/customers/error.mako')


    def bonus(self):
        if request.params['bonus_id'] == '':
            bonus = model.Bonus()
        else:
            bonus = self.db.query(model.Bonus).filter(model.Bonus.id == request.params['bonus_id']).first()
        bonus.btype = 'X'
        bonus.cust_id = request.params['cust_id']
        bonus.mo = session['mo']
        bonus.yr = session['yr']
        bonus.vol = request.params['vol'].replace(',','')
        bonus.amt = request.params['amt'].replace(',','')
        bonus.cre_dt = datetime.now()
        self.db.add(bonus)
        self.db.commit()
        redirect(url('/customers/xcharge/view'))


    def setmonth(self):
        session['mo'] = int(request.params['mo'])
        session['yr'] = int(request.params['yr'])
        session.save()
        redirect(url('/customers/xcharge/view'))


    def prevmonth(self):
        if session['mo'] == 1:
            session['mo'] = 12
            session['yr'] -= 1
        else:
            session['mo'] -= 1
        session.save()
        redirect(url('/customers/xcharge/view'))


    def nextmonth(self):
        if session['mo'] == 12:
            session['mo'] = 1
            session['yr'] += 1
        else:
            session['mo'] += 1
        session.save()
        redirect(url('/customers/xcharge/view'))


    def new(self):
        customer = model.Customer()
        customer_types = self.db.query(model.CustomerType).order_by(model.CustomerType.dscr).all()
        return render('/customers/new.mako', extra_vars=dict(customer=customer, customer_types=customer_types))


    def view(self, cust_id=None):
        if cust_id is None:
            cust_id = session['cust_id']
        else:
            session['cust_id'] = cust_id
            session.save()
        customer = self.db.query(model.Customer).filter(model.Customer.id == cust_id).first()
        if customer is None:
            customer = model.Customer()
        bonus = {}
        sql = """
        select
          yr,
          sum(amt) as sum_amt, sum(vol) as sum_vol,
          avg(amt) as avg_amt, avg(vol) as avg_vol,
          count(*) as cnt
        from bonuses
        where cust_id = %s
        group by yr
        order by yr
        """
        conn = self.db.connection()
        bonuses = conn.execute(sql, (cust_id,)).fetchall()
        customer_types = self.db.query(model.CustomerType).order_by(model.CustomerType.dscr).all()
        return render('/customers/view.mako', extra_vars=dict(customer=customer, bonuses=bonuses, customer_types=customer_types))


    def edit(self, cust_id=None):
        session['cust_id'] = cust_id
        session.save()
        customer = self.db.query(model.Customer).filter(model.Customer.id == cust_id).first()
        if customer is None:
            customer = model.Customer()
        customer_types = self.db.query(model.CustomerType).order_by(model.CustomerType.dscr).all()
        return render('/customers/new.mako', extra_vars=dict(customer=customer, customer_types=customer_types))


    def save(self):
        if 'cust_nm' in request.params:
            if request.params.get('cust_id','') == '':
                customer = model.Customer()
                customer.cre_dt = datetime.now()
                self.db.add(customer)
            else:
                customer = self.db.query(model.Customer).filter(model.Customer.id == request.params['cust_id']).first()
            customer.cust_nm = request.params['cust_nm']
            customer.account_id = request.params['account_id']
            customer.processor = request.params['processor']
            customer.cust_type = ''.join(request.params.getall('cust_type'))
            rate = (request.params.get('rate') or '').strip()
            if rate == '':
                customer.rate = None
                customer.abrv = None
            else:
                customer.rate = rate
                customer.abrv = request.params.get('abrv')
            customer.status = int(request.params['status'])
            customer.mod_dt = datetime.now()
            self.db.commit()
            session['cust_id'] = customer.id
            session.save()
            h.flash("Database updated.")
            redirect(url.current(action='view'))
        else:
            h.flash("Missing required data.")
            redirect(url.current(action='find'))
