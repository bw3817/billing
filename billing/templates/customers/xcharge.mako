<%doc>
========================================
	Template: customers/xcharge.mako
	Author: Brian Wolf
	Date: 2009.01.03
========================================
</%doc>
<%inherit file="/customers/index.mako"/>

<%!
  from pylons import session
  from billing.lib.common.utils import Utils
  from decimal import Decimal
%>

<%
  utils = Utils()
  total = {'vol':Decimal('0.00'), 'amt':Decimal('0.00')}
  mo = session['mo']-1
  yr = session['yr']
  STYLES = {1:'', 0:'style="color: #AFB4C4;"'}
%>

##--------------------------------------------------------------------------------

<div class="colhdr"> <a href="/customers/prevmonth"><</a> ${utils.MONTHS[mo]} ${yr} <a href="/customers/nextmonth">></a></div>

<table style="border: 1px solid #aaa; width: 100%">
  <tr class="colhdr">
    <th>ID</th>
    <th>Customer</th>
    <th>Volume</th>
    <th>Amount</th>
  </tr>
  %for n,customer in enumerate(customers):
    <% if customer.status == 0 and customer.bonus is None: continue %>

  <tr style="background-color: ${utils.COLORS[n % 2]}">
    <td align="right">${customer.id}</td>
    <td><a href="/customers/view/${customer.id}" ${STYLES[customer.status] | n}>${customer.cust_nm}</a></td>
    %if customer.bonus is None:
    <td colspan="2" style="text-align: center"><a href="/customers/xcharge/add/${customer.id}">Add</a></td>
    %else:
    <td style="text-align: right">
      ${utils.fmt(customer.bonus.vol)}
      <%
        total['vol'] += customer.bonus.vol
        total['amt'] += customer.bonus.amt
      %>
    </td>
    <td style="text-align: right">
      <a href="/customers/xcharge/edit/${customer.bonus.id}">${utils.fmt(customer.bonus.amt)}</a>
    </td>
    %endif
  </tr>
  %endfor
  <tr class="total">
    <td colspan="2">${utils.MONTHS[mo]} ${yr}</td>
    <td style="text-align: right">${utils.fmt((total['vol']))}</td>
    <td class="total">${utils.fmt((total['amt']))}</td>
  </tr>
</table>
