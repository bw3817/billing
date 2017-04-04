<%doc>
========================================
    Template: /invoices/base.mako
    Author: Brian Wolf
    Date: 2009.12.31
========================================
</%doc>
<%inherit file="/base.mako"/>

##--------------------------------------------------------------------------------

<%def name="section()">
Invoices
</%def>

<%def name="leftnav()">
<div><hr style="color: #E8EBF4"/></div>
<div class="leftnav"><a href="/projects/manage">Manage Projects</a></div>
<div class="leftnav"><a href="/projects/add">Add Project</a></div>
<div class="leftnav"><hr/></div>
<div class="leftnav"><a href="/hours/show">Show Hours</a></div>
<div class="leftnav"><a href="/hours/add">Add Hours</a></div>
</%def>

