<%doc>
========================================
    Template: login.mako
    Author: Brian Wolf
    Date: 2009.11.11
========================================
</%doc>
<%!
  import os
  from pylons import request, session
%>

<%
  messages = h.flash.pop_messages()
  if messages:
    message = messages[0]
  else:
    message = ''
%>


##--------------------------------------------------------------------------------

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
<meta name="description" content="Activus Billing">
<meta name="keywords" content="">
<title>Activus Billing</title>
<link rel="stylesheet" href="/css/billing.css" type="text/css" />
<script type="text/javascript">
var requiredfields = {'usrnam': 'User ID', 'pwd':'Password'};
function BtnClicked(obj)
{
    document.getElementById('btn').value = obj.id;
}
</script>
</head>

<body style="background-color: #fefefe;" onload="document.frm_login.usrnam.focus();">
<div align="center" style="color: #330000; font-size: 18pt; font-style: normal; font-family: arial, helvetica, sans-serif; padding: 20px;">Activus Billing</div>
<form name="frm_login" method="post" action="/site/loginsubmit" enctype="multipart/form-data">
<input type="hidden" id="btn" name="btn" value=""/>
<table align="center" style="background-color: #E5EAF7; border: 1px solid #330000; padding: 5px; width: 280px;">
    <tr align="center">
        <td class="error-message" colspan="2">${message}</td>
    </tr>

    <tr align="center">
        <td class="prompt" width="100">User ID:</td>
        <td><input class="lookup" type="text" id="usrnam" name="usrnam" value="${session.get('usrnam')}" required="true" tabindex="10" maxlength="5" /></td>
    </tr>

    <tr align="center">
        <td class="prompt" width="100">Password:</td>
        <td class="info"><input class="lookup" type="password" id="pwd" name="pwd" required="true" tabindex="20" /></td>
    </tr>

    <tr>
        <td align="center" colspan="2" style="padding-top: 10px;">
        <input class="button" type="submit" id="login" value="Login" tabindex="30" onclick="BtnClicked(this); return CheckRequiredFields();" />
        </td>
    </tr>
</table>
</form>
</body>
</html>
