<%doc>
========================================
    Template: /invoices/invoice_generate.mako
    Author: Brian Wolf
    Date: 2014.01.27
========================================
</%doc>
<%inherit file="/invoices/base.mako"/>

<%! from datetime import date, timedelta %>

<%
  COLORS = {1:'odd', 0:'even'}

  def ShowSelected(value1, value2):
    if str(value1) == str(value2):
      return 'selected="selected"'
    else:
      return ''
%>


##--------------------------------------------------------------------------------

<p>${customer.rate}</p>

<p>${from_dt}</p>
<p>${to_dt}</p>

%for hr in hours:
<p>${hr}</p>
%endfor
