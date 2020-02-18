# controller: revenues
from pylons import config, url, request, session, tmpl_context as c
from pylons.controllers.util import redirect
from billing.lib.baseplus import BasePlusController, render
import billing.model as model
import billing.lib.helpers as h
from billing.lib.common.rowdata import RowData
from datetime import datetime, date, timedelta
from decimal import Decimal

# SQL functions
from sqlalchemy import or_, and_, not_, func, distinct, extract

# form handling
import formencode


class RevenueForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    amt = formencode.validators.String(not_empty=True, strip=True, messages={"empty":"Enter an amount."})
    cust_id = formencode.validators.String(not_empty=True, strip=True, messages={"empty":"Select a customer."})


class RevenuesController(BasePlusController):
    def __init__(self):
        BasePlusController.__init__(self)
        self.FMT = "%Y-%m-%d"


    def index(self):
        return render('/revenues/index.mako')


    def find(self):
        revenues = self.db.query(model.Revenue).order_by(model.Revenue.dep_dt).all()
        return render('/revenues/revenues.mako', extra_vars={'revenues':revenues})


    def new(self):
        c.revenue = model.Revenue()
        c.revenue.details = []
        customer_types = self.db.query(model.CustomerType).order_by(model.CustomerType.dscr).all()
        customer_type_list = or_( * [model.Customer.cust_type.contains(t)
                                     for t in [ct.cust_type for ct in customer_types]] )
        qry = self.db.query(model.Customer)
        qry = qry.filter(customer_type_list)
        #qry = qry.filter(model.Customer.status == True)
        qry = qry.order_by(model.Customer.cust_nm)
        c.customers = qry.all()
        return render('/revenues/new.mako')


    def view(self, rev_id=None):
        if rev_id is None:
            rev_id = session['rev_id']
        else:
            session['rev_id'] = rev_id
            session.save()
        revenue = self.db.query(model.Revenue).filter(model.Revenue.id == rev_id).first()
        if revenue is None:
            revenue = model.Revenue()
        c.revenue = RowData(revenue)
        c.revenue.details = []
        qry = self.db.query(model.RevenueDetail)
        qry = qry.join(model.Customer, model.Customer.id == model.RevenueDetail.cust_id)
        qry = qry.filter(model.RevenueDetail.rev_id == rev_id)
        qry = qry.add_column(model.Customer.cust_nm)
        qry = qry.order_by(model.RevenueDetail.id)
        details = qry.all()
        for detail in details:
            d = RowData(detail.RevenueDetail)
            d.cust_nm = detail.cust_nm
            c.revenue.details.append(d)
        return render('/revenues/view.mako')


    def edit(self, rev_id=None):
        session['rev_id'] = rev_id
        session.save()
        customer_types = self.db.query(model.CustomerType).order_by(model.CustomerType.dscr).all()
        customer_type_list = or_( * [model.Customer.cust_type.contains(t) for t in [ct.cust_type for ct in customer_types]] )
        c.customers = self.db.query(model.Customer).filter(customer_type_list).filter(model.Customer.status == True).order_by(model.Customer.cust_nm).all()
        revenue = self.db.query(model.Revenue).filter(model.Revenue.id == rev_id).first()
        if revenue is None:
            revenue = model.revenue()
        c.revenue = RowData(revenue)
        c.revenue.details = []
        details = self.db.query(model.RevenueDetail).filter(model.RevenueDetail.rev_id == revenue.id).order_by(model.RevenueDetail.id).all()
        for detail in details:
            c.revenue.details.append(RowData(detail))
        return render('/revenues/new.mako')


    def save(self):
        if request.params.get('rev_id','') == '':
            revenue = model.Revenue()
            revenue.cre_dt = revenue.mod_dt = datetime.now()
        else:
            revenue = self.db.query(model.Revenue).filter(model.Revenue.id == request.params['rev_id']).first()

        # revenue (parent)
        revenue.total = request.params.get('amt',0)
        revenue.dep_dt = request.params.get('dep_dt') or date.today().isoformat()
        revenue.cre_dt = datetime.now()
        self.db.add(revenue)
        self.db.commit()
        session['rev_id'] = revenue.id
        session.save()

        # capture details (children)
        html_data = {}
        for k,v in request.params.items():
            parts = k.split('.')
            if parts[0] == 'detail':
                indx = int(parts[1])
                if indx not in html_data:
                    html_data[indx] = {}
                html_data[indx][parts[2]] = v

        # update details
        for indx,data in html_data.items():
            # existing row
            if 'id' in data:
                qry = self.db.query(model.RevenueDetail)
                qry = qry.filter(model.RevenueDetail.id == int(data['id']))
                detail = qry.first()
                if 'cbx' in data:
                    self.db.delete(detail)
                else:
                    detail.cust_id = data['cust_id']
                    detail.amt = data['amt'].replace(',','')
                    detail.rcv_dt = data['rcv_dt']
                    detail.mod_dt = datetime.now()
                    detail.comments = data.get('comments')
            # new row
            else:
                if 'cbx' not in data:
                    detail = model.RevenueDetail()
                    detail.rev_id = revenue.id
                    detail.cust_id = data['cust_id']
                    detail.amt = data['amt']
                    detail.rcv_dt = data['rcv_dt']
                    detail.cre_dt = detail.mod_dt = datetime.now()
                    detail.comments = data.get('comments')
                    self.db.add(detail)
        self.db.commit()

        # update total
        total = Decimal('0.00')
        details = self.db.query(model.RevenueDetail).filter(model.RevenueDetail.rev_id == revenue.id).all()
        for detail in details:
            total += detail.amt
        revenue.total = total
        self.db.commit()

        # indicate update
        h.flash("Database updated.")
        redirect(url.current('view'))


    def report(self):
        c.customers = self.db.query(model.Customer).filter(model.Customer.status == True).order_by(model.Customer.cust_nm).all()
        return render('/revenues/report.mako')


    def results(self, rpt_type='bydate'):
        # start date
        c.start_dt = request.params['start_dt']
        if c.start_dt == '':
            c.start_dt = date.today().replace(day=1)
        else:
            c.start_dt = self._str2dt(c.start_dt)

        # end date
        c.end_dt = request.params['end_dt']
        if c.end_dt == '':
            c.end_dt = self._endofmonth()
        else:
            c.end_dt = self._str2dt(c.end_dt)

        # all customers or a specific customer
        c.cust_id = request.params['cust_id']

        # get results
        self._getresults()

        # display template
        return render('/revenues/results.mako')


    def _getresults(self):
        # pull revenues that match criteria
        qry = self.db.query(model.Revenue.id, model.Revenue.total, model.Revenue.dep_dt)
        qry = qry.join(model.RevenueDetail, model.RevenueDetail.rev_id == model.Revenue.id)
        qry = qry.filter(model.Revenue.dep_dt >= c.start_dt.strftime(self.FMT))
        qry = qry.filter(model.Revenue.dep_dt <= c.end_dt.strftime(self.FMT))
        if c.cust_id != 'all':
            qry = qry.filter(model.RevenueDetail.cust_id == c.cust_id)
        qry = qry.distinct()
        qry = qry.order_by(model.Revenue.dep_dt)
        revenues = qry.all()

        # move data to context
        c.revenues = []
        for revenue in revenues:
            rev = RowData()
            rev.id = revenue.id
            rev.total = revenue.total
            for col in ('id', 'total', 'dep_dt'):
                setattr(rev, col, getattr(revenue, col))

            # revenue details
            rev.details = []
            qry = self.db.query(model.RevenueDetail)
            qry = qry.filter(model.RevenueDetail.rev_id == rev.id)
            qry = qry.join(model.Customer, model.Customer.id == model.RevenueDetail.cust_id)
            qry = qry.add_column(model.Customer.cust_nm)
            qry = qry.add_column(model.RevenueDetail.amt)
            qry = qry.add_column(model.RevenueDetail.comments)
            qry = qry.order_by(model.RevenueDetail.id)
            details = qry.all()
            for detail in details:
                d = RowData()
                for col in ('cust_nm', 'amt', 'comments'):
                    setattr(d, col, getattr(detail, col))
                rev.details.append(d)
            c.revenues.append(rev)


    def delete(self):
        rev_id = request.params['rev_id']
        # delete detail rows
        for k,v in request.params.items():
            parts = k.split('.')
            if len(parts) == 3:
                if parts[0] == 'detail' and parts[2] == 'id':
                    detail = self.db.query(model.RevenueDetail).filter(model.RevenueDetail.rev_id == rev_id).first()
                    self.db.delete(detail)
        # delete parent row
        revenue = self.db.query(model.Revenue).filter(model.Revenue.id == rev_id).first()
        self.db.delete(revenue)
        # commit changes
        self.db.commit()

        # display template
        first_of_month = date.today().replace(day=1)
        day30 = first_of_month + timedelta(days=30)
        for field,days in {'start_dt':first_of_month,'end_dt':day30}.items():
            if getattr(c, field) == '':
                setattr(c, field, days)
            elif type(getattr(c, field)) is type(''):
                setattr(c, field, self._str2dt(getattr(c, field)))
        return render('/revenues/results.mako')


    def summary(self):
        c.rev_year = request.params['rev_year']

        qry = self.db.query(model.Customer)
        qry = qry.join(model.RevenueDetail, model.RevenueDetail.cust_id == model.Customer.id)
        qry = qry.filter(extract('year', model.RevenueDetail.rcv_dt) == c.rev_year)
        qry = qry.add_column(model.Customer.id)
        qry = qry.add_column(model.Customer.cust_nm.label('name'))
        qry = qry.add_column(model.Customer.status.label('status'))
        qry = qry.add_column(func.sum(model.RevenueDetail.amt).label('amount'))
        qry = qry.group_by(model.Customer.id)
        c.customers = qry.order_by(model.Customer.cust_nm).all()

        qry = self.db.query(func.sum(model.RevenueDetail.amt).label('total'))
        qry = qry.filter(extract('year', model.RevenueDetail.rcv_dt) == c.rev_year)
        c.revenue_total = qry.scalar()

        return render('/revenues/summary.mako')
