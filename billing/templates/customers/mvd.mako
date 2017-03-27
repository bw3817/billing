<%doc>
========================================
	Template: customers/mvd.mako
	Author: Brian Wolf
	Date: 2012.04.30
========================================
</%doc>
<%inherit file="/customers/index.mako"/>

##--------------------------------------------------------------------------------

<div><input type="file" id="spreadsheet"/></div>
<div><button type="button" onclick="Process()">Process</button></div>

<script type="text/javascript">
function Process()
{
	var spreadsheet = document.getElementById("spreadsheet");
	if (spreadsheet.value.trim() == "")
	{
		alert("Please select a spreadsheet to import.");
		return;
	}
	var url = "/ajax/getmvd?spreadsheet=" + spreadsheet.value;
	new Ajax.Request(url,
	{
	  method: 'get',
	  onSuccess: ShowStatus,
	  onFailure: function() {alert("There was an error with the connection.");}
	});
}

function ShowStatus(results)
{
	var json_data = results.responseText.evalJSON();
	var status = {0:"Unfortunately, spreadsheet data failed to import.", 1: "Spreadsheet data imported successfully."}
	alert(status[json_data.ok]);
}
</script>