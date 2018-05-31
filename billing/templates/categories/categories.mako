<%doc>
========================================
    Template: vendors/categories.mako
    Author: Brian Wolf
    Date: 2010.01.03
========================================
</%doc>
<%inherit file="/vendors/index.mako"/>

<%!
  from billing.lib.common.utils import Utils
%>

<%
  utils = Utils()
  MAPSTATUS = {True: 'Active', False: 'Inactive'}
  FGCOLORS = {True: '', False: 'style="color: #AFB4C4;"'}

  def ShowChecked(value):
    if c.status in ('AN','NA'):
      return 'checked'
    elif c.status == value:
      return 'checked'
    else:
      return ''


  messages = h.flash.pop_messages()
%>

##--------------------------------------------------------------------------------

%for message in messages:
<div class="error-message">${message}</div>
%endfor

<div align="center" style="margin: 5px">
  <input type="checkbox" id="category_status_active" name="category_status" value="A" onchange="SetStatus(this, document.getElementById('category_status_inactive'));" ${ShowChecked('A')}/>&nbsp;Active
  <span style="margin-right: 15px">&nbsp;</span>
  <input type="checkbox" id="category_status_inactive" name="category_status" value="N" onchange="SetStatus(this, document.getElementById('category_status_active'));" ${ShowChecked('N')}/>&nbsp;Inactive
</div>

<script type="text/javascript">
function SetStatus(obj, other_obj)
{
  var params = "";
  if (obj.checked)
      params += obj.value;
  if (other_obj.checked)
      params += other_obj.value;
  window.location = "/categories/find?status=" + params;
}

</script>

<table style="border: 1px solid #aaa; width: 100%">
  <tr class="colhdr">
    <th>ID</th>
    <th>Category</th>
    <th>Status</th>
  </tr>

  %for n, category in enumerate(categories):
  <tr style="background-color: ${utils.COLORS[n % 2]}">
    <td>${category.id}</td>
    <td><a href="/categories/view/${category.id}">${category.cat_nm}</a></td>
    <td>${MAPSTATUS[category.status]}</td>
  </tr>
  %endfor

</table>

