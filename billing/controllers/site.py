# controller: site

# built-ins
from datetime import datetime, date

# pylons
from pylons import config, url, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

# application
import billing.lib.helpers as h
from billing.lib import app_globals
from billing.lib.baseplus import BasePlusController, render

# model
import billing.model as model


class SiteController(BasePlusController):
    def index(self):
        redirect(url.current('home'))


    def home(self):
        return render('/home.mako')


    def info(self):
        return render('/siteinfo.mako')


    def login(self):
        return render('/login.mako')


    def loginsubmit(self):
        btn = request.params.get('btn','?')
        if btn == 'login':
            if 'usrnam' in request.params and 'pwd' in request.params:
                session['usrnam'] = request.params['usrnam']
                qry = self.db.query(model.User)
                qry = qry.filter(model.User.usrnam == request.params['usrnam'])
                qry = qry.filter(model.User.pwd == request.params['pwd'])
                user = qry.first()
                if user is None:
                    h.flash("Incorrect login credentials.")
                    redirect(url.current('login'))
                elif not user.status:
                    h.flash("Account has been disabled.")
                    redirect(url.current('login'))
                else:
                    c.user = user
                    session['user_id'] = user.id
                    session['login_dt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    settings = self.db.query(model.Setting).all()
                    for setting in settings:
                        if setting.field == 'yr':
                            setting.value = session['yr'] = date.today().year
                        elif setting.field == 'mo':
                            setting.value = session['mo'] = date.today().month
                    self.db.commit()
                    session.save()
                    if 'requested_url' in session:
                        redirect(url(str(session['requested_url'])))
                    else:
                        redirect(url.current('home'))
            else:
                h.flash("Incomplete login credentials.")
                redirect(url('/site/login'))


    def logoff(self):
        settings = self.db.query(model.Setting).filter(model.Setting.field.in_(('mo','yr'))).all()
        for setting in settings:
            for field in ('yr','mo'):
                if setting.field == field:
                    setting.value = session.get(field)
        self.db.commit()
        session.clear()
        session.save()
        h.flash("You have been logged off.")
        redirect(url('/site/login'))


    def error(self):
        return render('/error.mako')
