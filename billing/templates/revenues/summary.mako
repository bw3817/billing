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
%>

##--------------------------------------------------------------------------------

<legend>Revenue Summary for ${c.rev_year}</legend>

<table style="border: 1px solid #aaa; width: 100%">
  <tr class="colhdr">
    <th>Customer</th>
    <th>Amount</th>
  </tr>
  %for n,customer in enumerate(c.customers):
  <tr style="background-color: ${utils.COLORS[n % 2]}">
    <td>${customer.name}</td>
    <td>${customer.amount}</td>
  </tr>
  %endfor
</table>
