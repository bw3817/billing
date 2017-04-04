<%doc>
========================================
	Template: customers/find.mako
	Author: Brian Wolf
	Date: 2009.12.31
========================================
</%doc>
<%inherit file="/customers/index.mako"/>

<%! from billing.lib.common.utils import Utils %>

<%
  utils = Utils()
  MAPSTATUS = {True: 'Active', False:'Inactive'}
  FGCOLORS = {True:'', False:'style="color: #AFB4C4;"'}
%>

##--------------------------------------------------------------------------------

<div align="center">
  %for letter in letters:
  <a href="/customers/find/${letter.letter}" style="padding: 2px">${letter.letter}</a>
  %endfor
  <button onclick="window.location='/customers/all'">ALL</button>
</div>

<table style="border: 1px solid #aaa; width: 100%">
  <tr class="colhdr">
    <th>ID</th>
    <th>Customer</th>
    <th>Type</th>
    <th>Status</th>
  </tr>
  %for n,customer in enumerate(customers):
  <tr style="background-color: ${utils.COLORS[n % 2]}">
    <td ${FGCOLORS[customer.status] | n}>${customer.id}</td>
    <td><a href="/customers/view/${customer.id}" ${FGCOLORS[customer.status] | n}>${customer.cust_nm}</a></td>
    <td ${FGCOLORS[customer.status] | n}>${customer.cust_type}</td>
    <td ${FGCOLORS[customer.status] | n}>${MAPSTATUS[customer.status]}</td>
  </tr>
  %endfor
</table>

