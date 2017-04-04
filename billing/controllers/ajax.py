# controller: ajax
import simplejson as json
from pylons import config, url, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from billing.lib import app_globals
from billing.lib.baseplus import BasePlusController, render
from billing.lib.common.rowdata import RowData
from billing.lib.common.mvd import MerchantVolumeData
from billing.model import *
from sqlalchemy import or_
from datetime import datetime, date
from decimal import Decimal
from types import *


class AjaxController(BasePlusController):
    def vendors_per_category(self, cat_id):
        qry = self.db.query(Vendor)
        if cat_id != 'all':
            qry = qry.filter(Vendor.cat_id == cat_id)
        qry = qry.filter(Vendor.status == 1)
        qry = qry.order_by(Vendor.vend_nm)
        vendors = qry.all()
        vendorlist = []
        for vendor in vendors:
            vendorlist.append(self._stringify(RowData(vendor)))

        # send response to browser
        response.headers['Content-Type'] = 'application/json'
        return json.dumps(vendorlist)


    def getmvd(self):
        spreadsheet = request.params.get("spreadsheet")
        mvd = MerchantVolumeData(self.db)
        rtncode = mvd.read(spreadsheet)

        # send response to browser
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({'ok':rtncode})


    def _stringify(self, obj):
        if type(obj) is ListType:
            values = []
            for item in obj:
                values.append(self._stringify(item))
            return values

        values = {}
        for field in dir(obj):
            # skip these types
            if field == 'metadata': continue
            if field[:1] == '_': continue
            if type(getattr(obj, field)) is MethodType: continue

            # handle these types
            if self._hasParentClass(getattr(obj, field), 'Base'):
                values[field] = self._stringify(getattr(obj, field))
            elif type(getattr(obj, field)) is BooleanType:
                values[field] = int(getattr(obj, field))
            elif isinstance(getattr(obj, field), RowData):
                values[field] = self._stringify(getattr(obj, field))
            elif type(getattr(obj, field)) is ListType:
                values[field].append(self._stringify(getattr(obj, field)))
            elif type(getattr(obj, field)) in (type(datetime.today()), type(date.today())):
                values[field] = getattr(obj, field).strftime("%Y-%m-%d %H:%M:%S")
            elif type(getattr(obj, field)) is Decimal:
                values[field] = str(getattr(obj, field))
            else:
                values[field] = getattr(obj, field)
        return values


    def _hasParentClass(self, obj, classname):
        for cls in obj.__class__.__bases__:
            if cls.__name__ == classname:
                return True
        return False
