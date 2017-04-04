<%doc>
========================================
    Template: /invoices/projects_manage.mako
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

  def ShowChecked(value1, value2):
    if str(value1) == str(value2):
      return 'checked'
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
    var div, cbx, node;
    for (proj_id in cust_projects)
    {
      div = document.createElement("div");
      cbx = document.createElement("input");
      cbx.type = "checkbox";
      cbx.id = "project." + proj_id;
      cbx.value = proj_id;
      cbx.checked = true;
      div.appendChild(cbx);
      node = document.createTextNode(cust_projects[proj_id]);
      div.appendChild(node);
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

<form id="frm_projects" method="post" action="/projects/manage/save">

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
    Projects:
    <div id="projectlist">
      %for project_id,name in projects[last_cust_id].items():
      <div><input type="checkbox" name="project.${project_id}" value="${project_id}" checked/>${name | n}</div>
      %endfor
    </div>
  </div>

  <button onclick="return CheckProject();">Save</button>
</form>
