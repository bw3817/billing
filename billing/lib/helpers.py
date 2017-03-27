"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
from webhelpers.html import literal
from webhelpers.pylonslib import Flash as _Flash
flash = _Flash()

"""
def verify_https(request):
	if not request.params.get('https') == 'on':
		params = ['%s=%s' % (k,v) for (k,v) in request.params.items() if k! = 'https']
		params.append('https=on')
		redirect_to(str(request.environ['PATH_INFO']+'?'+'&'.join(params)))
"""
