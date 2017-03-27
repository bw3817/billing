<%doc>
========================================
    Template: vendors/view.mako
    Author: Brian Wolf
    Date: 2009.01.04
========================================
</%doc>
<%inherit file="/vendors/index.mako"/>

<%! from billing.lib.common.utils import Utils %>

<%
  utils = Utils()

  def ShowSelected(value1,value2):
    if value1 is None or value2 is None:
      return ''
    elif value1 == value2:
      return 'selected'
    else:
      return ''
%>

##--------------------------------------------------------------------------------

<form id="frm_vendor" method="post" action="/vendors/edit/${vendor.id}">
<table>
    <tr>
        <td class="prompt">ID:</td>
        <td class="data">${vendor.id}</td>
    </tr>
    <tr>
        <td class="prompt">Vendor:</td>
        <td class="data">${vendor.vend_nm}</td>
    </tr>
    <tr>
        <td class="prompt">Category:</td>
        <td class="data">${vendor.cat_nm}
        </td>
    </tr>
    <tr>
        <td class="prompt">Status:</td>
        <td class="data">${vendor.status}
        </td>
    </tr>
    <tr>
        <td align="center" colspan="2"><input type="submit" class="button" value="Edit"/></td>
    </tr>
</table>
</form>
