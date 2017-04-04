# controller: vendors
from pylons import config, url, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from billing.lib.baseplus import BasePlusController, render
import billing.model as model
import billing.lib.helpers as h
from billing.lib.common.rowdata import RowData
from datetime import datetime


class VendorsController(BasePlusController):
    def index(self):
        return render('/vendors/index.mako')


    def _getLetters(self):
        # get distinct first letter of customer names
        sql = """select distinct left(vend_nm,1) as letter
        from vendors
        order by left(vend_nm,1)
        """
        conn = self.db.connection()
        letters = conn.execute(sql).fetchall()
        return letters


    def find(self, letter=None):
        qry = self.db.query(model.Vendor)
        qry = qry.join((model.Category, model.Category.id == model.Vendor.cat_id))
        qry = qry.add_column(model.Category.cat_nm)
        # 2012.01.02 bw - filter on status (A=active, N=inactive)
        c.status = request.params.get('status')
        if c.status == 'A':
            qry = qry.filter(model.Vendor.status == True)
        elif c.status == 'N':
            qry = qry.filter(model.Vendor.status == False)
        vendorlist = qry.order_by(model.Vendor.vend_nm).all()
        vendors = []
        for vendor in vendorlist:
            v = RowData(vendor.Vendor)
            v.cat_nm = vendor.cat_nm
            vendors.append(v)
        return render('/vendors/find.mako', extra_vars={'vendors':vendors})


    def new(self):
        c.vendor = model.Vendor()
        c.categories = self.db.query(model.Category).order_by(model.Category.cat_nm).all()
        return render('/vendors/new.mako')


    def view(self, vend_id=None):
        if vend_id is None:
            vend_id = session['vend_id']
        else:
            session['vend_id'] = vend_id
            session.save()
        qry = self.db.query(model.Vendor)
        qry = qry.join((model.Category, model.Category.id == model.Vendor.cat_id))
        qry = qry.add_column(model.Category.cat_nm)
        qry = qry.filter(model.Vendor.id == vend_id)
        vendor = qry.first()
        if vendor:
            v = RowData(vendor.Vendor)
            v.cat_nm = vendor.cat_nm
        else:
            v = RowData(model.Vendor())
            v.cat_nm = None
        return render('/vendors/view.mako', extra_vars={'vendor':v})


    def edit(self, vend_id=None):
        session['vend_id'] = vend_id
        session.save()
        c.categories = self.db.query(model.Category).order_by(model.Category.cat_nm).all()
        c.vendor = self.db.query(model.Vendor).filter(model.Vendor.id == vend_id).first()
        if c.vendor is None:
            c.vendor = model.Vendor()
        return render('/vendors/new.mako')


    def save(self):
        if 'vend_nm' in request.params:
            if request.params.get('vend_id','') == '':
                vendor = model.Vendor()
                vendor.cre_dt = datetime.now()
                self.db.add(vendor)
            else:
                vendor = self.db.query(model.Vendor).filter(model.Vendor.id == request.params['vend_id']).first()
            vendor.vend_nm = request.params['vend_nm']
            vendor.cat_id = request.params['cat_id']
            vendor.status = int(request.params['status'])
            vendor.mod_dt = datetime.now()
            self.db.commit()
            session['vend_id'] = vendor.id
            session.save()
            h.flash("Database updated.")
            redirect(url.current('view'))
        else:
            h.flash("Missing required data.")
            redirect(url.current('find'))
