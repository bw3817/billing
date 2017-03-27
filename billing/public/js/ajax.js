var httpreq;

function SendRequest(url)
{
	// send request
	httpreq = GetXmlHttpObject();
	httpreq.open("GET", url, true);
	httpreq.onreadystatechange = HandleRequest;
	httpreq.send(null);
}

function HandleRequest()
{
	if (httpreq.readyState==4 || httpreq.readyState=="complete")
		ProcessResults(httpreq.responseText);
}

function GetXmlHttpObject()
{
	var httpreq = null;
	try
	{
		// Firefox, Opera 8.0+, Safari
		httpreq = new XMLHttpRequest();
	}
	catch (e)
	{
		// Internet Explorer
		try
		{
			httpreq = new ActiveXObject("Msxml2.XMLHTTP");
		}
		catch (e)
		{
			httpreq = new ActiveXObject("Microsoft.XMLHTTP");
		}
	}
	return httpreq;
}
