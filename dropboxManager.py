#! usr/bin/python
# -*- coding: utf8 -*-
try:
	from abc import ABCMeta, abstractmethod
	import dropbox
except ImportError as e:
	print str(e)
import os.path
import smtplib
import logging
from logging.handlers import RotatingFileHandler

class DropboxManager(object):
	__metaclass__ = ABCMeta

	app_key = '252qoqj1ohaw1mg'
	app_secret = 'b454qxw784w19sw'
	mail_login = "projetpythonisen@gmail.com"
	mail_password = "testtest12"

	def __init__(self):

		#Add a logger for the app
		self.logger = logging.getLogger()
		#on met le niveau du logger à DEBUG, comme ça il écrit tout
		self.logger.setLevel(logging.DEBUG)
		 
		# création d'un formateur qui va ajouter le temps, le niveau
		# de chaque message quand on écrira un message dans le log
		formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
		# création d'un handler qui va rediriger une écriture du log vers
		# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
		file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
		# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
		# créé précédement et on ajoute ce handler au logger
		file_handler.setLevel(logging.DEBUG)
		file_handler.setFormatter(formatter)
		self.logger.addHandler(file_handler)
		self.logger.debug('Start the app')


	@abstractmethod
	def start(self):
		raise Exception("start() must be overriden")


	def getConnectionUrl(self):
		try:
			self.logger.debug("try to connect the app to dropbox")
			self.flow = dropbox.client.DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)
			self.logger.debug("the app is connected to dropbox")
		except Exception, e:
			self.logger.critical("Can't connect the app to dropbox : " + str(e))
		# Have the user sign in and authorize this token
		return self.flow.start() #return the url of dropbox.com for asking to connect

	
	#Connect this app to a dropbox account with the client code
	def getClient(self, code):
		try:
			self.logger.debug("try to connect to the client dropbox account")
			self.access_token, self.user_id = self.flow.finish(code)
			self.client = dropbox.client.DropboxClient(self.access_token)
			self.logger.debug("Connection to the client dropbox account success")
		except Exception, e: #if the connection failed 
			self.logger.warning("Connection to the client dropbox account FAILED : " + str(e))


	def uploadFile(self, path):
		self.logger.debug("Try to upload a file")
		#Check if the file exist
		if not os.path.isfile(path):
			self.logger.warning("it is not a file")
			raise Exception("Can't get the file")
		f = open(path) #get the file
		#Create a "dropboxManagerUploads" directory if not exist and upload the file
		self.lastUploadResponse =  self.client.put_file('/dropboxManagerUploads/'+os.path.basename(path), f) #keep the response of the last upload file
		self.logger.info("The file was uploaded ")

	def shareLastFile(self, emailList):
		self.logger.debug("try to share a file ")
		link = self.client.share(self.lastUploadResponse["path"]) #get the link of the last upload file with the response
		for mail in emailList : 
			self.shareLink(link, mail) #send email with the link at all of specified mails
		self.logger.info("The file was shared ")


	#Send a mail with a link of the dropbox file 
	def shareLink(self, link, email):
		sender = 'projetPythonM1@isen-lille.fr'
		receivers = email

		message = u"""From: Projet Python M1

Bonjour,
Un fichier dropbox vous a ete partage par : """+self.client.account_info()['display_name']+""" 
Vous pouvez le telecharger en cliquant sur ce lien : """ + link['url']

		server = smtplib.SMTP('smtp.gmail.com',587) #use the smtp server of google to send the mail 
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(self.mail_login, self.mail_password) #connect to our gmail account
		server.sendmail(sender, receivers, message)#send the mail 
