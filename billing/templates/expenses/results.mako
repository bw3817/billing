<%doc>
========================================
    Template: expenses/results.mako
    Author: Brian Wolf
    Date: 2009.01.04
========================================
</%doc>
<%inherit file="/expenses/index.mako"/>

<%!
  import billing.lib.helpers as h
  from datetime import date, timedelta
  from decimal import Decimal
  from billing.lib.common.utils import Utils
%>

<%
  utils = Utils()
  HYPHEN = h.literal('&#8212;')
  total = Decimal('0.00')
  colors = ['odd','even']
%>

<%def name="morejs()">
<script type="text/javascript">
function Duplicate()
{
    var elements = document.getElementsByTagName("input");
    var selected = [];
    for (var j=0; j < elements.length; j++)
    {
        if (elements[j].type == "checkbox")
            if (elements[j].checked)
                selected.push(elements[j].id.substr(4));
    }

    //return if none was checked off
    if (selected.length == 0)
    {
        alert("Please select at least one row to duplicate.");
        return;
    }

    //Duplicate selected rows
    new Ajax.Request("/expenses/duplicate",
    {
        method: "get",
        parameters: {"cbx": selected.join(",")},
        onSuccess: function(results) {
            var json_data = results.responseText.evalJSON();
            window.location.reload(true);
        },
        onFailure: function() {alert("There was an error with the connection.");}
    });

}
</script>
</%def>

##--------------------------------------------------------------------------------

<div align="center" class="total">${c.start_dt_str} ${HYPHEN | n} ${c.end_dt_str}</div>
<div align="center" class="total">
    <input type="button" onclick="javascript:window.location='/expenses/report?start_dt=${c.start_dt}&end_dt=${c.end_dt}&cat_id=${c.cat_id}&vend_id=${c.vend_id}'" value="Back to Expense Report Configuration"/>
    <input type="button" onclick="Duplicate(); return false;" value="Duplicate"/>
    <input type="button" onclick="window.location.reload(true); return false;" value="Reload"/>
</div>
<table id="tbl_expenses" style="width: 100%">
    <thead>
      <tr class="colhdr">
        <th>ID</th>
        <th></th>
        <th>Vendor</th>
        <th>Method</th>
        <th>Check</th>
        <th>Paid Dt</th>
        <th>Month</th>
        <th>Amount</th>
        <th>Comments</th>
      </tr>
    </thead>

    <tbody id="tby_expenses">
    %for n,expense in enumerate(c.expenses):
      <% total += expense.amt %>
      <tr class="${colors[n % 2]}">
        <td><a href="/expenses/edit/${expense.id}">${expense.id}</td>
        <td style="text-align: center; width: 20px;"><input type="checkbox" id="cbx_${expense.id}" /></td>
        <td style="text-align: left; width: 200px;">${expense.vend_nm}</td>
        <td style="text-align: center; width: 55px;">${utils.PAYMENT_METHODS.get(expense.pay_mthd)}</td>
        <td style="text-align: center; width: 55px;">${expense.check_no}</td>
        <td style="text-align: center; width: 85px;">${expense.paid_dt}</td>
        <td style="text-align: center; width: 72px;">${utils.MONTHS[expense.mo-1]} ${expense.yr}</td>
        <td style="text-align: right">${expense.amt}</td>
        <td style="text-align: left; width: 250px;">${expense.comments}</td>
      </tr>
    %endfor
    </tbody>

    <tr class="total">
        <td colspan="7">&nbsp;</td>
        <td style="text-align: right;">${utils.fmt(total)}</td>
        <td>&nbsp;</td>
    </tr>
</table>

<div align="center">Rows returned: ${len(c.expenses)}</div>
