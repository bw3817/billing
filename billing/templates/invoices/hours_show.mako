<%doc>
========================================
    Template: /invoices/hours_show.mako
    Author: Brian Wolf
    Date: 2014.01.27
========================================
</%doc>
<%inherit file="/invoices/base.mako"/>

<%!
  from datetime import date, timedelta
  from decimal import Decimal
%>

<%
  COLORS = {1:'odd', 0:'even'}
  BILLING_STATUS = ('unbilled', 'billed', 'paid')
  total = Decimal('0.00')
  n = 0

  def ShowSelected(value1, value2):
    if str(value1) == str(value2):
      return 'selected="selected"'
    else:
      return ''

  def SetChecked(status):
    if status == 'unbilled':
      return 'checked'
    else:
      return ''

  def SetRightMargin(status):
    if status == BILLING_STATUS[-1]:
      return 0
    else:
      return 15
%>

<%def name="morecss()">
<link type="text/css" href="${url('/css/dateselector.css')}" rel="stylesheet" />
</%def>

<%def name="morejs()">
<script type="text/javascript">
function SelectCbx(val)
{
  var elements = document.getElementsByTagName("input");
  var map = {"all":true, "none":false};
  for (var j=0; j < elements.length; j++)
  {
    if (elements[j].type == "checkbox")
      elements[j].checked = map[val];
  }
}

function CheckParams()
{
  var params = {"status": true};

  //customer
  var customer_id = document.getElementById("customer_id");
  params["customer_id"] = customer_id.value;
  if (customer_id.value == "")
  {
    alert("Please select a customer.");
    params["status"] = false;
    return params;
  }

  //project
  var project_id = document.getElementById("project_id");
  params["project_id"] = project_id.value;
  if (project_id.value == "")
  {
    alert("Please select a project.");
    params["status"] = false;
    return params;
  }

  //dates
  var from_dt = document.getElementById("from_dt");
  from_dt.value = from_dt.value.trim();
  params["from_dt"] = from_dt.value;
  if (from_dt.value == "")
  {
    alert("Please provide a start date.");
    params["status"] = false;
    return params;
  }

  var to_dt = document.getElementById("to_dt");
  to_dt.value = to_dt.value.trim();
  params["to_dt"] = to_dt.value;
  if (to_dt.value == "")
  {
    alert("Please provide an end date.");
    params["status"] = false;
    return params;
  }

  //unbilled, billed, paid
  params["unbilled"] = document.getElementById("cbx.unbilled").checked;
  params["billed"] = document.getElementById("cbx.billed").checked;
  params["paid"] = document.getElementById("cbx.paid").checked;

  //ok
  return params;
}

function GetSelections()
{
  var total=0, count=0;
  var elements = document.getElementsByTagName("input");
  var hrs = [];
  var selections = {"status": true};
  for (var j=0; j < elements.length; j++)
  {
    if (elements[j].type == "checkbox")
    {
      total += 1;
      if (elements[j].checked)
      {
        if (elements[j].id.substr(0, 8) == "id_hours")
        {
          count += 1;
          hrs.push(elements[j].value);
        }
      }
    }
  }

  if (count < 1)
  {
    alert("Please select at least one checkbox.");
    selections["status"] = false;
    return selections;
  }

  //ok
  selections["hrs"] = hrs;
  return selections;
}

function SelectCustomer(cust_id)
{
  //populate with projects for the selected customer
  var url = "/projects/find";
  var customer_id = document.getElementById("customer_id");
  var params = {"customer_id": customer_id.value};
  new Ajax.Request(url,
  {
    method: "get",
    parameters: params,
    onSuccess: function(results) {
      var json_data = results.responseText.evalJSON();
      var projects = document.getElementById("project_id");
      ClearSelect(projects);
      var option;
      for (var j=0; j < json_data.project_count; j++)
      {
        option = document.createElement("option");
        option.value = json_data.projects[j].id;
        option.text = json_data.projects[j].name;
        projects.appendChild(option);
      }
    },
    onFailure: function() {alert("There was an error with the connection.");}
  });
}

function GenerateInvoice()
{
  var params = CheckParams();
  if (!params["status"])
    return false;

  var selections = GetSelections();
  if (!selections["status"])
    return false;

  //possibly apply discount or set maximum
  discount = document.getElementById("discount");
  maximum = document.getElementById("maximum");
  params["maximum"] = maximum.value.trim();
  params["discount"] = discount.value.trim();

  //generate invoice
  var url = "/invoices/generate?hrs=" + selections["hrs"].join("&hrs=");
  new Ajax.Request(url,
  {
    method: "get",
    parameters: params,
    onSuccess: function(results) {
      var json_data = results.responseText.evalJSON();
      alert("Generated invoice: " + json_data.invoice)
    },
    onFailure: function() {alert("There was an error with the connection.");}
  });
}

function GetBillingStatus(obj)
{
  if (!obj.billed)
    return "Not billed";

  if (!obj.paid)
    return "Billed";

  return "Paid";
}

function GetHours()
{
  var params = CheckParams();
  if (!params["status"])
    return false;

  //get hours for the selected customer and project
  var url = "/hours/find";
  new Ajax.Request(url,
  {
    method: "get",
    parameters: params,
    onSuccess: function(results) {
      var json_data = results.responseText.evalJSON();
      var tbl = document.getElementById("tbl_hours");
      var rowcnt = tbl.getElementsByTagName("tr").length;

      //clear table of all but first row
      if (rowcnt > 1)
      {
        for (var r=0; r < (rowcnt - 1); r++)
          tbl.deleteRow(rowcnt - r - 1);
      }

      //add row for each item found
      var tr, td, tbx, a, node, total_hours = 0.0, total_expenses = 0.00, total_amount = 0.00;
      var classes = ["even", "odd"];
      var show_billing_status = {'U': 'Unbilled', 'B': 'Billed', 'P': 'Paid'};
      for (var r=0; r < json_data.hours_count; r++)
      {
        tr = tbl.insertRow();
        tr.className = classes[r % 2];

        // column 1: checkbox
        colcnt = 0;
        td = tr.insertCell(colcnt);
        cbx = document.createElement("input");
        cbx.type = "checkbox";
        cbx.id = "id_hours_" + json_data.hours[r].id;
        cbx.name = "hours";
        cbx.value = json_data.hours[r].id;
        td.appendChild(cbx);
        tr.appendChild(td);

        // column 2: billed, paid
        colcnt = 0;
        td = tr.insertCell(colcnt);
        node = document.createTextNode(show_billing_status[json_data.hours[r].billing_status]);
        td.appendChild(node);
        tr.appendChild(td);

        // column 3: customer
        colcnt += 1;
        td = tr.insertCell(colcnt);
        a = document.createElement("a");
        node = document.createTextNode(json_data.hours[r].customer);
        a.appendChild(node);
        a.title = json_data.hours[r].customer;
        a.href = "/customers/view/" + json_data.hours[r].cust_id;
        td.appendChild(a);
        tr.appendChild(td);

        // column 4: project
        colcnt += 1;
        td = tr.insertCell(colcnt);
        node = document.createTextNode(json_data.hours[r].project);
        td.appendChild(node);
        tr.appendChild(td);

        // column 5: performed
        colcnt += 1;
        td = tr.insertCell(colcnt);
        node = document.createTextNode(json_data.hours[r].performed);
        td.appendChild(node);
        tr.appendChild(td);

        // column 6: hours
        colcnt += 1;
        td = tr.insertCell(colcnt);
        td.align = "right";
        if (json_data.hours[r].hrs)
        {
            tbx = document.createElement("input");
            tbx.id = "hrs." + json_data.hours[r].id;
            tbx.name = "hrs." + json_data.hours[r].id;
            tbx.className = "hours";
            tbx.value = json_data.hours[r].hrs.toFixed(2);
            td.appendChild(tbx);
            tr.appendChild(td);
            total_hours += json_data.hours[r].hrs;
            total_amount += json_data.hours[r].hrs * json_data.hours[r].rate;
        }
        tr.appendChild(td);

        // column 7: expense
        colcnt += 1;
        td = tr.insertCell(colcnt);
        td.align = "right";
        if (json_data.hours[r].amt_exp)
        {
            tbx = document.createElement("input");
            tbx.id = "amt_exp." + json_data.hours[r].id;
            tbx.name = "amt_exp." + json_data.hours[r].id;
            tbx.className = "hours";
            tbx.value = json_data.hours[r].amt_exp.toFixed(2);
            total_expenses += json_data.hours[r].amt_exp;
            total_amount += json_data.hours[r].amt_exp;
            td.appendChild(tbx);
        }
        tr.appendChild(td);
      }

      //total hours
      tr = tbl.insertRow();
      tr.className = "total";

      // column 1: total
      colcnt = 0;
      td = tr.insertCell(colcnt);
      td.align = "right";
      td.colSpan = 6;
      node = document.createTextNode(total_hours.toFixed(2));
      td.appendChild(node);

      colcnt += 1;
      td = tr.insertCell(colcnt);
      td.align = "right";
      node = document.createTextNode(total_expenses.toFixed(2));
      td.appendChild(node);
      tr.appendChild(td);

      //total billable amount
      tr = tbl.insertRow();
      tr.className = "total";

      // column 1: billable amount
      colcnt = 0;
      td = tr.insertCell(colcnt);
      td.align = "right";
      td.colSpan = 6;
      node = document.createTextNode("$" + total_amount.toFixed(2));
      td.appendChild(node);
      tr.appendChild(td);

      // column 2: expense amount
      colcnt += 1;
      td = tr.insertCell(colcnt);
      td.align = "right";
      node = document.createTextNode("$" + total_expenses.toFixed(2));
      td.appendChild(node);
      tr.appendChild(td);

      //discount and maximum
      var fields = ["discount","maximum"];
      for (var r=0; r < fields.length; r++)
      {
        tr = tbl.insertRow();
        tr.className = classes[(r + json_data.hours_count) % 2];

        // column 1: empty column
        colcnt = 0;
        td = tr.insertCell(colcnt);
        td.align = "right";
        td.colSpan = 4;
        node = document.createTextNode(fields[r].capitalize() + ":");
        td.appendChild(node);
        tr.appendChild(td);

        // column 2: extra field
        colcnt += 1;
        td = tr.insertCell(colcnt);
        tbx = document.createElement("input");
        tbx.type = "text";
        tbx.id = fields[r];
        tbx.style.width = "65px";
        td.appendChild(tbx);
        tr.appendChild(td);

        // column 3: another empty column
        colcnt += 1;
        td = tr.insertCell(colcnt);
        tr.appendChild(td);
      }
    },
    onFailure: function() {
      alert("There was an error with the connection.");
    }
  });
}

function Billed()
{
  var selections = GetSelections();
  if (!selections["status"])
    return false;

  //set checked hours as billed
  var url = "/hours/setbilled?hrs=" + selections["hrs"].join("&hrs=");
  new Ajax.Request(url,
  {
    method: "get",
    //parameters: params,
    onSuccess: function(results) {
      var json_data = results.responseText.evalJSON();
      alert(json_data.msg);
    },
    onFailure: function() {
      alert("There was an error with the connection.");
    }
  });
}

function Paid()
{
  var selections = GetSelections();
  if (!selections["status"])
    return false;

 //set checked hours as paid
  var url = "/hours/setpaid?hrs=" + selections["hrs"].join("&hrs=");
  new Ajax.Request(url,
  {
    method: "get",
    //parameters: params,
    onSuccess: function(results) {
      var json_data = results.responseText.evalJSON();
      alert(json_data.msg);
    },
    onFailure: function() {
      alert("There was an error with the connection.");
    }
  });
}

function ExecFn(fn, context, args)
{
    var args = Array.prototype.slice.call(arguments, 2);
    var namespaces = fn.split(".");
    var func = namespaces.pop();
    for (var j=0; j < namespaces.length; j++)
    {
        context = context[namespaces[j]];
    }
    return context[func].apply(context, args);
}

function TakeAction()
{
  var sel = document.getElementById("sel_actions");
  //var t = sel.options[sel.selectedIndex].text;
  var p = sel.value.indexOf("(");
  var fn = sel.value.substr(0, p);
  var args = sel.value.substring(p+1, sel.value.length-1).split(",");
  var j = 0;
  args.forEach(function(arg) {
    if (arg.substr(0,1) == "'")
      arg = arg.substr(1);
    if (arg.substr(arg.length-1) == "'")
      arg = arg.substr(0,arg.length-1);
    args[j] = arg;
    j += 1;
  });
  ExecFn(fn, window, args);
}

function UpdateHours()
{

  //get hours for the selected customer and project
  var url = "/hours/update";
  var tbl = document.getElementById("tbl_hours");
  var rows = tbl.getElementsByTagName("tr");
  var params = {}, elements;
  if (rows.length == 1)
    return;
  for (var j=1; j < rows.length - 4; j++)
  {
    elements = rows[j].getElementsByTagName("input");
    for (var k=0; k < elements.length; k++)
    {
      if (elements[k].type == "text")
        params[elements[k].id] = elements[k].value;
    }
  }

  new Ajax.Request(url,
  {
    method: "get",
    parameters: params,
    onSuccess: function(results) {
      var json_data = results.responseText.evalJSON();
      alert(json_data.msg + "\nNumber of rows: " + json_data.rowcnt);
    },
    onFailure: function() {alert("There was an error with the connection.");}
  });
}

</script>
</%def>

##--------------------------------------------------------------------------------

<table cellpadding="10px" cellspacing="5px">
  <tr>
    <td>
      Customer:
      <select id="customer_id" name="customer_id" onchange="SelectCustomer(this.value);" required>
        <option value="">--Select--</option>
        %for customer in customers:
        <option value="${customer.id}" ${ShowSelected(last_cust_id,customer.id) | n}>${customer.cust_nm | n}</option>
        %endfor
      </select>
    </td>

    <td>
      Project:
      <select id="project_id" name="project_id" required>
        <option value="all">All Projects</option>
        %for project_id,name in projects[last_cust_id].items():
        <option value="${project_id}" ${ShowSelected(last_project_id,project_id) | n}>${name | n}</option>
        %endfor
      </select>
    </td>
  </tr>

  <tr>
    <td>
      <fieldset style="padding: 10px; width: 180px;">
        <legend>Dates</legend>
        <div>
          From: <input type="text" id="from_dt" name="from_dt" value="${settings['from_dt']}" style="width: 80px" required/>
          <a href="#" onclick="displayDatePicker('from_dt');"><img src="${url('/images/cal.gif')}" width="16" height="16" border="0" alt="Pick a date"></a>
        </div>
        <div>
          &nbsp;&nbsp;&nbsp; To: <input type="text" id="to_dt" name="to_dt" value="${settings['to_dt']}" style="width: 80px" required/>
          <a href="#" onclick="displayDatePicker('to_dt');"><img src="${url('/images/cal.gif')}" width="16" height="16" border="0" alt="Pick a date"></a>
        </div>
      </fieldset>
    </td>

    <td style="vertical-align: top;">
      <fieldset style="padding: 10px; width: 240px;">
        <legend>Search Parameters</legend>
          %for status in BILLING_STATUS:
          <input type="checkbox" id="cbx.${status}" value="1" ${SetChecked(status)}/> <span style="margin-right: ${SetRightMargin(status)}px;">${status.capitalize()}</span>
          %endfor
      </fieldset>
    </td>
  </tr>

</table>

<div>
  <button style="margin: 10px;" onclick="GetHours();">Get Hours</button>
</div>

<div style="margin-top: 20px;">
  <select id="sel_actions">
    <option value="SelectCbx('all')">Select ALL</option>
    <option value="SelectCbx('none')">Select NONE</option>
    <option value="GenerateInvoice()">Invoice</option>
    <option value="Billed()">Billed</option>
    <option value="Paid()">Paid</option>
    <option value="UpdateHours()">Update Hours</option>
  </select>
  <button onclick="TakeAction();">Take Action</button>
</div>

<table id="tbl_hours" cellpadding="5px" cellspacing="5px" style="width: 100%;">
  <tr class="total">
    <th>&nbsp;</th>
    <th>Status</th>
    <th>Customer</th>
    <th>Project</th>
    <th>Date</th>
    <th>Hours</th>
    <th>Expenses</th>
  </tr>
</table>
