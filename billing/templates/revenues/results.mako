<%doc>
========================================
    Template: revenues/results.mako
    Author: Brian Wolf
    Date: 2009.01.05
========================================
</%doc>
<%inherit file="/revenues/index.mako"/>

<%!
  import billing.lib.helpers as h
  from decimal import Decimal
  from datetime import datetime
  from billing.lib.common.utils import Utils
%>
<%
  utils = Utils()
  HYPHEN = h.literal('&#8212;')
  grand_total = Decimal('0.00')
  sub_total = Decimal('0.00')
%>


##--------------------------------------------------------------------------------

<div align="center">${c.start_dt.strftime("%b %d, %Y")} ${HYPHEN | n} ${c.end_dt.strftime("%b %d, %Y")}</div>
<table style="width: 99%;">
    <tr class="colhdr">
        <th>ID</th>
        <th>Customer</th>
        <th>Item</th>
        <th>Amount</th>
        <th>Deposited</th>
        <th>Comments</th>
    </tr>
    %for r,revenue in enumerate(c.revenues):
      %for d,detail in enumerate(revenue.details):
        <%
           grand_total += detail.amt
           sub_total += detail.amt
        %>
        <tr style="background-color: ${utils.COLORS[r % 2]}">
          %if d == 0:
            <td style="padding: 5px; vertical-align: top;" rowspan="${len(revenue.details)}">
              <a href="/revenues/edit/${revenue.id}">${revenue.id}</a>
            </td>
          %endif
          <td style="padding: 5px; width: 200px; vertical-align: top;">${detail.cust_nm}</td>
          <td style="padding: 5px; text-align: right; vertical-align: top;">${utils.fmt(detail.amt)}</td>
          %if d == 0:
            <td style="padding: 5px; text-align: right; vertical-align: top;" rowspan="${len(revenue.details)}">${utils.fmt(revenue.total)}</td>
            <td style="width: 115px; padding: 5px; text-align: center; vertical-align: top;" rowspan="${len(revenue.details)}">${revenue.dep_dt.strftime('%m/%d/%Y')}</td>
          %endif
          <td style="padding: 5px; vertical-align: top; width: 200px;">${detail.comments}</td>
        </tr>
      %endfor
    %endfor

    <tr class="total">
      <td colspan="2" style="text-align: right;">Total:</td>
      <td style="text-align: right;">${utils.fmt(sub_total)}</td>
      <td style="text-align: right;">${utils.fmt(grand_total)}</td>
      <td colspan="4">&nbsp;</td>
    </tr>
</table>

<div align="center">Rows returned: ${len(c.revenues)}</div>
