<%doc>
========================================
    Template: customers/view.mako
    Author: Brian Wolf
    Date: 2009.12.31
========================================
</%doc>
<%inherit file="/customers/index.mako"/>

<%!
  from datetime import date
  from billing.lib.common.utils import Utils
%>

<%
  utils = Utils()
  MAPSTATUS = {True: 'Active', False:'Inactive'}
  customer_type_dict = {customer_type.cust_type: customer_type.dscr
                        for customer_type in customer_types}

  def ShowCustomerTypes(cust_types):
    if cust_types is None:
      return ''
    else:
      return ', '.join( [customer_type_dict.get(cust_type) for cust_type in cust_types] )
%>

##--------------------------------------------------------------------------------

<form id="frm_customer" method="post" action="/customers/edit/${customer.id}">

<table>
    <tr>
        <td class="prompt">ID:</td>
        <td class="data">${customer.id}</td>
    </tr>
    <tr>
        <td class="prompt">Customer:</td>
        <td class="data">${customer.cust_nm}</td>
    </tr>
    <tr>
        <td class="prompt">Type:</td>
        <td class="data">${ShowCustomerTypes(customer.cust_type)}</td>
    </tr>
    <tr>
        <td class="prompt">Processor:</td>
        <td class="data">${customer.processor}</td>
    </tr>
    <tr>
        <td class="prompt">Account ID:</td>
        <td class="data">${customer.account_id}</td>
    </tr>
    <tr>
        <td class="prompt">Rate:</td>
        <td class="data">${customer.rate}</td>
    </tr>
    <tr>
        <td class="prompt">Abbreviation:</td>
        <td class="data">${customer.abrv}</td>
    </tr>
    <tr>
        <td class="prompt">Status:</td>
        <td class="data">${MAPSTATUS[customer.status]}</td>
    </tr>
    <tr>
        <td align="center" colspan="2"><input type="submit" class="button" value="Edit"/></td>
    </tr>
</table>
</form>

%if 'X' in customer.cust_type:
<table style="margin-top: 20px;">
  <tr>
    <th class="colhdr" rowspan="2" style="vertical-align: top;">Year</td>
    <th class="colhdr" colspan="2">Volume</td>
    <th class="colhdr" colspan="2">Amount</td>
    <th class="colhdr" rowspan="2" style="vertical-align: top;">Count</td>
    <th class="colhdr" rowspan="2" style="vertical-align: top;">Ratio</td>
  </tr>
  <tr>
    <th class="colhdr">Total</td>
    <th class="colhdr">Mean</td>
    <th class="colhdr">Total</td>
    <th class="colhdr">Mean</td>
  </tr>

  %for bonus in bonuses:
  <tr>
    <td class="prompt">${bonus.yr}</td>
    <td class="data" style="text-align: right; padding: 5px;">${utils.fmt(bonus.sum_vol)}</td>
    <td class="data" style="text-align: right; padding: 5px;">${utils.fmt(bonus.avg_vol)}</td>
    <td class="data" style="text-align: right; padding: 5px;">${utils.fmt(bonus.sum_amt)}</td>
    <td class="data" style="text-align: right; padding: 5px;">${utils.fmt(bonus.avg_amt)}</td>
    <td class="data" style="text-align: center; padding: 5px;">
      %if bonus.cnt > 0:
        ${bonus.cnt}
      %endif
    </td>
    <td class="data" style="text-align: right; padding: 5px;">
      %if bonus.sum_amt is not None and bonus.sum_vol is not None and bonus.sum_vol > 0.00:
        ${utils.fmt(1000 * bonus.sum_amt / bonus.sum_vol)}
      %endif
    </td>
  </tr>
  %endfor

<table>
%endif
