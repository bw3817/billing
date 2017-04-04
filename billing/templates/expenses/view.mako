<%doc>
========================================
    Template: expenses/view.mako
    Author: Brian Wolf
    Date: 2009.01.04
========================================
</%doc>
<%inherit file="/expenses/index.mako"/>

<%!
  from billing.lib.common.utils import Utils
%>

<%
  utils = Utils()

  def ShowSelected(value1,value2):
    if value1 is None or value2 is None:
      return ''
    elif value1 == value2:
      return 'selected'
    else:
      return ''
%>

##--------------------------------------------------------------------------------

<form id="frm_expense" method="post" action="/expenses/edit/${expense.id}">
<table>
    <tr>
        <td class="prompt">ID:</td>
        <td class="data">${expense.id}</td>
    </tr>
    <tr>
        <td class="prompt">Expense:</td>
        <td class="data">${expense.amt}</td>
    </tr>
    <tr>
        <td class="prompt">Vendor:</td>
        <td class="data">${expense.vend_nm}</td>
    </tr>
    <tr>
        <td class="prompt">Method of Payment:</td>
        <td class="data">${utils.PAYMENT_METHODS.get(expense.pay_mthd)}</td>
    </tr>
    <tr>
        <td class="prompt">Check Number:</td>
        <td class="data">${expense.check_no}</td>
    </tr>
    <tr>
        <td class="prompt">Paid Dt:</td>
        <td class="data">${expense.paid_dt}</td>
    </tr>
    <tr>
        <td class="prompt">Month:</td>
        <td class="data">${utils.MONTHS[expense.mo-1]} ${expense.yr}</td>
    </tr>
    <tr>
        <td class="prompt">Comments:</td>
        <td class="data">${expense.comments}</td>
    </tr>
    <tr>
        <td align="center" colspan="2"><input type="submit" class="button" value="Edit"/></td>
    </tr>
</table>
</form>
