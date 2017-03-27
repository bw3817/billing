# controller: invoices
# built-ins
import os
import simplejson as json
from datetime import datetime, timedelta

# sqlalchemy
#from sqlalchemy import or_, and_, not_, func
#from sqlalchemy import inspect

# pylons
from pylons import config, url, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from billing.lib.baseplus import BasePlusController, render
import billing.model as model

# form handling
from formencode import Schema, validators, FancyValidator, Invalid
from pylons.decorators import validate
from pylons.decorators.rest import restrict

# application-specific
from geninvoice import GenInvoice


class HoursOrExpense(FancyValidator):
    messages = dict(
        invalid="Specify hours or expense, but not both",
        missing="Specify hours or expense",
    )

    def validate_python(self, fields, state):
        if fields['hrs'] and fields['amt_exp']:
            msg = self.message('invalid', state)
            raise Invalid(msg, fields, state,
                error_dict=dict(hrs=msg))

        elif not fields['hrs'] and not fields['amt_exp']:
            msg = self.message('missing', state)
            raise Invalid(msg, fields, state,
                error_dict=dict(hrs=msg))


class HoursData(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    iso_date_pattern = """^([0-9]{4})(?:(1[0-2]|0[1-9])|-?(1[0-2]|0[1-9])-?)(3[0-1]|0[1-9]|[1-2][0-9])$"""
    hours_id = validators.String(not_empty=True, strip=True, messages={"empty":"Missing hours ID."})
    customer_id = validators.Int(not_empty=True, strip=True, messages={"empty":"Please select a customer."})
    project_id = validators.Int(not_empty=True, strip=True, messages={"empty":"Please select a project."})
    performed = validators.Regex(regex=iso_date_pattern, not_empty=True, strip=True, messages={"empty":"Please enter a date."})
    hrs = validators.Number(not_empty=False, strip=True)
    amt_exp = validators.Number(not_empty=False, strip=True)
    chained_validators = [HoursOrExpense()]


class HrsReportData(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    iso_date_pattern = """^([0-9]{4})(?:(1[0-2]|0[1-9])|-?(1[0-2]|0[1-9])-?)(3[0-1]|0[1-9]|[1-2][0-9])$"""
    customer_id = validators.Int(not_empty=True, strip=True, messages={"missing":"Please select a custgomer."})
    project_id = validators.Int(not_empty=True, strip=True, messages={"missing":"Please select a project."})
    from_dt = validators.Regex(regex=iso_date_pattern, not_empty=True, strip=True, messages={"missing":"Please enter a 'from' date."})
    to_dt = validators.Regex(regex=iso_date_pattern, not_empty=True, strip=True, messages={"missing":"Please enter a 'to' date."})


class DataDict(dict):
    def __missing__(self, key):
        self[key] = r = {}
        return r


class InvoicesController(BasePlusController):
    def index(self):
        extra_vars = {}
        return render('/invoices/invoices.mako', extra_vars=extra_vars)


    def projects_manage(self):
        extra_vars = self._get_data()
        return render('/invoices/projects_manage.mako', extra_vars=extra_vars)


    def projects_add(self):
        extra_vars = self._get_data()
        return render('/invoices/projects_add.mako', extra_vars=extra_vars)


    @restrict('POST')
    def projects_add_save(self):
        project = model.Project()
        project.cust_id = request.POST['customer_id']
        project.name = request.POST['project']
        project.cre_dt = datetime.now()
        self.db.add(project)
        self.db.commit()
        redirect(url('/projects/manage'))


    @restrict('POST')
    def projects_manage_save(self):
        cust_id = request.POST['customer_id']
        qry = self.db.query(model.Project)
        qry = qry.filter(model.Project.cust_id == cust_id)
        projects = qry.all()
        for project in projects:
            project.status = ('project.{0}'.format(project.id) in request.POST)
        self.db.commit()
        redirect(url('/projects/manage'))


    def projects_find(self):
        customer_id = request.GET['customer_id']
        qry = self.db.query(model.Project)
        qry = qry.filter(model.Project.cust_id == customer_id)
        qry = qry.filter(model.Project.status == True)
        qry = qry.order_by(model.Project.name)
        rows = qry.all()
        projects = [dict(id=row.id, name=row.name) for row in rows]
        projects.insert(0, dict(id='all', name='All projects'))
        info = dict(status=1, rate=141.00, projects=projects, project_count=len(projects))

        # send response to browser
        response.headers['Content-Type'] = 'application/json'
        return json.dumps(info)


    def invoice_generate(self):
        # customer
        customer_id = request.GET['customer_id']
        customer = self.db.query(model.Customer).filter(model.Customer.id == customer_id).first()

        # hours
        hrs_id_list = request.GET.getall('hrs')
        qry = self.db.query(model.Hours)
        qry = qry.join(model.Project, model.Project.id == model.Hours.project_id)
        qry = qry.filter(model.Hours.id.in_(hrs_id_list))
        qry = qry.add_column(model.Project.name.label('project_name'))
        qry = qry.add_column(model.Hours.hrs)
        qry = qry.add_column(model.Hours.amt_exp)
        qry = qry.add_column(model.Hours.performed)
        qry = qry.add_column(model.Hours.comments)
        qry = qry.order_by(model.Hours.performed, model.Hours.id)
        hours = qry.all()

        # maximum, discount
        maximum = request.GET.get('maximum')
        discount = request.GET.get('discount')

        # generate invoice
        g = GenInvoice(customer, hours, maximum=maximum, discount=discount)
        fullpath = g.make()
        path,filename = os.path.split(fullpath)
        fn,ext = os.path.splitext(filename)
        info = dict(status=1, invoice=fn)

        # send response to browser
        response.headers['Content-Type'] = 'application/json'
        return json.dumps(info)


    def hours_add(self):
        extra_vars = self._get_data()
        extra_vars.update(hours_id='NEW')
        return render('/invoices/hours_add.mako', extra_vars=extra_vars)


    def hours_show(self):
        extra_vars = self._get_data()
        settings_list = self.db.query(model.Setting).all()
        settings = {setting.field: setting.value for setting in settings_list}
        extra_vars.update(settings=settings)
        return render('/invoices/hours_show.mako', extra_vars=extra_vars)


    def hours_find(self):
        # parameters
        customer_id = request.params.get('customer_id')
        project_id = request.params.get('project_id')
        from_dt = request.params.get('from_dt')
        to_dt = request.params.get('to_dt')
        status_list = [billing_status[0].upper()
                       for billing_status in ('unbilled', 'billed', 'paid')
                       if request.params.get(billing_status, 'false') == 'true'
        ]

        # save parameters
        settings = self.db.query(model.Setting).all()
        for setting in settings:
            for field in ('customer_id','project_id','from_dt','to_dt'):
                if field in request.params:
                    if setting.field == field:
                        setattr(setting, 'value', request.params[field])
        self.db.commit()

        # get hours
        if all((customer_id, project_id, from_dt, to_dt)):
            # get report data
            qry = self.db.query(model.Hours)
            qry = qry.join(model.Customer, model.Customer.id == model.Hours.cust_id)
            qry = qry.join(model.Project, model.Project.id == model.Hours.project_id)
            qry = qry.filter(model.Hours.cust_id == customer_id)
            if project_id != 'all':
                qry = qry.filter(model.Hours.project_id == project_id)
            qry = qry.filter(model.Hours.performed >= datetime.strptime(from_dt, '%Y-%m-%d'))
            qry = qry.filter(model.Hours.performed <  datetime.strptime(to_dt, '%Y-%m-%d') + timedelta(days=1))
            qry = qry.filter(model.Hours.billing_status.in_(status_list))
            qry = qry.add_column(model.Customer.rate)
            qry = qry.add_column(model.Customer.cust_nm.label('customer'))
            qry = qry.add_column(model.Project.name.label('project'))
            qry = qry.add_column(model.Hours.id.label('id'))
            qry = qry.add_column(model.Hours.cust_id)
            qry = qry.add_column(model.Hours.project_id)
            qry = qry.add_column(model.Hours.performed)
            qry = qry.add_column(model.Hours.billing_status)
            qry = qry.add_column(model.Hours.hrs)
            qry = qry.add_column(model.Hours.amt_exp)
            qry = qry.order_by(model.Hours.performed, model.Hours.id)
            rows = qry.all()

            hours = [dict(id=row.id,
                          cust_id=row.cust_id,
                          customer=row.customer,
                          rate=row.rate,
                          project_id=row.project_id,
                          project=row.project,
                          performed=row.performed.isoformat(),
                          billing_status=row.billing_status,
                          hrs=row.hrs,
                          amt_exp=row.amt_exp,
                         )
                     for row in rows
                    ]
            info = dict(status=1, hours=hours, hours_count=len(hours))
        else:
            info = dict(status=0, hours=[], hours_count=0)

        # send response to browser
        response.headers['Content-Type'] = 'application/json'
        return json.dumps(info)


    def hours_update(self):
        for k,v in request.GET.items():
            if k.startswith('hrs.'):
                hours = self.db.query(model.Hours).filter(model.Hours.id == k[len('hrs.'):]).first()
                hours.hrs = v
            elif k.startswith('amt_exp.'):
                #amt_exp = self.db.query(model.Hours).filter(model.Hours.id == k[len('amt_exp.'):]).first()
                hours.amt_exp = v
        self.db.commit()
        rowcnt = len(request.GET.keys())
        info = dict(rowcnt=rowcnt, msg="Hours updated.")

        # send response to browser
        response.headers['Content-Type'] = 'application/json'
        return json.dumps(info)


    def setbilled(self):
        hrs_id_list = request.GET.getall('hrs')
        hours = self.db.query(model.Hours).filter(model.Hours.id.in_(hrs_id_list)).all()
        for hour in hours:
            #hour.billed = True
            hour.billing_status = 'B'
        self.db.commit()
        info = dict(status=1, msg="Selected hours set as billed.")

        # send response to browser
        response.headers['Content-Type'] = 'application/json'
        return json.dumps(info)


    def setpaid(self):
        hrs_id_list = request.GET.getall('hrs')
        hours = self.db.query(model.Hours).filter(model.Hours.id.in_(hrs_id_list)).all()
        for hour in hours:
            #hour.paid = True
            hour.billing_status = 'P'
        self.db.commit()
        info = dict(status=1, msg="Selected hours set as paid.")

        # send response to browser
        response.headers['Content-Type'] = 'application/json'
        return json.dumps(info)


    def _get_data(self):
        # customers
        qry = self.db.query(model.Customer)
        qry = qry.filter(model.Customer.status == True)
        qry = qry.filter(model.Customer.cust_type.like('%A%'))
        qry = qry.filter(model.Customer.cust_nm != 'Unknown')
        qry = qry.order_by(model.Customer.cust_nm)
        customers = qry.all()
        extra_vars = dict(customers=customers)

        # projects
        projectlist = self.db.query(model.Project).filter(model.Project.status == True).all()
        projects = DataDict()
        for project in projectlist:
            projects[project.cust_id][project.id] = project.name
        extra_vars.update(projects=projects)

        # settings
        settingslist = self.db.query(model.Setting).all()
        settings = {setting.field: setting.value for setting in settingslist}
        extra_vars.update(last_cust_id=int(settings['customer_id']))
        try:
            project_id = int(settings['project_id'])
        except ValueError,e:
            project_id = 'all'
        extra_vars.update(last_project_id=project_id)

        # most recent customer
        extra_vars.update(
            customer=self.db.query(model.Customer).filter(id==extra_vars['last_cust_id']).first()
        )
        return extra_vars


    @restrict('POST')
    @validate(schema=HoursData(), form='hours_add', post_only=False, on_get=True)
    def hours_save(self):
        # function to strip white space from input fields and
        # return None if empty
        f = lambda s: s.strip() if (s or '').strip() else None

        # fields from input form
        hours_id = f(request.POST.get('hours_id'))
        customer_id = f(request.POST.get('customer_id'))
        project_id = f(request.POST.get('project_id'))
        performed = f(request.POST.get('performed'))
        hrs = f(request.POST.get('hrs'))
        amt_exp = f(request.POST.get('amt_exp'))
        comments = f(request.POST.get('comments'))

        #
        #inspect(MyTable).c.id

        if hours_id == 'NEW':
            # add hours
            hours = model.Hours()
            hours.cust_id = customer_id
            hours.project_id = project_id
            hours.performed = datetime.strptime(performed, '%Y-%m-%d')
            hours.cre_dt = datetime.now()
            hours.mod_dt = datetime.now()
            hours.hrs = hrs
            hours.amt_exp = amt_exp
            hours.comments = comments
            self.db.add(hours)
            self.db.commit()

            # save parameters
            for field in ('customer_id','project_id'):
                setting = self.db.query(model.Setting).filter(model.Setting.field == field).first()
                if setting:
                    value = request.POST[field]
                    if field.endswith('_dt'):
                        setting.value = datetime.strptime(value, '%Y-%m-%d')
                    else:
                        setting.value = value
                self.db.commit()

            redirect(url('/hours/show'))
