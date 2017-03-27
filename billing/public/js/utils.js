String.prototype.trim = function()
{
    return this.replace(/^\s*(\S*(\s+\S+)*)\s*$/, "$1");
};

String.prototype.capitalize = function()
{
    return this.substr(0,1).toUpperCase() + this.substr(1);
};

function Go(fn)
{
    window.location = fn;
}

function SetTitle(param)
{
    var std_txt = "Activus Billing";
    if (param == undefined)
    {
        var collection = document.getElementsByTagName('h1');
        if (collection.length > 0)
            document.title = collection[0].innerHTML.replace('&amp;','&').replace('.','') + std_txt;
        else
            document.title = std_txt;
    }
    else
        document.title = param + std_txt;
}

function AddOptions(sel, options)
{
  for (var key in options)
  {
    if (options.hasOwnProperty(key))
    {
      opt = document.createElement("option");
      opt.value = key;
      opt.innerHTML = options[key];
      sel.appendChild(opt);
    }
  }
}

function ClearSelect(sel)
{
    for(var j=sel.options.length-1; j >=0; j--)
        sel.remove(j);
}

function SetElementVisible(elementID, visible)
{
    var element = document.getElementById(elementID);

    switch (BrowserDetect.browser)
    {
        case 'Firefox':
            var setting = visible ? 'block' : 'none';
            element.setAttribute('style', 'display:' + setting);
            break;
        case 'MSIE':
            element.style.display = visible ? 'block' : 'none';
            document.all[elementID].style.visibility = visible ? 'visible' : 'hidden';
            break;
        case 'Netscape':
            element.style.display = visible ? 'block' : 'none';
            document.layers[elementID].visibility = visible ? 'show' : 'hide';
            break;
        case 'Safari':
            var setting = visible ? 'block' : 'none';
            element.setAttribute('style', 'display:' + setting);
            break;
    }
}

function BuildQS(dict)
{
    var params = new Array();
    for (var key in dict)
        params.push(key + "=" + dict[key])
    return params.join("&")
}
