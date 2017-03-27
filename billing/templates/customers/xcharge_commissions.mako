<%doc>
========================================
	Template: customers/xcharge_bonus.mako
	Author: Brian Wolf
	Date: 2009.01.03
========================================
</%doc>
<%inherit file="/customers/index.mako"/>

<%!
  from pylons import session
  from decimal import Decimal
  from billing.lib.common.utils import Utils
%>

<%
  utils = Utils()

  mo = session['mo'] - 1
  yr = session['yr']
%>

##--------------------------------------------------------------------------------

<form method="post" action="/customers/bonus">
<input type="hidden" id="bonus_id" name="bonus_id" value="${bonus.id}"/>
<input type="hidden" id="cust_id" name="cust_id" value="${customer.id}"/>
<table>
  <tr>
    <td class="colhdr">Month:</td>
    <td>${utils.MONTHS[mo]}</td>
  </tr>
  <tr>
    <td class="colhdr">Year:</td>
    <td>${yr}</td>
  </tr>
  <tr>
    <td class="colhdr">Customer:</td>
    <td>${customer.cust_nm}</td>
  </tr>
  <tr>
    <td class="colhdr">Volume:</td>
    <td><input type="text" id="vol" name="vol" value="${bonus.vol}" class="lookup" style="width: 95px"/></td>
  </tr>
  <tr>
    <td class="colhdr">Amount:</td>
    <td><input type="text" id="amt" name="amt" value="${bonus.amt}" class="lookup" style="width: 55px"/></td>
  </tr>
  <tr>
    <td align="center" colspan="2"><input type="submit" value="Save"/></td>
  </tr>
</table>
</form>

<script type="text/javascript">
document.getElementById('vol').focus()
</script>