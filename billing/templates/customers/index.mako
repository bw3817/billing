<%doc>
========================================
	Template: customers/index.mako
	Author: Brian Wolf
	Date: 2009.12.31
========================================
</%doc>
<%inherit file="/base.mako"/>

##--------------------------------------------------------------------------------

<%def name="section()">
Customers
</%def>

<%def name="leftnav()">
<div><hr style="color: #E8EBF4"/></div>
<div class="leftnav"><a href="/customers/xcharge/setmonth">Set Month</a></div>
<div class="leftnav"><a href="/customers/xcharge/mvd">Import X-Charge Commissions</a></div>
<div class="leftnav"><a href="/customers/xcharge/view">View X-Charge Commissions</a></div>
<div class="leftnav"><a href="/customers/xcharge/report">X-Charge Report</a></div>
<div class="leftnav"><a href="/customers/find">Customers</a></div>
<div class="leftnav"><a href="/customers/new">New Customer</a></div>
</%def>

