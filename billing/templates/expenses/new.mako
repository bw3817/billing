<%doc>
========================================
    Template: expenses/new.mako
    Author: Brian Wolf
    Date: 2009.01.04
========================================
</%doc>
<%inherit file="/expenses/index.mako"/>

<%!
  from datetime import date, timedelta
  from collections import OrderedDict
  from billing.lib.common.utils import Utils
%>

<% utils = Utils() %>

<%def name="morecss()">
<link type="text/css" href="${url('/css/dateselector.css')}" rel="stylesheet"/>
</%def>

<%def name="morejs()">
<script type="text/javascript" src="${url('/js/dateselector.js')}"></script>
</%def>

<%
  if c.expense.id is None:
    c.expense.yr = date.today().year
    c.expense.mo = date.today().month
  exp_dt = '%s-%s' % (c.expense.yr,('00'+str(c.expense.mo))[-2:])

  def ShowSelected(value1, value2):
    if value1 is None or value2 is None:
      return ''
    elif value1 == value2:
      return 'selected'
    else:
      return ''
%>

##--------------------------------------------------------------------------------

<form id="frm_expense" method="post" action="/expenses/save">
<input type="hidden" name="exp_id" value="${c.expense.id}"/>
<table>
    %if c.expense.id is not None:
    <tr>
        <td class="prompt">ID:</td>
        <td class="data">${c.expense.id}</td>
    </tr>
    %endif
    <tr>
        <td class="prompt">Vendor:</td>
        <td>
          <select id="vend_id" name="vend_id" class="lookup" style="width: 320px">
            <option value="">Select...</option>
            %for vendor in c.vendors:
              <option value="${vendor.id}" ${ShowSelected(c.expense.vend_id,vendor.id)}>${vendor.vend_nm}::${vendor.cat_nm}</option>
            %endfor
          </select>
        </td>
    </tr>
    <tr>
        <td class="prompt">Method of Payment:</td>
        <td>
          <select id="pay_mthd" name="pay_mthd" class="lookup" onchange="SetCheckNumber(this)">
            <option value="">Select...</option>
            %for k,v in OrderedDict(sorted(utils.PAYMENT_METHODS.items(),key=lambda m: m[1])).items():
              <option value="${k}" ${ShowSelected(c.expense.pay_mthd,k)}>${v}</option>
            %endfor
          </select>
        </td>
    </tr>
    <tr>
        <td class="prompt">Paid Dt:</td>
        <td>
          <input type="text" id="paid_dt" name="paid_dt" value="${c.expense.paid_dt}" style="text-align: center; width: 90px;"/>
          <a href="#" onclick="displayDatePicker('paid_dt');"><img src="${url('/images/cal.gif')}" width="16" height="16" border="0" alt="Pick a date"></a>
        </td>
    </tr>
    <tr>
        <td class="prompt">Month:</td>
        <td>
          <input type="text" id="dt" name="dt" value="${exp_dt}" style="text-align: center; width: 90px;"/>
          <a href="#" onclick="displayDatePicker('dt');"><img src="${url('/images/cal.gif')}" width="16" height="16" border="0" alt="Pick a date"></a>
        </td>
    </tr>
    <tr>
        <td class="prompt">Amount:</td>
        <td>
          <input type="text" id="amt" name="amt" value="${c.expense.amt}" style="width: 70px;"/>
        </td>
    </tr>
    <tr>
        <td class="prompt">Check Number:</td>
        <td class="data">
          <input type="text" id="check_no" name="check_no" value="${c.expense.check_no}" style="width: 70px;" disabled="disabled"/>
        </td>
    </tr>
    <tr>
        <td class="prompt">Comments:</td>
        <td><textarea id="comments" name="comments" class="comments">${c.expense.comments}</textarea></td>
    </tr>
    <tr>
        <td align="center" colspan="2">
          <input type="submit" class="button" value="Save"/>
          %if c.expense.id is not None:
            <input type="submit" class="button" value="Delete" onclick="document.getElementById('frm_expense').action='/expenses/delete';"/>
          %endif
        </td>
    </tr>
</table>
</form>

<script type="text/javascript">
document.getElementById('amt').focus();

function SetCheckNumber(obj)
{

    var check_no = document.getElementById('check_no');
    check_no.disabled = (obj.value != 'chk');
}

</script>
