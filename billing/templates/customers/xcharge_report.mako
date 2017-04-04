<%doc>
========================================
	Template: customers/xcharge_report.mako
	Author: Brian Wolf
	Date: 2010.03.07
========================================
</%doc>
<%inherit file="/customers/index.mako"/>

<%!
  from datetime import date
  from billing.lib.common.utils import Utils
%>

<%
  utils = Utils()

  mo = session['mo'] - 1
  yr = session['yr']
%>

##--------------------------------------------------------------------------------

<table style="margin-top: 20px;">
  <tr>
	<th class="colhdr" rowspan="2" style="vertical-align: top;">Year</td>
	<th class="colhdr" colspan="2">Volume</td>
	<th class="colhdr" colspan="2">Amount</td>
	<th class="colhdr" rowspan="2" style="vertical-align: top;">Count</td>
	<th class="colhdr" rowspan="2" style="vertical-align: top;">Ratio</td>
  </tr>
  <tr>
	<th class="colhdr">Total</td>
	<th class="colhdr">Mean</td>
	<th class="colhdr">Total</td>
	<th class="colhdr">Mean</td>
  </tr>
  %for bonus in bonuses:
  <tr>
	<td class="prompt">${bonus.yr}</td>
	<td class="data" style="text-align: right; padding: 5px;">${utils.fmt(bonus.sum_vol)}</td>
	<td class="data" style="text-align: right; padding: 5px;">${utils.fmt(bonus.avg_vol)}</td>
	<td class="data" style="text-align: right; padding: 5px;">${utils.fmt(bonus.sum_amt)}</td>
	<td class="data" style="text-align: right; padding: 5px;">${utils.fmt(bonus.avg_amt)}</td>
	<td class="data" style="text-align: center; padding: 5px;">
	  %if bonus.cnt > 0:
	    ${bonus.cnt}
	  %endif
	</td>
	<td class="data" style="text-align: right; padding: 5px;">
	  %if bonus.sum_amt is not None and bonus.sum_vol is not None:
	    ${utils.fmt(1000 * bonus.sum_amt / bonus.sum_vol)}
	  %endif
	</td>
  </tr>
  %endfor
<table>
