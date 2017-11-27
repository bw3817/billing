# controller: expenses
import billing.model as model
import billing.lib.helpers as h
import simplejson as json
from pylons import config, url, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from billing.lib.baseplus import BasePlusController, render
from billing.lib.common.rowdata import RowData
from billing.lib.common.utils import Utils
from datetime import datetime, date


# form handling
from formencode import Schema, validators, htmlfill
from pylons.decorators import validate
from pylons.decorators.rest import restrict


ISO_DATE_FORMAT = "%Y-%m-%d"


class ExpenseData(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    #iso_date_pattern = """^(\d{4}(?:(?:(?:\-)?(?:00[1-9]|0[1-9][0-9]|[1-2][0-9][0-9]|3[0-5][0-9]|36[0-6]))?|(?:(?:\-)?(?:1[0-2]|0[1-9]))?|(?:(?:\-)?(?:1[0-2]|0[1-9])(?:\-)?(?:0[1-9]|[12][0-9]|3[01]))?|(?:(?:\-)?W(?:0[1-9]|[1-4][0-9]5[0-3]))?|(?:(?:\-)?W(?:0[1-9]|[1-4][0-9]5[0-3])(?:\-)?[1-7])?)?)$"""
    iso_date_pattern = """^([0-9]{4})(?:(1[0-2]|0[1-9])|-?(1[0-2]|0[1-9])-?)(3[0-1]|0[1-9]|[1-2][0-9])$"""
    #year_month_pattern = """^([0-9]{4})-(1[0-2]|0[1-9]|[1-9])$"""
    year_month_pattern = """^([0-9]{4})-(1[0-2]|0[1-9]|[1-9])*"""
    vend_id = validators.Int(not_empty=True, strip=True, messages={"empty":"Please select a vendor."})
    pay_mthd = validators.String(not_empty=True, strip=True, messages={"empty":"Please select a payment method."})
    dt = validators.Regex(regex=year_month_pattern, not_empty=True, strip=True, messages={"empty":"Please enter the month payment applies to."})
    paid_dt = validators.Regex(regex=iso_date_pattern, not_empty=True, strip=True, messages={"empty":"Please enter the payment date."})
    amt = validators.Number(not_empty=True, strip=True, messages={"empty":"Please enter the payment amount."})


class ExpensesController(BasePlusController):
    def index(self):
        return render('/expenses/index.mako')


    def report(self):
        c.start_dt = request.params.get('start_dt','')
        c.end_dt = request.params.get('end_dt','')
        c.cat_id = request.params.get('cat_id')
        c.vend_id = request.params.get('vend_id')

        # categories
        categories = self.db.query(model.Category).filter(model.Category.status == True).order_by(model.Category.cat_nm).all()

        # get vendors
        qry = self.db.query(model.Vendor)
        qry = qry.filter(model.Vendor.status == True)
        if c.cat_id is not None:
            qry = qry.filter(model.Vendor.cat_id == c.cat_id)
        qry = qry.order_by(model.Vendor.vend_nm)
        vendors = qry.all()
        return render('/expenses/report.mako', extra_vars={'vendors':vendors, 'categories':categories})


    def eoy(self, yr, mo_start=1, mo_end=12):
        sql = """
        select c.cat_nm, v.vend_nm, sum(amt) as sum_amt
        from expenses e
        join vendors v
          on v.id = e.vend_id
        join categories c
          on c.id = v.cat_id
        where e.yr = %s
        group by c.cat_nm, e.vend_id
        order by c.cat_nm, v.vend_nm
        """
        conn = self.db.connection()
        c.rows = conn.execute(sql, yr).fetchall()
        return render('/expenses/eoy.mako')


    def results(self):
        # get criteria; defaults to: first day to last day of current month
        c.start_dt = request.params['start_dt']
        c.end_dt = request.params['end_dt']
        if c.start_dt == '':
            c.start_dt = date.today().replace(day=1).strftime(ISO_DATE_FORMAT)
        if c.end_dt == '':
            c.end_dt = self._endofmonth(c.start_dt).strftime(ISO_DATE_FORMAT)
        cat_id = request.params.get('cat_id', 'all')
        vend_id = request.params.get('vend_id', 'all')

        # pull expenses that match criteria
        qry = self.db.query(model.Expense)
        if cat_id is not None:
            qry = qry.join(model.Vendor, model.Vendor.id == model.Expense.vend_id)
            qry = qry.join(model.Category, model.Category.id == model.Vendor.cat_id)
            qry = qry.add_column(model.Vendor.vend_nm)
            if cat_id != 'all':
                qry = qry.filter(model.Category.id == cat_id)
            if vend_id != 'all':
                qry = qry.filter(model.Vendor.id == vend_id)
        qry = qry.filter(model.Expense.paid_dt >= c.start_dt)
        qry = qry.filter(model.Expense.paid_dt <= c.end_dt)
        expenses = qry.order_by(model.Expense.paid_dt, model.Expense.id)
        c.expenses = []
        for expense in expenses:
            r = RowData(expense.Expense)
            r.vend_nm = expense.vend_nm
            c.expenses.append(r)

        # display template
        c.start_dt_str = datetime.strptime(c.start_dt, ISO_DATE_FORMAT).strftime(ISO_DATE_FORMAT)
        c.end_dt_str = datetime.strptime(c.end_dt, ISO_DATE_FORMAT).strftime(ISO_DATE_FORMAT)
        c.cat_id = cat_id
        c.vend_id = vend_id
        return render('/expenses/results.mako')


    def new(self):
        qry = self.db.query(model.Vendor).join((model.Category, model.Category.id == model.Vendor.cat_id))
        qry = qry.filter(model.Vendor.status == True)
        qry = qry.add_column(model.Category.cat_nm)
        vendors = qry.order_by(model.Vendor.vend_nm, model.Category.cat_nm).all()
        c.vendors = []
        for vendor in vendors:
            v = RowData(vendor.Vendor)
            v.cat_nm = vendor.cat_nm
            c.vendors.append(v)
        c.expense = model.Expense()
        return render('/expenses/new.mako')


    def view(self, exp_id=None):
        if exp_id is None:
            exp_id = session['exp_id']
        else:
            session['exp_id'] = exp_id
            session.save()
        qry = self.db.query(model.Expense)
        qry = qry.join(model.Vendor, model.Vendor.id == model.Expense.vend_id)
        qry = qry.add_column(model.Vendor.vend_nm)
        expense = qry.filter(model.Expense.id == exp_id).first()
        if expense:
            exp = RowData(expense.Expense)
            exp.vend_nm = expense.vend_nm
        else:
            exp = RowData(model.Expense())
            exp.vend_nm = None
        return render('/expenses/view.mako', extra_vars={'expense':exp})


    def edit(self, exp_id=None):
        session['exp_id'] = exp_id
        session.save()
        conn = self.db.connection()
        sql = """
        select vendors.*, categories.cat_nm
        from vendors
        join categories
        on categories.id = vendors.cat_id
        where vendors.status = 1
        order by vendors.vend_nm, categories.cat_nm
        """
        c.vendors = conn.execute(sql).fetchall()
        c.expense = self.db.query(model.Expense).filter(model.Expense.id == exp_id).first()
        if c.expense is None:
            c.expense = model.Expense()
        return render('/expenses/new.mako')


    @restrict('POST')
    @validate(schema=ExpenseData(), form='new', post_only=False, on_get=True)
    def save(self):
        if request.params.get('exp_id','') == '':
            expense = model.Expense()
            expense.cre_dt = datetime.now()
        else:
            expense = self.db.query(model.Expense).filter(model.Expense.id == request.params['exp_id']).first()
        expense.vend_id = request.params['vend_id']
        expense.amt = request.params['amt'].replace(',','')
        expense.paid_dt = request.params.get('paid_dt')
        expense.pay_mthd = request.params.get('pay_mthd')
        expense.check_no = None
        if 'check_no' not in request.params or request.params.get('check_no','') == '':
            expense.check_no = None
        else:
            expense.check_no = request.params.get('check_no')
        dt_parts = request.params.get('dt').split('-')
        # year and month only (not day)
        expense.yr = dt_parts[0]
        expense.mo = dt_parts[1]
        expense.mod_dt = datetime.now()
        expense.comments = request.params.get('comments')
        self.db.add(expense)
        self.db.commit()
        session['exp_id'] = expense.id
        session.save()
        h.flash("Database updated.")
        redirect(url.current('view'))


    def delete(self):
        if request.params.get('exp_id','') == '':
            h.flash("Expense not deleted; missing ID.")
            redirect(url.current('index'))
        expense = self.db.query(model.Expense).filter(model.Expense.id == request.params['exp_id']).first()
        self.db.delete(expense)
        self.db.commit()
        h.flash("Database updated.")
        redirect(url.current('index'))


    def duplicate(self):
        utils = Utils()

        #import logging
        #log = logging.getLogger(__name__)
        newrows = []
        for cbx_id in request.GET.get('cbx','').split(','):
            qry = self.db.query(model.Expense, model.Vendor.vend_nm)
            qry = qry.join(model.Vendor, model.Vendor.id == model.Expense.vend_id)
            qry = qry.filter(model.Expense.id == int(cbx_id))
            qry = qry.add_column(model.Expense.vend_id)
            qry = qry.add_column(model.Expense.amt)
            qry = qry.add_column(model.Expense.pay_mthd)
            qry = qry.add_column(model.Expense.check_no)
            qry = qry.add_column(model.Expense.comments)
            old_expense = qry.one()

            dt = datetime.now()
            new_expense = model.Expense(cre_dt=dt, mod_dt=dt)
            for col in ['vend_id', 'amt', 'pay_mthd', 'check_no', 'comments']:
                setattr(new_expense, col, getattr(old_expense, col))
            new_expense.mo = dt.month
            new_expense.yr = dt.year
            new_expense.paid_dt = dt.date()
            self.db.add(new_expense)
            self.db.commit()

            d = dict(
                id=new_expense.id,
                vendor=old_expense.vend_nm,
                method=utils.PAYMENT_METHODS.get(new_expense.pay_mthd, ''),
                check=new_expense.check_no or '',
                paid_dt=new_expense.paid_dt.isoformat(),
                month='{mo} {yr}'.format(mo=utils.MONTHS[new_expense.mo - 1], yr=new_expense.yr),
                amount=new_expense.amt,
                comments=new_expense.comments,
                )
            newrows.append(d)

        # send response to browser
        response.headers['Content-Type'] = 'application/json'
        return json.dumps(newrows)
