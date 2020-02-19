<%doc>
========================================
    Template: expenses/eoy.mako
    Author: Brian Wolf
    Date: 2012.04.04
========================================
</%doc>
<%inherit file="/expenses/index.mako"/>

<%!
  from datetime import date
  from decimal import Decimal
  from billing.lib.common.utils import Utils
  utils = Utils()
%>

<%
  category = None
  subtotal = Decimal('0.00')
  total = Decimal('0.00')

  def ShowSelect(id1, id2):
    if str(id1 or "") == str(id2 or ""):
      return 'selected'
    else:
      return ''
%>

<%def name="morecss()">
<link type="text/css" href="${url('/css/dateselector.css')}" rel="stylesheet" />
<style>
.button {
  background-color: #EEE;
  border-radius: 2px;
  color: #AA0000;
  padding: .3em;
  text-decoration: none;
  cursor: pointer;
}

.button:focus,
.button:hover {
  background-color: #AA0000;
  color: #FFF;
}

.content {
  display: none;
  margin: 1em 0;
}

.content.active,
.no-js .content {
  display: block;
}
</style>
</%def>

<%def name="morejs()">
<script type="text/javascript">
document.onreadystatechange = function () {
    var content = [];
    var row;

  <%
    category = None
    subtotal = Decimal('0.00')
  %>

    %for n, row in enumerate(c.rows):
      row = [];

      %if row.cat_nm == category:
        <% subtotal += row.sum_amt %>
        row = ['""', '"${row.vend_nm}"', '"${row.sum_amt}"', '"${subtotal}"'];
      %else:
        <%
           category = row.cat_nm
           subtotal = row.sum_amt
        %>
        row = ['"${row.cat_nm}"', '"${row.vend_nm}"', '"${row.sum_amt}"', '"${subtotal}"'];
      %endif

      row.push('\r\n');
      content.push(row);

    %endfor

    if (document.readyState == 'interactive') {
        var element = document.getElementById('id_download');
        element.addEventListener('click', function(event) {
            var blob = new Blob(content, {type: 'text/csv, encoding=utf8'});
            element.download = GetFormattedTime() + '.csv';
            element.href = window.URL.createObjectURL(blob);
            element.dataset.downloadurl = ['text/csv', element.download, element.href].join(':');
        });
    }

    function GetFormattedTime() {
        var today = new Date();
        var yr = today.getFullYear();
        var mo = today.getMonth() + 1;
        var day = today.getDate();
        return yr + '-' + mo.toString().padStart(2, '0') + '-' + day.toString().padStart(2, '0');
    }
}
</script>
</%def>

##--------------------------------------------------------------------------------

<div style="border: 1px solid #aaa; width: 500px; padding: 10px;">
  <div style="font-weight: bold;">
    Expense Report By Category
    <a id="id_download" class="button" download>Download</a>
  </div>
  <table style="width: 100%" cellspacing="5px">
    <tr style="background-color: #e0e0e0">
      <th>Category</th>
      <th>Vendor</th>
      <th>Amount</th>
      <th>Subtotal</th>
    </tr>

    %for n, row in enumerate(c.rows):

      %if row.cat_nm == category:
        <% subtotal += row.sum_amt %>
        <tr style="background-color: ${utils.COLORS[n % 2]}">
          <td>&nbsp;</td>
          <td>${row.vend_nm}</td>
          <td align="right">${row.sum_amt}</td>
          <td align="right">${subtotal}</td>
        </tr>

      %else:
        <%
           category = row.cat_nm
           subtotal = row.sum_amt
        %>
        <tr style="background-color: ${utils.COLORS[n % 2]}">
          <td>${row.cat_nm}</td>
          <td>${row.vend_nm}</td>
          <td align="right">${row.sum_amt}</td>
          <td align="right">${subtotal}</td>
        </tr>
      %endif

      <% total += row.sum_amt %>

    %endfor

    <% n = 0 %>

    <tr style="background-color: ${utils.COLORS[n % 2]}">
      <td colspan="3">&nbsp;</td>
      <td align="right">${total}</td>
    </tr>

  </table>
</div>
