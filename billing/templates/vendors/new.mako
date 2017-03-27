<%doc>
========================================
	Template: vendors/new.mako
	Author: Brian Wolf
	Date: 2009.01.03
========================================
</%doc>
<%inherit file="/vendors/index.mako"/>

<%
  def ShowSelected(value1, value2):
    if value1 == value2:
      return 'selected'
    else:
      return ''
%>

##--------------------------------------------------------------------------------

<form id="frm_vendor" method="post" action="/vendors/save">
<input type="hidden" name="vend_id" value="${c.vendor.id}"/>
<table>
	<tr>
		<td>Vendor:</td>
		<td><input type="text" id="vend_nm" name="vend_nm" class="lookup" value="${c.vendor.vend_nm}" style="width: 250px" maxlength="40"/></td>
	</tr>
	<tr>
		<td>Category:</td>
		<td>
		  <select id="cat_id" name="cat_id" class="lookup">
		    %for category in c.categories:
		    <option value="${category.id}" ${ShowSelected(category.id,c.vendor.cat_id)}>${category.cat_nm}</option>
		    %endfor
		  </select>
		</td>
	</tr>
	<tr>
		<td>Status:</td>
		<td>
		  <select id="status" name="status" class="lookup">
		    <option value="1" ${ShowSelected(c.vendor.status,True)}>Active</option>
		    <option value="0" ${ShowSelected(c.vendor.status,False)}>Inactive</option>
		  </select>
		</td>
	</tr>
	<tr>
		<td align="center" colspan="2"><input type="submit" class="button" value="Save"/></td>
	</tr>
</table>
</form>
