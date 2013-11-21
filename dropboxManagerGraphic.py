#! usr/bin/python
# -*- coding: utf8 -*-
try:
	import Tkinter,tkFileDialog
	import os.path
	import webbrowser
	import logging
	from Tkinter import *
except ImportError as e:
	print str(e)

from dropboxManager import DropboxManager


class DropboxManagerGraphic(Frame, DropboxManager):
	
	def __init__(self, window):
		#create the frame
		Frame.__init__(self, window, width=600, height=500)
		DropboxManager.__init__(self)
		self.pack(expand = True ,fill = BOTH)
		title = Label(self, text="Dropbox Manager" , font=("Purisa",32)) #add the app title
		title.pack(pady = 25)
		self.logger.debug("start graphical app")


	def start(self):
		#draw the connection pannel
		messageTop = Label(self, text="Vous n'etes pas connecté à un compte Dropbox")
		messageTop.pack(pady = 10)
		boutonConnect = Button(self, text="Connectez vous", command=self.goToDropbox)
		boutonConnect.pack()
		messageCode = Label(self, text="Et recopiez le code ici :")
		messageCode.pack(pady = 10)
		self.input = StringVar()
		e = Entry(self, textvariable=self.input, width=40)
		e.pack(pady = 10)
		ok = Button(self, text="Ok", command=self.done)
		ok.pack(pady = 10)
		self.elements = [messageTop,boutonConnect,messageCode,e,ok]

	#when the user click on the connection button
	def goToDropbox(self):
		webbrowser.open_new(self.getConnectionUrl()) #Open the user web browser to the dropbox connection url
	
	#When the user click on the 
	def done(self):
		try :
			self.getClient(self.input.get())
			if not hasattr(self, 'client'):
				raise Exception("The app is not connected to a dropbox account")
			self.printMainMenu()
		except Exception, e:
			print str(e)


	#clear the frame and ask the user to upload a file
	def printMainMenu(self):
		self.clear()
		messageTop = Label(self, text="Vous etes connecte entant que : " + self.client.account_info()['display_name'])
		messageTop.pack(pady = 10)
		self.message = Label(self, text="Vous n'avez pas choisi de fichier à uploader.")
		self.message.pack(pady = 10)
		self.bouton_choose_file = Button(self, text="Choisir un fichier", command=self.choosePath)
		self.bouton_choose_file.pack(ipady = 20, ipadx = 20, pady = 20)
		self.elements = [messageTop, self.message, self.bouton_choose_file]

	#When the user want to upload a file
	def choosePath(self): #Ask him wich file to upload
		path = tkFileDialog.askopenfilename(title='Choose a file')
		if path != None:
			self.message["text"] = "Vous avez choisi d'uploader le fichier : " + os.path.basename(path)
			self.path = path
			self.bouton_choose_file.configure(command = self.uploadFileUI, text = "Envoyer le fichier")

	#When the user choosed a file to upload
	def uploadFileUI(self):
		if self.path != None:
			self.uploadFile(self.path) #upload it 
			self.message["text"] = "Votre fichier '{}' a bien ete envoyé".format(os.path.basename(self.path))
			self.bouton_choose_file.pack_forget()
			#ask him if he want to share it 
			bouton_go_home = Button(self, text="Retour a l'accueuil", command=self.printMainMenu) #if no, return to the main menu
			bouton_go_home.pack(ipady = 20, ipadx = 20, pady = 20)
			bouton_share = Button(self, text="Partager le fichier", command=self.printShareMenu)
			bouton_share.pack(ipady = 20, ipadx = 20, pady = 20)
			self.elements.append(bouton_go_home)
			self.elements.append(bouton_share)

	#When the user want to share the last upload file
	def printShareMenu(self):
		self.clear() #clear the frame
		if self.path != None: #ask him on wich mails he want to share it
			self.message = Label(self, text="A quels mails voulez vous partager '{}'  (séparez les par une ',')".format(os.path.basename(self.path)))
			self.message.pack(pady = 10)
			self.input = StringVar()
			e = Entry(self, textvariable=self.input, width=70)
			e.pack()
			ok = Button(self, text="Ok", command=self.doneMail)
			ok.pack()
			self.elements = [self.message,e,ok]

	#When the user specified mails to share the last uploded file
	def doneMail(self):
		self.clear()
		self.shareLastFile(self.input.get().split(","))#share the file to all of mails
		self.message = Label(self, text="Votre fichier '{}' a bien été partagé".format(os.path.basename(self.path)))
		self.message.pack(pady = 10)
		bouton_go_home = Button(self, text="Retour a l'accueil", command=self.printMainMenu) #ask to return to the main menu
		bouton_go_home.pack(ipady = 20, ipadx = 20, pady = 20)
		self.elements = [bouton_go_home, self.message]


	#clear the frame
	def clear(self):
		for element in self.elements:
			element.pack_forget()
		self.elements = []


if __name__ == "__main__":
	window = Tk() #create the window
	window.title("Dropbox Manager")
	window.geometry("600x500")
	manager = DropboxManagerGraphic(window) #create the frame and add it to the window
	manager.start()
	manager.mainloop()
	manager.destroy()