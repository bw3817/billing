<%doc>
========================================
    Template: categories/new.mako
    Author: Brian Wolf
    Date: 2009.01.03
========================================
</%doc>
<%inherit file="/vendors/index.mako"/>

<%
  def ShowChecked(value):
    if value:
      return 'checked'
    else:
      return ''
%>

##--------------------------------------------------------------------------------

<form id="frm_category" method="post" action="/categories/save">
<input type="hidden" name="cat_id" value="${category.id}"/>
<table>
    <tr>
        <td>Category:</td>
        <td><input type="text" id="cat_nm" name="cat_nm" class="lookup" value="${category.cat_nm}" style="width: 250px" maxlength="40"/></td>
    </tr>
    <tr>
        <td>Status:</td>
        <td><input type="checkbox" id="status" name="status" class="lookup" value="1" ${ShowChecked(category.status)}/></td>
    </tr>
    <tr>
        <td align="center" colspan="2"><input type="submit" class="button" value="Save"/></td>
    </tr>
</table>
</form>
