<%doc>
========================================
	Template: showuser.mako
	Author: Brian Wolf
	Date: 2009.11.01
========================================
</%doc>
<%!
  from pylons import session
  from datetime import datetime
%>

<%
  def ShowLoginDT():
    dt = session['login_dt'].split(' ')
    return datetime( *tuple( map(int,dt[0].split('-')) + map(int,dt[1].split(':')) ) ).strftime("%I:%M %p").lower()
%>

##--------------------------------------------------------------------------------

<div>${c.user.full_name}</div>
<div>Login: ${ShowLoginDT()}</div>
<div>Current: ${datetime.now().strftime("%I:%M %p").lower()}</div>
