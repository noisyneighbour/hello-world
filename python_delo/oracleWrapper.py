import cx_Oracle, sys, os
import numpy as np
import datetime
import pandas as pd

class oracleWrapper(object):


	"""
	A class for handling db operations

		WHEN initializing an object, the required parameter is one of the predefined dictionary keys in the "connection_info" dictionary below!
		It is containing the information about different oracle connections {key:name, value: constring}
		"""

	connection_info = {
		"hidpro" : 'hidpro/hidpro@172.19.0.90:1521/tajfun.arso.sigov.si',
		"vodepro" : 'vode_pro/vode_pro@172.19.0.90:1521/tajfun.arso.sigov.si',
		"db_string_2" : 'user_name2/password2@172.19.0.90:1521/tajfun.arso.sigov.si',
	}

	def __init__(self, name):
		self.name = name
		print(self.name.lower())
		if self.name.lower() not in self.connection_info.keys():
				print("Unknown connection name. Make sure the given connection name is in the 'connection_info' dictionary. Terminating...")
				sys.exit()
		else:
				
				self.constring = self.connection_info[self.name].strip()
				self.db_connection = cx_Oracle.connect(self.constring)
				self.cursor = self.db_connection.cursor()				

	def execute(self, sqlstr):
		"""
		Use for anything other than select statements
		such as insert
		"""

		self.cursor.execute(sqlstr)

		self.db_connection.commit()

	def select(self, sqlstr):
		"""
		Use only for select statement
		"""

		self.cursor.execute(sqlstr)

		return self.cursor.fetchall()

	def close_connection(self):
      
		try:
		        self.cursor.close()
		        self.db_connection.close()
		        # print "Connection to the " + self.name + " closed succesfully."
		except cx_Oracle.Error:
		        print("WARNING: Couldn't close the connection to the " + self.name + ".")

