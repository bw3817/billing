<%doc>
========================================
	Template: revenues/report.mako
	Author: Brian Wolf
	Date: 2009.01.05
========================================
</%doc>
<%inherit file="/revenues/index.mako"/>

<%!
  from datetime import date, timedelta
%>

<%def name="morecss()">
<link type="text/css" href="${url('/css/dateselector.css')}" rel="stylesheet" />
</%def>

<%def name="morejs()">
<script type="text/javascript" src="${url('/js/dateselector.js')}"></script>
</%def>

##--------------------------------------------------------------------------------

<div style="border: 1px solid #aaa; width: 400px; padding: 10px;">
	Report By Date Range
	<form id="frm_expense_rpt" method="post" action="/revenues/results/bydate">
	<div>Start Date:
	  <input type="text" id="start_dt" name="start_dt" value="" style="text-align: center; width: 90px;" />
	  <a href="#" onclick="displayDatePicker('start_dt');"><img src="${url('/images/cal.gif')}" width="16" height="16" border="0" alt="Pick a date"></a>
	</div>
	<div>End Date:
	  <input type="text" id="end_dt" name="end_dt" value="" style="text-align: center; width: 90px;" />
	  <a href="#" onclick="displayDatePicker('end_dt');"><img src="${url('/images/cal.gif')}" width="16" height="16" border="0" alt="Pick a date"></a>
	</div>
	<div>Customer:
	  <select id="cust_id" name="cust_id" class="lookup" style="width: 250px">
	    <option value="all">All Customers</option>
	    %for customer in c.customers:
	    <option value="${customer.id}">${customer.cust_nm}</option>
	    %endfor
	  </select>
	</div>
	<div align="center" style="padding-top: 10px;"><input type="submit" class="button" value="Generate Report"/></div>
	</form>
</div>
