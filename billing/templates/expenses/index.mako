<%doc>
========================================
	Template: expenses/index.mako
	Author: Brian Wolf
	Date: 2009.12.31
========================================
</%doc>
<%inherit file="/base.mako"/>

<%! from datetime import date %>

##--------------------------------------------------------------------------------

<%def name="section()">
Expenses
</%def>

<%def name="leftnav()">
<div><hr style="color: #E8EBF4"/></div>
<div class="leftnav"><a href="/expenses/eoy/${date.today().year - 1}">EOY Category Report</a></div>
<div class="leftnav"><a href="/expenses/eoy/${date.today().year}">YTD Category Report</a></div>
<div class="leftnav"><a href="/expenses/report">Expense Report</a></div>
<div class="leftnav"><a href="/expenses/new">New Expense</a></div>
</%def>

