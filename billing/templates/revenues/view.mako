<%doc>
========================================
    Template: revenues/view.mako
    Author: Brian Wolf
    Date: 2009.01.05
========================================
</%doc>
<%inherit file="/revenues/index.mako"/>
<%! from billing.lib.common.utils import Utils %>

<%
  utils = Utils()

  def ShowDate(dt):
    if dt is None:
      return ''
    else:
      return dt.strftime('%Y-%m-%d')
%>

##--------------------------------------------------------------------------------

<form id="frm_revenue" method="post" action="/revenues/edit/${c.revenue.id}">
<table>
    <tr>
        <td class="prompt">ID:</td>
        <td class="data">${c.revenue.id}</td>
    </tr>
    <tr>
        <td class="prompt">Total:</td>
        <td class="data">$${c.revenue.total}</td>
    </tr>
    <tr>
        <td class="prompt">Deposited:</td>
        <td class="data">${ShowDate(c.revenue.dep_dt)}</td>
    </tr>
</table>

<table cellpadding="5px">
    <tr class="colhdr">
        <th>ID</th>
        <th>Customer</th>
        <th>Amount</th>
        <th>Received</th>
        <th>Comments</th>
    </tr>
    %for d,detail in enumerate(c.revenue.details):
      <tr style="background-color: ${utils.COLORS[d % 2]};">
        <td>${detail.id}</td>
        <td>${detail.cust_nm}</td>
        <td align="right">${detail.amt}</td>
        <td align="center" style="width: 80px;">${detail.rcv_dt}</td>
        <td>${detail.comments}</td>
      </tr>
    %endfor
</table>

<div align="center">
    <input type="submit" class="button" value="Edit"/>
</div>
</form>
