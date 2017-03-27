<%doc>
========================================
    Template: /invoices/projects_add.mako
    Author: Brian Wolf
    Date: 2014.01.30
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

<%def name="morejs()">
<script type="text/javascript">
var projects = {};
%for key,values in projects.items():
projects["${key}"] = {};
%for k,v in values.items():
projects["${key}"]["${k}"]= "${v}";
%endfor
%endfor

function ShowProjects(cust_id)
{
  if (cust_id == "")
  {
    alert("Please select a customer.")
    return;
  }

  //display existing projects
  var projectlist = document.getElementById("projectlist");
  projectlist.innerHTML = "";
  var cust_projects = projects[cust_id];
  if (cust_projects !== undefined)
  {
    var div;
    for (proj_id in cust_projects)
    {
      div = document.createElement("div");
      div.innerHTML = cust_projects[proj_id];
      projectlist.appendChild(div);
    }
  }
}

function CheckProject()
{
  var customer_id = document.getElementById("customer_id");
  if (customer_id.value == "")
  {
    alert("Please select a customer.")
    return false;
  }

  var project = document.getElementById("project");
  project.value = project.value.trim();
  if (project.value == "")
  {
    alert("Please enter a project.");
    return false;
  }
  return true;
}
</script>
</%def>

##--------------------------------------------------------------------------------

<form id="frm_projects" method="post" action="/projects/add/save">

  <div>
    Customer:
    <select id="customer_id" name="customer_id" onchange="ShowProjects(this.value);" required>
      <option value="">--Select--</option>
      %for customer in customers:
      <option value="${customer.id}" ${ShowSelected(last_cust_id,customer.id) | n}>${customer.cust_nm | n}</option>
      %endfor
    </select>
  </div>

  <div style="margin: 10px">
    Existing projects:
    <div id="projectlist">
      %for project_id,name in projects[last_cust_id].items():
      <div>${name | n}</div>
      %endfor
    </div>
  </div>

  <div style="margin: 10px">
    Project:
    <input type="text" id="project" name="project"/>
  </div>

  <button onclick="return CheckProject();">Save</button>
</form>
