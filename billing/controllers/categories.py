# controller: categories
from pylons import config, url, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from billing.lib.baseplus import BasePlusController, render
import billing.model as model
import billing.lib.helpers as h
from datetime import datetime
from billing.lib.common.utils import Utils

# database modules
from sqlalchemy import or_, and_
from sqlalchemy.sql.functions import coalesce, concat
from sqlalchemy.sql.expression import distinct


class CategoriesController(BasePlusController):
    def index(self):
        return render('/categories/index.mako')

    def find(self):
        categories = self.db.query(model.Category).order_by(model.Category.cat_nm).filter(model.Customer.status == True).all()
        return render('/categories/categories.mako', extra_vars={'categories':categories})

    def new(self):
        category = model.Category()
        return render('/categories/new.mako', extra_vars={'category':category})

    def view(self, cat_id=None):
        if cat_id is None:
            cat_id = session['cat_id']
        else:
            session['cat_id'] = cat_id
            session.save()
        category = self.db.query(model.Category).filter(model.Category.id == cat_id).first()
        if category is None:
            category = model.Category()
        return render('/categories/view.mako', extra_vars={'category':category})

    def edit(self, cat_id=None):
        session['cat_id'] = cat_id
        session.save()
        category = self.db.query(model.Category).filter(model.Category.id == cat_id).first()
        if category is None:
            category = model.Category()
        return render('/categories/new.mako', extra_vars={'category':category})

    def save(self):
        if 'cat_nm' in request.params:
            if request.params.get('cat_id','') == '':
                category = model.Category()
                category.cre_dt = datetime.now()
            else:
                category = self.db.query(model.Category).filter(model.Category.id == request.params['cat_id']).first()
            category.cat_nm = request.params['cat_nm']
            self.db.add(category)
            self.db.commit()
            session['cat_id'] = category.id
            session.save()
            h.flash("Database updated.")
            redirect(url.current('view'))
        else:
            h.flash("Missing required data.")
            redirect(url.current('find'))
