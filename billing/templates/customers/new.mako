<%doc>
========================================
    Template: customers/new.mako
    Author: Brian Wolf
    Date: 2009.12.31
========================================
</%doc>
<%inherit file="/customers/index.mako"/>

<%
  def ShowSelected(value1, value2):
    if value1 == value2:
      return 'selected'
    else:
      return ''

  def ShowChecked(value1, value2):
    if value1 is None or value2 is None:
      return ''
    elif value1 in value2:
      return 'checked'
    else:
      return ''
%>

##--------------------------------------------------------------------------------

<form id="frm_customer" method="post" action="/customers/save">
<input type="hidden" name="cust_id" value="${customer.id}"/>
<table>
    <tr>
        <td>Customer:</td>
        <td><input type="text" id="cust_nm" name="cust_nm" class="lookup" value="${customer.cust_nm}" style="width: 250px" maxlength="40"/></td>
    </tr>
    <tr>
        <td>Type:</td>
        <td>
          %for customer_type in customer_types:
            <div><input type="checkbox" id="cust_type_${customer.cust_type}" name="cust_type" value="${customer_type.cust_type}" ${ShowChecked(customer_type.cust_type,customer.cust_type)}>&nbsp;${customer_type.dscr}</div>
          %endfor
        </td>
    </tr>
    <tr>
        <td>Account ID:</td>
        <td><input type="text" id="account_id" name="account_id" class="lookup" value="${customer.account_id}" style="width: 70px" maxlength="9"/></td>
    </tr>
    <tr>
        <td>Processor:</td>
        <td>
          <select id="processor" name="processor" class="lookup">
            <option value="">Select...</option>
            %for processor in ('AXIA', 'GLOBAL'): ##,'TRANSFIRST','CONCORD'):
              <option value="${processor}" ${ShowSelected(customer.processor,processor)}>${processor}</option>
            %endfor
          </select>
        </td>
    </tr>
    <tr>
        <td>Status:</td>
        <td>
          <select id="status" name="status" class="lookup">
            <option value="1" ${ShowSelected(customer.status,True)}>Active</option>
            <option value="0" ${ShowSelected(customer.status,False)}>Inactive</option>
          </select>
        </td>
    </tr>
    <tr>
        <td>Rate:</td>
        <td><input type="text" id="rate" name="rate" value="${customer.rate}"/></td>
    </tr>
    <tr>
        <td>Abbreviation:</td>
        <td><input type="text" id="abrv" name="abrv" value="${customer.abrv}"/></td>
    </tr>
    <tr>
        <td align="center" colspan="2"><input type="submit" class="button" value="Save"/></td>
    </tr>
</table>
</form>
