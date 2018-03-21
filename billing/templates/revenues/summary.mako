<%doc>
========================================
    Template: revenues/summary.mako
    Author: Brian Wolf
    Date: 2018.01.30
========================================
</%doc>
<%inherit file="/revenues/index.mako"/>

<%!
  from billing.lib.common.utils import Utils
%>

<%
  utils = Utils()
  def checkmark(status):
    return h.literal('&#x2713;') if status else ''
%>

##--------------------------------------------------------------------------------

<legend>Revenue Summary for ${c.rev_year}</legend>

<table style="border: 1px solid #aaa; width: 100%">
  <tr class="colhdr">
    <th>Customer</th>
    <th>Active</th>
    <th>Amount</th>
  </tr>
  %for n,customer in enumerate(c.customers):
  <tr style="background-color: ${utils.COLORS[n % 2]}">
    <td>${customer.name}</td>
    <td align="center">${checkmark(customer.status)}</td>
    <td>${customer.amount}</td>
  </tr>
  %endfor
  <tr class="colhdr">
    <td colspan="2">Total</td>
    <td>${c.revenue_total}</td>
  </tr>
</table>
