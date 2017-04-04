<%doc>
========================================
    Template: /invoices/items_add.mako
    Author: Brian Wolf
    Date: 2015.01.30
========================================
</%doc>
<%inherit file="/invoices/base.mako"/>

<%! from datetime import date %>

<%
  def ShowSelected(value1, value2):
    if str(value1) == str(value2):
      return 'selected="selected"'
    else:
      return ''
%>

<%def name="morecss()">
<link type="text/css" href="${url('/css/dateselector.css')}" rel="stylesheet" />
</%def>

<%def name="morejs()">
<script type="text/javascript">
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

  //date
  var performed = document.getElementById("performed");
  performed.value = performed.value.trim();
  params["performed"] = performed.value;
  if (performed.value == "")
  {
    alert("Please provide a date.");
    params["status"] = false;
    return params;
  }

  //hours
  var hrs = document.getElementById("hrs");
  hrs.value = hrs.value.trim();
  params["hrs"] = hrs.value;

  var amt_exp = document.getElementById("amt_exp");
  amt_exp.value = amt_exp.value.trim();
  params["amt_exp"] = amt_exp.value;

  if (hrs.value == "" && amt_exp.value == "")
  {
    alert("Please enter either hours or expense amount.");
    params["status"] = false;
    return params;
  }

  //ok
  return params;
}

function Validate()
{
  var params = CheckParams();
  return params["status"];
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
</script>
</%def>

##--------------------------------------------------------------------------------

<div class="container">

<form id="frm_hours" method="post" action="/hours/save">

  <input type="hidden" id="hours_id" name="hours_id" value="${hours_id}"/>

  <div>
    Customer:
    <select id="customer_id" name="customer_id" onchange="SelectCustomer(this.value);" required>
      <option value="">--Select--</option>
      %for customer in customers:
      <option value="${customer.id}" ${ShowSelected(last_cust_id,customer.id) | n}>${customer.cust_nm | n}</option>
      %endfor
    </select>
  </div>

  <div>
    Project:
    <select id="project_id" name="project_id" required>
      <option value="">--Select--</option>
      %for project_id,name in projects[last_cust_id].items():
      <option value="${project_id}" ${ShowSelected(last_project_id,project_id) | n}>${name | n}</option>
      %endfor
    </select>
  </div>

  <div>
    Date:
    <input type="text" id="performed" name="performed" value="${date.today().isoformat()}" style="width: 80px" required/>
    <a href="#" onclick="displayDatePicker('performed');"><img src="${url('/images/cal.gif')}" width="16" height="16" border="0" alt="Pick a date"></a>
  </div>

  <div>
    Hours:
    <input type="text" id="hrs" name="hrs" value="" style="width: 40px;"/>
  </div>

  <div>
    Expense:
    <input type="text" id="amt_exp" name="amt_exp" value="" style="width: 40px;"/>
  </div>

  <div style="vertical-align: middle;">
    <div>Comments:</div>
    <textarea id="comments" name="comments"></textarea>
  </div>

  <button onclick="return Validate();">Save</button>

</form>

</div>
