<%doc>
========================================
  Template: revenues/new.mako
  Author: Brian Wolf
  Date: 2009.01.05
========================================
</%doc>
<%inherit file="/revenues/index.mako"/>
<%! from billing.lib.common.utils import Utils %>

<%
  utils = Utils()

  def ShowDate(dt):
    try:
      return dt.strftime('%Y-%m-%d')
    except:
      return ''

  def ShowSelected(value1, value2):
    if value1 is None or value2 is None:
      return ''
    elif value1 == value2:
      return 'selected'
    else:
      return ''

  def ShowID(id):
    if id is None:
      return 'NEW'
    else:
      return id
%>

<%def name="morecss()">
<link type="text/css" href="${url('/css/dateselector.css')}" rel="stylesheet" />
</%def>

<%def name="morejs()">
<script type="text/javascript" src="${url('/js/dateselector.js')}"></script>
</%def>

##--------------------------------------------------------------------------------

<form id="frm_revenue" method="post" action="/revenues/save">

<input type="hidden" name="rev_id" value="${c.revenue.id}"/>

<table>
  <tr>
    <td class="prompt">ID:</td>
    <td>&nbsp;${ShowID(c.revenue.id)}</td>
  </tr>
  %if c.revenue.id:
  <tr>
    <td class="prompt">Total:</td>
    <td><input type="text" id="amt" name="amt" class="lookup" value="${c.revenue.total}" style="width: 70px" /></td>
  </tr>
  %endif
  <tr>
    <td class="prompt">Deposit Date:</td>
    <td>
      <input type="text" id="dep_dt" name="dep_dt" class="lookup" value="${ShowDate(c.revenue.dep_dt)}" style="text-align: center; width: 90px;" />
      <a href="#" onclick="displayDatePicker('dep_dt');"><img src="${url('/images/cal.gif')}" width="16" height="16" border="0" alt="Pick a date"></a>
    </td>
  </tr>
  <tr>
    <td class="prompt">Include inactive?:</td>
    <td>&nbsp;<input type="checkbox" id="cust_inactive"/></td>
  </tr>
</table>

<table id="tbl_details" rules="cols" cellpadding="5" style="border: 1px solid #aaa;">
  <tr class="colhdr">
    <th>X</th>
    <th>Customer</th>
    <th>Amount</th>
    <th>Received</th>
    <th>Modified</th>
    <th>Comments</th>
  </tr>
  %for d,detail in enumerate(c.revenue.details):
  <input type="hidden" id="detail.${d}.id" name="detail.${d}.id" value="${detail.id}" />
  <tr style="background-color: ${utils.COLORS[d % 2]}">
    <td align="center"><input type="checkbox" id="detail.${d}.cbx" name="detail.${d}.cbx" value="Y" />
    <td>
      <select id="detail.${d}.cust_id" name="detail.${d}.cust_id" class="lookup" style="width: 250px;">
        %for customer in c.customers:
          <option value="${customer.id}" ${ShowSelected(detail.cust_id,customer.id)}>${customer.cust_nm}</option>
        %endfor
      </select>
    </td>
    <td><input type="text" id="detail.${d}.amt" name="detail.${d}.amt" class="lookup" value="${detail.amt}" style="width: 70px" /></td>
    <td>
      <input type="text" id="detail.${d}.rcv_dt" name="detail.${d}.rcv_dt" class="lookup" value="${ShowDate(detail.rcv_dt)}" style="text-align: center; width: 90px;" />
      <a href="#" onclick="displayDatePicker('detail.${d}.rcv_dt');"><img src="${url('/images/cal.gif')}" width="16" height="16" border="0" alt="Pick a date"></a>
    </td>
    <td>${detail.mod_dt}</td>
    <td><textarea id="detail.${d}.comments" name="detail.${d}.comments" class="lookup" >${detail.comments}</textarea></td>
  </tr>
  %endfor
</table>

<div align="center" style="margin: 10px">
  <input type="submit" class="button" value="Add" onclick="AddDetail(); return false;"/>
  <input type="submit" class="button" value="Save" onclick="return CheckDetails();"/>
  %if c.revenue.id is not None:
  <input type="submit" class="button" value="Delete" onclick="ChgAction('delete');"/>
  %endif
</div>

</form>

<script type="text/javascript">
function ChgAction(a)
{
  var frm = document.getElementById('frm_revenue');
  frm.action = '/revenues/delete';
}

function AddDetail()
{
  var tbl = document.getElementById('tbl_details');
  var rowcnt = tbl.rows.length;
  var tr = tbl.insertRow(rowcnt);
  var td;
  var classes = {"True":"active", "False":"inactive"};
  var cust_inactive = document.getElementById("cust_inactive").checked;

  //checkbox
  td = tr.insertCell(0);
  var cbx = document.createElement('input');
  cbx.setAttribute("type", "checkbox");
  cbx.setAttribute("id", "detail." + rowcnt + ".cbx");
  cbx.setAttribute("name", "detail." + rowcnt + ".cbx");
  cbx.setAttribute("align", "center");
  td.appendChild(cbx);

  //customer
  td = tr.insertCell(1);
  var customers = document.createElement('select');
  customers.setAttribute("id", "detail." + rowcnt + ".cust_id");
  customers.setAttribute("name", "detail." + rowcnt + ".cust_id");
  customers.setAttribute("style", "width: 250px;");
  customers.options[0] = new Option("--Select--","");
  cnt = 0;
  %for customer in c.customers:
    if ("${str(customer.status)}" == "True" || (cust_inactive && "${str(customer.status)}" == "False"))
    {
      cnt += 1;
      customers.options[cnt] = new Option("${customer.cust_nm | n}","${customer.id}");
      customers.options[cnt].className = classes["${str(customer.status)}"];
    }
  %endfor
  td.appendChild(customers);

  //amount
  td = tr.insertCell(2);
  var amount = document.createElement('input');
  amount.setAttribute("id", "detail." + rowcnt + ".amt");
  amount.setAttribute("name", "detail." + rowcnt + ".amt");
  amount.setAttribute("style", "width: 70px");
  td.appendChild(amount);

  //received date
  td = tr.insertCell(3);
  var rcv_dt = document.createElement('input');
  rcv_dt.setAttribute("id", "detail." + rowcnt + ".rcv_dt");
  rcv_dt.setAttribute("name", "detail." + rowcnt + ".rcv_dt");
  rcv_dt.setAttribute("style", "width: 90px");
  td.appendChild(rcv_dt);
  anchor = document.createElement('a');
  anchor.href = "#";
  var fieldname = 'detail.' + rowcnt + '.rcv_dt';
  anchor.setAttribute('onclick', "displayDatePicker('detail." + rowcnt + ".rcv_dt')");
  var image = document.createElement('img');
  image.src = "/images/cal.gif";
  image.width = "16";
  image.height = "16";
  image.border = "0";
  image.alt = "Pick a date";
  anchor.appendChild(image);
  td.appendChild(anchor);

  //modified date (empty)
  td = tr.insertCell(4);

  //comments
  td = tr.insertCell(5);
  var comments = document.createElement('textarea');
  comments.setAttribute("id", "detail." + rowcnt + ".comments");
  comments.setAttribute("name", "detail." + rowcnt + ".comments");
  comments.setAttribute("style", "width: 150px");
  td.appendChild(comments);

  //set focus on the customer field
  customers.focus();
}

function CheckDetails()
{
  var tbl = document.getElementById("tbl_details");
  var fields = {"cust_id":"select a customer", "amt":"enter an amount", "rcv_dt":"select date of receipt"}
  var element;

  for (r=1; r < tbl.rows.length; r++)
  {
    for (field in fields)
    {
      element = document.getElementById("detail." + r + "." + field);
      if (element.value == null || element.value.trim() == "")
      {
        alert("Please " + fields[field] + " in row " + r + ".");
        return false;
      }
    }
  }
  return true;
}
</script>
