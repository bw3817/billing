"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper


def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'], always_scan=config['debug'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{cust_id}', controller='error')

    # CUSTOM ROUTES HERE
    map.connect('home','/home', controller='site', action='home')
    map.connect('/', controller='site', action='home')
    #
    map.connect('/categories/{action}/{cat_id}', controller='categories')
    #
    map.connect('/revenues/edit/{rev_id}', controller='revenues', action='edit')
    map.connect('/revenues/view/{rev_id}', controller='revenues', action='view')
    #
    map.connect('/expenses/edit/{exp_id}', controller='expenses', action='edit')
    map.connect('/expenses/view/{exp_id}', controller='expenses', action='view')
    map.connect('/expenses/eoy/{yr}', controller='expenses', action='eoy')
    map.connect('/expenses/report', controller='expenses', action='report')
    #
    map.connect('/vendors/edit/{vend_id}', controller='vendors', action='edit')
    map.connect('/vendors/view/{vend_id}', controller='vendors', action='view')
    #
    map.connect('/customers/view/{cust_id}', controller='customers', action='view')
    map.connect('/customers/edit/{cust_id}', controller='customers', action='edit')
    map.connect('/customers/xcharge/setmonth', controller='customers', action='xcharge', xaction='setmonth')
    map.connect('/customers/xcharge/view', controller='customers', action='xcharge', xaction='view')
    map.connect('/customers/xcharge/report', controller='customers', action='xcharge', xaction='report')
    map.connect('/customers/xcharge/add/{id}', controller='customers', action='xcharge', xaction='add')
    map.connect('/customers/xcharge/edit/{id}', controller='customers', action='xcharge', xaction='edit')
    map.connect('/customers/xcharge/mvd', controller='customers', action='xcharge', xaction='mvd')
    map.connect('/{controller}/find/{letter}', action='find')
    map.connect('/ajax/vendors_per_category/{cat_id}', controller='ajax', action='vendors_per_category')
    map.connect('/ajax/getmvd', controller='ajax', action='getmvd')
    #
    map.connect('/projects/manage', controller='invoices', action='projects_manage')
    map.connect('/projects/add', controller='invoices', action='projects_add')
    map.connect('/projects/add/save', controller='invoices', action='projects_add_save')
    map.connect('/projects/manage/save', controller='invoices', action='projects_manage_save')
    map.connect('/projects/find', controller='invoices', action='projects_find')
    #
    map.connect('/hours', controller='invoices', action='hours_show')
    map.connect('/hours/show', controller='invoices', action='hours_show')
    map.connect('/hours/add', controller='invoices', action='hours_add')
    map.connect('/hours/edit', controller='invoices', action='hours_edit')
    map.connect('/hours/view', controller='invoices', action='hours_view')
    map.connect('/hours/find', controller='invoices', action='hours_find')
    map.connect('/hours/save', controller='invoices', action='hours_save')
    map.connect('/hours/setbilled', controller='invoices', action='setbilled')
    map.connect('/hours/setpaid', controller='invoices', action='setpaid')
    map.connect('/hours/update', controller='invoices', action='hours_update')
    #
    map.connect('/items', controller='invoices', action='items_show')
    map.connect('/items/show', controller='invoices', action='items_show')
    map.connect('/items/add', controller='invoices', action='items_add')
    map.connect('/items/edit', controller='invoices', action='items_edit')
    map.connect('/items/view', controller='invoices', action='items_view')
    map.connect('/items/find', controller='invoices', action='items_find')
    map.connect('/items/save', controller='invoices', action='items_save')
    #
    map.connect('invoice_generate', '/invoices/generate', controller='invoices', action='invoice_generate')
    #
    map.connect('', controller='site', action='index')
    map.connect('/{controller}', controller='site', action='index')
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')
    map.connect('/site/{placeholder}', controller='site', action='error')
    return map
