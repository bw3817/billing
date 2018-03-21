<%doc>
========================================
    Template: revenues/index.mako
    Author: Brian Wolf
    Date: 2010.01.05
========================================
</%doc>
<%inherit file="/base.mako"/>

<%!
  from datetime import date

  current_year = date.today().year
  yrs = range(current_year - 3, current_year + 1)

  def ShowSelected(value1, value2):
    if value1 == value2:
      return 'selected'
    else:
      return ''
%>

##--------------------------------------------------------------------------------

<%def name="section()">
Revenues
</%def>

<%def name="leftnav()">
<div><hr style="color: #E8EBF4"/></div>
<div class="leftnav"><a href="/revenues/report">Revenue Report</a></div>
<div class="leftnav"><a href="/revenues/new">New Revenue</a></div>
<div class="leftnav">
  <form id="id_summmary_frm" method="post" action="/revenues/summary">
    <a href="/revenues/summary">Summary</a>
    <select id="id_rev_year" name="rev_year">
      %for yr in yrs:
      <option value="${yr}" ${ShowSelected(yr, current_year)}>${yr}</option>
      %endfor
    </select>
    <button type="submit">Go</button>
  </form>
</div>
</%def>

