"""Project settings"""

#from pylons import config, url, request, response, session, tmpl_context as c
#from pylons.controllers.util import abort, redirect

from billing.lib.baseplus import BasePlusController, render
#import billing.model.meta as meta
import billing.model as model
import billing.lib.helpers as h
#from datetime import datetime
#from billing.lib.common.utils import Utils


class SettingsController(BasePlusController):
    def index(self):
        return render('/settings.mako')


    def setmonth(self):
        return render('/customers/setmonth.mako')


    def edit(self):
        category = self.db.query(model.Category).filter(model.Category.id == cat_id).first()
        if category is None:
            category = model.Category()
        return render('/categories/new.mako', extra_vars={'category':category})


    def save(self):
        if 'cat_nm' in request.params:
            if request.params.get('cat_id','') == '':
                category = model.Category()
                self.db.add(category)
            else:
                category = db.query(model.Category).filter(model.Category.id == request.params['cat_id']).first()
            category.cat_nm = request.params['cat_nm']
            self.db.commit()
            session['cat_id'] = category.id
            session.save()
            h.flash("Database updated.")
            redirect(url.current('view'))
        else:
            h.flash("Missing required data.")
            redirect(url.current(('find'))
