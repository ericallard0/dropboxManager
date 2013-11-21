#! usr/bin/python
# -*- coding: utf8 -*-

import logging
from dropboxManager import DropboxManager

class DropboxManagerText(DropboxManager):

	
	def __init__(self):
		DropboxManager.__init__(self)
		# add a handler for looging for the console
		steam_handler = logging.StreamHandler()
		steam_handler.setLevel(logging.INFO)
		self.logger.addHandler(steam_handler)
		self.logger.debug("start text app")

	#Connect To the dropbox account
	def connectDropbox(self):
		code = self.askClientConnection() #get the user code 
		if code == None :
			raise Exception("askClientConnection() must return the connection code")
		try :
			self.getClient(code)#connect to the user dropbox account 
		except Exception, e:
			self.logger.warning("can't connect to the user dropbox account : " + str(e))

	def askClientConnection(self):
		url = self.getConnectionUrl() #get the url to connect at the dropbox account
		print '1. Go to: ' + url
		print '2. Click "Allow" (you might have to log in first)'
		print '3. Copy the authorization code.'
		return raw_input("Enter the authorization code here: ").strip() #get the user dropbox account login code for the app


	def start(self):
		#while the app is not connected to dropbox ask the user to connect to his account 
		while not hasattr(self, 'client') :
			self.connectDropbox()  #connect to the user dropbox account

		print 
		print "---------------- Dropbox Manager ---------------- "
		print 
		key = ""
		#if the user type 'q' we stop the app
		while not key == "q" :
			print
			key = raw_input("Type 'u' to upload file or 'q' to quit this app :").strip()
			#If the user want to upload a file
			if key == "u" :
				print
				path = raw_input("Type the path of your file :").strip()
				try :
					self.uploadFile(path)
				except Exception, e:
		   			self.logger.info("The upload failed : " + str(e))
	   			#ask if the user want to share the file
	   			while key != "yes" and key !="no" and key != "q":
					key = raw_input("Do you want to share this file ? (yes/no) :").strip()
				#If the user want to share the file	
				if key == "yes" :
					print
					#ask on wich mail he want to share this file
					mails = raw_input("Type on wich mails you want to share this file (separate by using a ',' ):").strip()
					try :
						#send a mail at all of mails 
						self.shareLastFile(mails.split(",")) #create a list of mails 
					except Exception, e:
		   				self.logger.info("The share failed : " + str(e))
			   			
			print "          	------------------------"


if __name__ == "__main__":
	manager = DropboxManagerText()
	manager.start()