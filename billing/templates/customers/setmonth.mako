<%doc>
========================================
	Template: customers/setmonth.mako
	Author: Brian Wolf
	Date: 2009.01.03
========================================
</%doc>
<%inherit file="/customers/index.mako"/>

<%!
  from pylons import session
  from datetime import date
  from billing.lib.common.utils import Utils
%>

<%
  utils = Utils()

  def ShowSelected(value1, value2):
    if value1 is None or value2 is None:
      return ''
    elif value1 == value2:
      return 'selected'
    else:
      return ''
%>

##--------------------------------------------------------------------------------

<form method="post" action="/customers/setmonth">
<div align="center" style="padding: 10px">
Set Month:
<select name="mo">
%for mo in range(12):
  <option value="${mo+1}" ${ShowSelected(session.get('mo'),mo+1)}>${utils.MONTHS[mo]}</option>
%endfor
</select>

<select name="yr">
%for yr in range(2008,date.today().year+1):
  <option value="${yr}" ${ShowSelected(session.get('yr'),yr)}>${yr}</option>
%endfor
</select>

<input type="submit" value="Set" />
</div>
</form>
