<%doc>
========================================
	Template: vendors/index.mako
	Author: Brian Wolf
	Date: 2010.01.03
========================================
</%doc>
<%inherit file="/base.mako"/>

##--------------------------------------------------------------------------------

<%def name="section()">
Vendors
</%def>

<%def name="leftnav()">
<div><hr style="color: #E8EBF4"/></div>
<div class="leftnav"><a href="/vendors/find?status=A">List Vendors</a></div>
<div class="leftnav"><a href="/vendors/new">New Vendor</a></div>
<div class="leftnav"><hr/></div>
<div class="leftnav"><a href="/categories/find">List Categories</a></div>
<div class="leftnav"><a href="/categories/new">New Category</a></div>
</%def>
