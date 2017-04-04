<%doc>
========================================
	Template: customers/error.mako
	Author: Brian Wolf
	Date: 2012.04.30
========================================
</%doc>
<%inherit file="/customers/index.mako"/>

<%! from pylons import request %>

##Notes:
##request.url is the entire URL
##request.path_qs is the remainder (path) only

##--------------------------------------------------------------------------------

<div>Sorry, but <span class="error-message">${request.url}</span></div>
<div>has not been implemented.</div>
