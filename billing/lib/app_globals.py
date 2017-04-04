from pylons import config


class Globals(object):
	"""Globals acts as a container for objects available throughout the life of the application"""

	def __init__(self):
		"""One instance of Globals is created during application
		initialization and is available during requests via the
		'app_globals' variable"""
		##self.pdfdocs_dir = config['billing.pdfdocs_dir']
		##self.zipfiles_dir = config['billing.zipfiles_dir']
