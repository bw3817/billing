<%doc>
========================================
    Template: categories/view.mako
    Author: Brian Wolf
    Date: 2009.01.03
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
%>

##--------------------------------------------------------------------------------

<form id="frm_category" method="post" action="/categories/edit/${category.id}">
    <table>
        <tr>
            <td class="prompt">ID:</td>
            <td class="data">${category.id}</td>
        </tr>
        <tr>
            <td class="prompt">Category:</td>
            <td class="data">${category.cat_nm}</td>
        </tr>
        <tr>
            <td class="prompt">Active:</td>
            <td>${MAPSTATUS[category.status]}</td>
        </tr>
        <tr>
            <td align="center" colspan="2"><input type="submit" class="button" value="Edit"/></td>
        </tr>
    </table>
</form>
