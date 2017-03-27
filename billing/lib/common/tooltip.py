#----------------------------------------------------------------------
# Author:			Brian Wolf
# Date:			2008.10.29
# Module:			tooltip.py
# Description:		Provides support for tooltips using prototype.js
#
# Modifications:
#
#
#
#----------------------------------------------------------------------


#----------------------------------------------------------------------
# classes
#----------------------------------------------------------------------


class Tooltip:
	def __init__(self):
		pass

	def trigger(self, tt, a=None):
		if a:
			s = '<span id="tgr_%s" class="tooltip">%s</span>' % (tt, a)
		else:
			s = """<img id="tgr_%s" src="/images/info_icon.png" />""" % tt
		return s

	def tooltip(self, tt, title, content):

		s = '<div id="tt_%s" class="tooltip">' % tt
		s += '<div class="tooltip-title">%s</div>' % title
		s += '<div class="tooltip-content">%s</div>' % content
		s += '</div>'
		return s

	def js(self, tt, tags=False):
		s = "var tooltip_%s = new Tooltip('tgr_%s','tt_%s')" % (tt,tt,tt)
		if tags:
			s = '<script type="text/javascript">' + s + '</script>'
		return s
