# -*- coding: utf-8 -*-
# globalPlugins\Dictionaries\__init__.py
# dictionaries
# written by Rui Fontes <rui.fontes@tiflotecnia.com>, Ângelo Abrantes <ampa4374@gmail.com> and Abel Passos do Nascimento Jr. <abel.passos@gmail.com>
# Provides quick access to several dictionaries.
# Shortcut: Control+shift+F6
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# import the necessary modules.
import globalPluginHandler
import core
import os
import wx
import gui
from gui import guiHelper
import ui
import api
import threading
import urllib.request
# For update process
from . update import *
# Necessary For translation
from scriptHandler import script
import addonHandler
addonHandler.initTranslation()

#Global variables
#Path of dictionaries folder
filepath = os.path.join (os.path.dirname(__file__), "dictionaries")

dict = {
	# Translators: Name of a dictionary
	_("english-portuguese") : "ingles-portugues.txt",
	# Translators: Name of a dictionary
	_("french-portuguese") : "frances-portugues.txt",
	# Translators: Name of a dictionary
	_("german-portuguese") : "alemao-portugues.txt",
	# Translators: Name of a dictionary
	_("italian-portuguese") : "italiano-portugues.txt",
	# Translators: Name of a dictionary
	_("spanish-portuguese") : "espanhol-portugues.txt",
	# Translators: Name of a dictionary
	_("portuguese-english") : "portugues-ingles.txt",
	# Translators: Name of a dictionary
	_("portuguese-french") : "portugues-frances.txt",
	# Translators: Name of a dictionary
	_("portuguese-german") : "portugues-alemao.txt",
	# Translators: Name of a dictionary
	_("portuguese-italian") : "portugues-italiano.txt",
	# Translators: Name of a dictionary
	_("portuguese-spanish") : "portugues-espanhol.txt",
	# Translators: Name of a dictionary
	_("Englis (Concise Oxford dictionary)") : "azdictionary.txt",
	# Translators: Name of a dictionary
	_("portuguese - meanings (in portuguese)") : "portugues-significados.txt",
	# Translators: Name of a dictionary
	_("portuguese - synonyms (in portuguese)") : "portugues-sinomimos.txt",
	# Translators: Name of a dictionary
	_("Chemical (in portuguese)") : "dicionario_de_quimica.txt",
	# Translators: Name of a dictionary
	_("Medical (in portuguese)") : "dicionario_medico.txt",
	# Translators: Name of a dictionary
	_("Philosophy by Nicola Abbagnano (in portuguese)") : "dicionario_de_filosofia.txt",
	# Translators: Name of a dictionary
	_("Psychology by Raul Mesquita and  other (in portuguese)") : "dicionario_de_psicologia.txt",
	# Translators: Name of a dictionary
	_("Spanish - RAE (in spanish)") : "diccionario-de-la-lengua-espanhola-rae.txt",
	# Translators: Name of a dictionary
	_("Tecnical Informatic (in portuguese)") : "dicionario_tecnico_de_informatica.txt",
	# Translators: Name of a dictionary
	_("Englis synonyms dictionary)") : "ingles-sinonimos.txt",
	# Translators: Name of a dictionary
	_("Englis Spanish)") : "ingles-espanhol.txt"
}

dictList = list(dict.keys())
missingDicts = []
availableDictsList = []
dictToUse = ""
wordToSearch = ""
ourLine = ""


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# Creating the constructor of the newly created GlobalPlugin class.
	def __init__(self):
		# Call of the constructor of the parent class.
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		# Avoid use in secure screens
		if globalVars.appArgs.secure:
			return
		# Translators: Dialog title
		title = _("Dictionaries")
		# To allow waiting end of network tasks
		core.postNvdaStartup.register(self.networkTasks)

	def networkTasks(self):
		# Calling the update process...
		_MainWindows = Initialize()
		_MainWindows.start()

	def terminate(self):
		core.postNvdaStartup.unregister(self.networkTasks)

	#defining a script with decorator:
	@script(
		gesture="kb:Control+shift+F6",
		# Translators: Message to be announced during Keyboard Help  
		description= _("Main window to access several dictionaries"),
		# For translators: Name of the section in "Input gestures" dialog.  
		category= _("Dictionaries")
	)
	def script_exp1(self, event):
		#Calling the class "MainWindow" to select the dictionary to use or to download more.
		gui.mainFrame._popupSettingsDialog(MainWindow)


class MainWindow(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		# Translators: Dialog title
		self.SetTitle(_("Dictionaries"))

		#Filter the dictionaries present on dicts folder
		global missingDicts, availableDictsList, dictList
		availableDictsList = os.listdir(filepath)
		missingDicts = []
		dictList = list(dict.keys())
		n = 0
		while n < len(dictList):
			# If true dict is not present...
			if dict.get(dictList[n]) not in availableDictsList:
				# False, so join to missing dicts list...
				missingDicts.append(dictList[n])
				# And delete from available dicts list
				del dictList[n]
				# To allow to check all dicts since we have deleted the item with number n...
				n -= 1
			n += 1

		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		# Translators: StaticText with instructions for the user:
		label_1 = wx.StaticText(self, wx.ID_ANY, _("Choose the dictionary and press Enter"))
		sizer_1.Add(label_1, 0, 0, 0)

		global choice_1
		choice_1 = wx.Choice(self, wx.ID_ANY, choices = dictList)
		choice_1.SetFocus()
		choice_1.SetSelection(0)
		sizer_1.Add(choice_1, 0, 0, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		self.button_1 = wx.Button(self, wx.ID_OK, "")
		self.button_1.SetDefault()
		sizer_2.Add(self.button_1, 0, 0, 0)

		# Translators: Button to allow the download of more dictionnaries
		self.button_2 = wx.Button(self, wx.ID_ANY, _("Download more..."))
		sizer_2.Add(self.button_2, 0, 0, 0)

		self.button_CANCEL = wx.Button(self, wx.ID_CANCEL, "")
		sizer_2.AddButton(self.button_CANCEL)

		sizer_2.Realize()
		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetAffirmativeId(self.button_1.GetId())
		self.SetAffirmativeId(self.button_2.GetId())
		self.SetEscapeId(self.button_CANCEL.GetId())

		self.Layout()
		self.CentreOnScreen()

		self.Bind(wx.EVT_BUTTON, self.searchWindow, self.button_1)
		self.Bind(wx.EVT_BUTTON, self.downloadMore, self.button_2)

	def searchWindow(self, event):
		self.Close()
		global dictToUse, wordToSearch, ourLine
		event.Skip()
		# Get the selected dictionary
		dictToUse = choice_1.GetStringSelection()
		# Get the path of selected dictionary
		selectedDict = os.path.join(filepath, dict.get(choice_1.GetStringSelection()))
		# Translators: Asking user to enter the text to search
		wordToSearch = "€" + wx.GetTextFromUser(_("Enter the word or expression to search for:"), _("Dictionaries"))
		# Open the selected dictionary file
		with open(selectedDict, "r", encoding = "UTF-8") as f:
			# Reads the first line where it is the length of the file
			ourLine = f.readline() 
			# convverts to a numerical value
			totalLines = int(ourLine)  
			x = 0
			ourLine = ""
			# Read all lines untill find our word or get to file end
			while not ourLine.startswith(wordToSearch.lower()) and x<totalLines:
				x += 1
				# When the line starts with our word ends the search
				ourLine = f.readline().lower()
			# Found the end of file and the word do not exists...
			if x==totalLines:
				if gui.messageBox(
					# Translators: message informing the word do not exist
					_("%s not found in the dictionary of %s.\n") %(wordToSearch[1:], dictToUse)+"\n"+
					# Translators: message asking user if he wants to search again
					_("Do you want to search another word?"),
					caption = _("Dictionaries"), style = wx.YES | wx.NO) == wx.YES:
					MainWindow.searchWindow(self, event)
				else:
					return
			# The word was found, lets get the meaning.
			else:
				line1 = ""
				# Get all lines untill find "---" or at the end of file
				while "---" not in line1 and x<totalLines:
					# increment the counter to start in next line
					x += 1
					line1 = f.readline(x)
					# When false end of cycle, and when True it is not the end of the definition, so add to variable
					if "---" not in line1:
						ourLine = ourLine + line1
				# To remove the desired word of the first line and to clean the text from garbage in begining and end...
				y = len(wordToSearch)
				ourLine = ourLine[y:].strip()
				# Call the window showing the results
				gui.mainFrame._popupSettingsDialog(ShowResults)

	def downloadMore(self, event):
		event.Skip()
		# Calling the download window
		gui.mainFrame._popupSettingsDialog(DictDownload)


class ShowResults(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		# Translators: Dialog title
		self.SetTitle(_("Dictionaries"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		# Translators: Static text announcing the results
		label_1 = wx.StaticText(self, wx.ID_ANY, _("Here is the meaning of %s in the dictionary %s:") %(wordToSearch[1:], dictToUse))
		sizer_1.Add(label_1, 0, 0, 0)

		self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, ourLine, size = (550, 300), style=wx.TE_MULTILINE | wx.TE_READONLY)
		sizer_1.Add(self.text_ctrl_1, 0, 0, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		# Translators: Name of button to perform another search
		self.button_1 = wx.Button(self, wx.ID_ANY, _("Search again"))
		self.button_1.SetDefault()
		sizer_2.Add(self.button_1, 0, 0, 0)

		# Translators: Name of button that allows to copy results to clipboard
		self.button_SAVE = wx.Button(self, wx.ID_ANY, _("Copy to clipboard"))
		sizer_2.Add(self.button_SAVE, 0, 0, 0)

		self.button_CLOSE = wx.Button(self, wx.ID_CLOSE, "")
		sizer_2.AddButton(self.button_CLOSE)

		sizer_2.Realize()

		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetAffirmativeId(self.button_1.GetId())
		self.SetEscapeId(self.button_CLOSE.GetId())
		self.Bind(wx.EVT_BUTTON, self.searchAgain, self.button_1)
		self.Bind(wx.EVT_BUTTON, self.copyToClip, self.button_SAVE)
		self.Bind(wx.EVT_BUTTON, self.quit, self.button_CLOSE)

		self.Layout()
		self.CentreOnScreen()

	def searchAgain(self, event):
		event.Skip()
		# Calling the window to search another entry
		MainWindow.searchWindow(self, event)

	def copyToClip(self, event):
		event.Skip()
		# Copy result to clipboard
		api.copyToClip(ourLine)

	def quit(self, event):
		event.Skip()
		# Calling the main window to choose the dict to use or to download more
		gui.mainFrame._popupSettingsDialog(MainWindow)


class DictDownload(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		# Translators: Dialog title
		self.SetTitle(_("Dictionaries"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		# Translators: Asking user to choose the dictionary to download
		label_1 = wx.StaticText(self, wx.ID_ANY, _("Choose the dictionary to download and press Enter"))
		sizer_1.Add(label_1, 0, 0, 0)

		self.choice_2 = wx.Choice(self, wx.ID_ANY, choices = missingDicts)
		self.choice_2.SetFocus()
		self.choice_2.SetSelection(0)
		sizer_1.Add(self.choice_2, 0, 0, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		self.button_1 = wx.Button(self, wx.ID_OK, "")
		self.button_1.SetDefault()
		sizer_2.AddButton(self.button_1)

		self.button_CANCEL = wx.Button(self, wx.ID_CANCEL, "")
		sizer_2.AddButton(self.button_CANCEL)

		sizer_2.Realize()

		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetAffirmativeId(self.button_1.GetId())
		self.SetEscapeId(self.button_CANCEL.GetId())

		self.Layout()
		self.CentreOnScreen()

		self.Bind(wx.EVT_BUTTON, self.download, self.button_1)
		self.Bind(wx.EVT_BUTTON, self.quit, self.button_CANCEL)

	def download(self, event):
		event.Skip()
		# Online repository of dicts
		urlRepos = "https://www.tiflotecnia.net/dict/"
		# Get the file name of selected dictionary to download
		urlN = dict.get(self.choice_2.GetStringSelection())
		# Complete URL of the dictionary file...
		urlName = urlRepos + urlN
		# Complete path where to save the dictionary
		file = os.path.join(filepath, urlN)

		self.dialogActive = True
		# Translators: Message dialog box asking confirmation to download
		if gui.messageBox(_("Are you sure you want to download the %s dictionary from %s?") %(self.choice_2.GetStringSelection(), urlName), _("Dictionaries"), style=wx.ICON_QUESTION|wx.YES_NO) == wx.YES:

			req = urllib.request.Request(urlName, headers={'User-Agent': 'Mozilla/5.0'})
			response = urllib.request.urlopen(req)
			fileContents = response.read()
			response.close()
			f = open(file, "wb")
			f.write(fileContents)
			f.close()
			# Translators: Asking to wait while downloading
			ui.message(_("Downloading... Please wait..."))
		# Calling the main window to choose the dict to use or to download more
		gui.mainFrame._popupSettingsDialog(MainWindow)

	def quit(self, event):
		event.Skip()
		# Calling the main window to choose the dict to use or to download more
		gui.mainFrame._popupSettingsDialog(MainWindow)
