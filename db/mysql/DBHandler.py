
#-*- coding: utf-8 -*-

import sys
import os
file_path = (os.path.abspath(__file__))
sys.path.append(os.path.dirname(file_path) + "/../")

import MySQLdb
import lib.Logger as Logger

class DBHandler:
	def __init__(self):
		self.logger = Logger(logname='/var/log/houseData.log', loglevel=1, logger="houseDataLogger").getLogger()

	def get_db_conn(self, db_name, user_name, password):
		conn = None
		try:
			conn = MySQLdb.connect(host='localhost', user=user_name, passwd=password, db=db_name, port=3306, charset='utf8')
		except MySQLdb.Error, e:
			self.logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))


	def close_db_conn(self, conn):
		try:
			conn.close()
		except MySQLdb.Error, e:
			self.logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))

	def insert_single_record(self, conn, sql, values):
		try:
			cur = conn.cursor()
			n = cur.execute(sql, values)
			self.logger.info( "%d records have been inserted!" % n )
			conn.commit()
			cur.close()

		except MySQLdb.Error, e:
			self.logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))

	def insert_batch_record(self, conn, sql, values):
		try:
			cur = conn.cursor()
			n = cur.executemany(sql, values)
			self.logger.info("%d records have been inserted!" % n)
			conn.commit()
			cur.close()

		except MySQLdb.Error, e:
			self.logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))




