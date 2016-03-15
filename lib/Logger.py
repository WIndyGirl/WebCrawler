import logging

class Logger:
	'''
	specify the path of log file, log setLevel
	save log to the specified file
	'''
	def __init__(self, logname, loglevel, logger):
		# create logger
		self.logger = logging.getLogger(logger)
		self.logger.setLevel(logging.DEBUG)

		# create handler to write log to file
		fh = logging.FileHandler(logname)
		fh.setLevel(logging.DEBUG)

		# create handler to write log to console
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)

		# define the handler format
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		# # save log format in dict
		# format_dict = {
		#    1 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
		#    2 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
		#    3 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
		#    4 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
		#    5 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		# }

		# formatter = format_dict[int(loglevel)]
		fh.setFormatter(formatter)
		ch.setFormatter(formatter)

		# add handler to logger
		self.logger.addHandler(fh)
		# self.logger.addHandler(ch)

	def getLogger(self):
		return self.logger
