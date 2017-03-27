<%doc>
========================================
  Template: base.mako
  Author: Brian Wolf
  Date: 2009.11.01
========================================
</%doc>
<%!
  import os.path
  from datetime import date
  from pylons import session
%>

<%
  def getTemplate():
    try:
      return os.path.splitext(os.path.split(self.filename)[-1])[0]
    except:
      return "unknown"
%>

##--------------------------------------------------------------------------------

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="keyword" content="" />
<meta name="description" content=" " />
<title>Activus Billing</title>
<link rel="stylesheet" href="/css/billing.css" type="text/css" />
<link rel="stylesheet" href="/css/tabs.css" type="text/css" />
<link rel="stylesheet" href="/css/dateselector.css" type="text/css" />
<link rel="stylesheet" href="/css/autocomplete.css" type="text/css" />
${self.morecss()}
<script type="text/javascript" src="/js/scriptaculous/prototype.js"></script>
<script type="text/javascript" src="/js/scriptaculous/scriptaculous.js"></script>
<script type="text/javascript" src="/js/dateselector.js"></script>
<script type="text/javascript" src="/js/utils.js"></script>
${self.morejs()}
</head>

<body onload="SetTitle();">
<table id="tbl_toplevel" class="tbl_toplevel" style="margin-left: auto; margin-right: auto; padding: 10px;">
  <tr valign="top" style="color: #515874; background-color: #E8EBF4;">
    <td style="padding: 10px;"><%include file="showuser.mako" args="user=user"/></td>
    <td align="center" style="padding: 2px;">
      <div style="font-size: 18px;">Activus Billing</div>
      <div style="font-size: 12px;">${self.section()}</div>
    </td>
  </tr>
  <tr>
    <td valign="top" rowspan="2">
      <div class="boxcontent">
           <div class="colhdr">Navigation</div>
           <div class="leftnav"><a href="/home">Home</a></div>
           <div class="leftnav"><a href="/site/logoff">Logoff</a></div>
        ${self.leftnav()}
      </div>
    </td>
    <td valign="top" style="border: 1px solid #aaa;height: 99%;">${self.topnav()}</td>
  </tr>
  <tr>
    <td valign="top" style="padding: 0px 10px 0px 10px;">${self.body()}</td>
  </tr>
  <tr>
    <td id="footer" align="center" colspan="4">&copy;&nbsp;${date.today().year} Activus Technologies. All rights reserved.</td>
  </tr>
</table>
</body>
</html>

<%def name="section()">
</%def>

<%def name="topnav()">
<div>
  ##<button class="mainmenu" onclick="Go('/categories')">Categories</button>
  <button class="mainmenu" onclick="Go('/vendors')">Vendors</button>
  <button class="mainmenu" onclick="Go('/expenses')">Expenses</button>
  <button class="mainmenu" onclick="Go('/customers')">Customers</button>
  <button class="mainmenu" onclick="Go('/revenues')">Revenues</button>
  <button class="mainmenu" onclick="Go('/hours')">Hours</button>
  %if session.get('super'):
  <button class="mainmenu" onclick="Go('/admin');">Admin</button>
  %endif
</div>
</%def>

<%def name="leftnav()">
</%def>

<%def name="displaylogin()">
  ## if not logged in then display link to log in
      <div class="module">
        <h3>Log In</h3>
        <p>
        First Name:<br /><input type="text" name="first_name" id="first_name"/>
        Last Name:<br /><input type="text" name="last_name" id="last_name"/>
        </p>
        <p>Password:<br />
          <input type="text" name="pwd" id="pwd" />
        </p>
        <input type="submit" name="login" id="login" value="Log In" />
        <div class="clear-both" ></div>
      </div>
</%def>

<%def name="morecss()">
</%def>

<%def name="morejs()">
</%def>
