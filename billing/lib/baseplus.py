#----------------------------------------------------------------------
# Author:            Brian Wolf
# Date:            2009.11.11
# Module:            BasePlusController.py
# Description:        Extends BaseController
#
# Modifications:
#
#
#----------------------------------------------------------------------


from pylons import config, url, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from billing.lib.base import BaseController, render
import billing.model.meta as meta
import billing.model as model
from datetime import datetime, date, timedelta
from types import *


class BasePlusController(BaseController):
    def __init__(self):
        self.db = meta.Session()
        c.user = self.db.query(model.User).filter(model.User.id == session.get('user_id')).first()
        if c.user is not None:
            c.user.full_name = self._concat(c.user.salutation, c.user.first_name, c.user.middle_name, c.user.last_name)

    def __before__(self):
        # do not process URLs related to the login process
        if  request.environ.get('PATH_INFO') in ('/site/login','/site/loginsubmit','/site/logoff','/error/document'):
            return

        if 'user_id' not in session and 'login_dt' not in session:
            session['requested_url'] = self._current_url()
            session.save()
            redirect(url('/site/login'))

    def _current_url(self):
        # temporary kludge until pylons.url.current() stabilizes and returns the query string.
        if request.query_string:
            return "%s?%s" % (request.path_info, request.query_string)
        else:
            return request.path_info

    def _coalesce(self, s):
        if s in (None,''):
            return ''
        else:
            return s.strip()

    def _getUser(self, user_id):
        user = self.db.query(model.User).filter(model.User.user_id == user_id).first()
        user.full_name = self._concat(c.customer.salutation, c.customer.first_name, c.customer.middle_name, c.customer.last_name)
        return user

    def _concat(self, *args):
        s_list = []
        for s in args:
            if s is not None:
                s_list.append(s.strip())
        s = ' '.join(s_list)
        return s.strip()

    def _str2dt(self, s):
        date_parts = s.split('-')
        return date(int(date_parts[0]),int(date_parts[1]),int(date_parts[2]))

    def _endofmonth(self, dt=None):
        if dt is None:
            dt = date.today()
        if type(dt) in (StringType, UnicodeType):
            dt = self._str2dt(dt)
        # look for end of month
        if dt.day == 1:
            dt += timedelta(1)
        while dt.day != 1:
            dt += timedelta(1)
        dt -= timedelta(1)
        return dt
