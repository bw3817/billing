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
%>

##--------------------------------------------------------------------------------

<table style="border: 1px solid #aaa; width: 100%">
  <tr class="colhdr">
    <th>ID</th>
    <th>Category</th>
  </tr>
  %for n,category in enumerate(categories):
  <tr style="background-color: ${utils.COLORS[n % 2]}">
    <td>${category.id}</td>
    <td><a href="/categories/view/${category.id}">${category.cat_nm}</a></td>
  </tr>
  %endfor
</table>

