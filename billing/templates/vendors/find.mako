<%doc>
========================================
    Template: vendors/find.mako
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
  MAPSTATUS = {True: 'Active', False:'Inactive'}
  FGCOLORS = {True:'', False:'style="color: #AFB4C4;"'}

  def ShowChecked(value):
    if c.status in ('AN','NA'):
      return 'checked'
    elif c.status == value:
      return 'checked'
    else:
      return ''
%>

##--------------------------------------------------------------------------------

<div align="center" style="margin: 5px">
  <input type="checkbox" id="vendor_status_active" name="vendor_status" value="A" onchange="SetStatus(this, document.getElementById('vendor_status_inactive'));" ${ShowChecked('A')}/>&nbsp;Active
  <span style="margin-right: 15px">&nbsp;</span>
  <input type="checkbox" id="vendor_status_inactive" name="vendor_status" value="N" onchange="SetStatus(this, document.getElementById('vendor_status_active'));" ${ShowChecked('N')}/>&nbsp;Inactive
</div>

<script type="text/javascript">
function SetStatus(obj, other_obj)
{
  var params = "";
  if (obj.checked)
      params += obj.value;
  if (other_obj.checked)
      params += other_obj.value;
  window.location = "/vendors/find?status=" + params;
}

</script>


<table style="border: 1px solid #aaa; width: 100%">
  <tr class="colhdr">
    <th>ID</th>
    <th>Vendor</th>
    <th>Category</th>
    <th>Status</th>
  </tr>
  %for n,vendor in enumerate(vendors):
  <tr style="background-color: ${utils.COLORS[n % 2]}">
    <td ${FGCOLORS[vendor.status] | n}>${vendor.id}</td>
    <td><a ${FGCOLORS[vendor.status] | n} href="/vendors/view/${vendor.id}">${vendor.vend_nm}</a></td>
    <td ${FGCOLORS[vendor.status] | n}>${vendor.cat_nm}</td>
    <td ${FGCOLORS[vendor.status] | n}>${MAPSTATUS[vendor.status]}</td>
  </tr>
  %endfor
</table>

