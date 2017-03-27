<%doc>
========================================
    Template: expenses/report.mako
    Author: Brian Wolf
    Date: 2009.01.04
========================================
</%doc>
<%inherit file="/expenses/index.mako"/>

<%! from datetime import date, timedelta %>

<%
  def ShowSelect(id1, id2):
    if str(id1 or "") == str(id2 or ""):
      return 'selected'
    else:
      return ''
%>

<%def name="morecss()">
<link type="text/css" href="${url('/css/dateselector.css')}" rel="stylesheet" />
</%def>

<%def name="morejs()">
<script type="text/javascript">
function GetVendors(cat_id)
{
    var url = "/ajax/vendors_per_category/" + cat_id;
    new Ajax.Request(url,
    {
      method: 'get',
      onSuccess: ShowVendors,
      onFailure: function() {alert("There was an error with the connection.");}
    });
}

function ShowVendors(results)
{
    var json_data = results.responseText.evalJSON();

    var vendor = document.getElementById('vend_id');
    vendor.options.length = 0;
    vendor.options[0] = new Option("All Vendors","all");
    for (j=0; j < json_data.length; j++)
        vendor.options[j+1] = new Option(json_data[j].vend_nm, json_data[j].id);
}
</script>
</%def>

##--------------------------------------------------------------------------------

<div style="border: 1px solid #aaa; width: 400px; padding: 10px;">
    Report By Date Range
    <form id="frm_expense_rpt" method="post" action="/expenses/results/bydate">
    <div>Start Date:
      <input type="text" id="start_dt" name="start_dt" value="${c.start_dt}" style="text-align: center; width: 90px;" />
      <a href="#" onclick="displayDatePicker('start_dt');"><img src="${url('/images/cal.gif')}" width="16" height="16" border="0" alt="Pick a date"></a>
    </div>
    <div>End Date:
      <input type="text" id="end_dt" name="end_dt" value="${c.end_dt}" style="text-align: center; width: 90px;" />
      <a href="#" onclick="displayDatePicker('end_dt');"><img src="${url('/images/cal.gif')}" width="16" height="16" border="0" alt="Pick a date"></a>
    </div>
    <div>
      Category:
      <select id="cat_id" name="cat_id" class="lookup" style="width: 250px" onchange="if (this.selectedIndex) GetVendors(this.value);">
        <option value="all">All Categories</option>
        %for category in categories:
          <option value="${category.id}" ${ShowSelect(category.id,c.cat_id)}>${category.cat_nm}</option>
        %endfor
      </select>
    </div>
    <div>
      Vendor:
      <select id="vend_id" name="vend_id" class="lookup" style="width: 250px">
        <option value="all">All Vendors</option>
        %for vendor in vendors:
          <option value="${vendor.id}" ${ShowSelect(vendor.id,c.vend_id)}>${vendor.vend_nm}</option>
        %endfor:
      </select>
    </div>
    <div align="center" style="padding-top: 10px;"><input type="submit" class="button" value="Generate Report"/></div>
    </form>
</div>

%if c.cat_id and c.vend_id:

<script type="text/javascript">
GetVendors(${c.cat_id});
</script>
%endif
