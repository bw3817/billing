"""Provides the BaseController class for subclassing."""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from billing.model import meta


class BaseController(WSGIController):
    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        except UnicodeDecodeError,e:
            return "<html><head><title>Bogus Web Page</title></head><body><p>A UnicodeDecodeError has been encountered.</p></body></html>"
        finally:
            meta.Session.remove()
