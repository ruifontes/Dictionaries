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
import os
import wx
import gui
from gui import guiHelper
import ui
import api
import urllib.request
# For update process
from . update import *
# Necessary For translation
from scriptHandler import script
import addonHandler
addonHandler.initTranslation()

#Global variables
filepath = os.path.join (os.path.dirname(__file__), "dictionaries") #Path of dictionaries folder

dict = {
	_("english-portuguese") : "ingles-portugues.txt",
	_("french-portuguese") : "frances-portugues.txt",
	_("german-portuguese") : "alemao-portugues.txt",
	_("italian-portuguese") : "italiano-portugues.txt",
	_("spanish-portuguese") : "espanhol-portugues.txt",
	_("portuguese-english") : "portugues-ingles.txt",
	_("portuguese-french") : "portugues-frances.txt",
	_("portuguese-german") : "portugues-alemao.txt",
	_("portuguese-italian") : "portugues-italiano.txt",
	_("portuguese-spanish") : "portugues-espanhol.txt",
	_("Englis (Concise Oxford dictionary)") : "azdictionary.txt",
	_("portuguese - meanings (in portuguese)") : "portugues-significados.txt",
	_("portuguese - synonyms (in portuguese)") : "portugues-sinomimos.txt",
	_("Chemical (in portuguese)") : "dicionario_de_quimica.txt",
	_("Medical (in portuguese)") : "dicionario_medico.txt",
	_("Philosophy by Nicola Abbagnano (in portuguese)") : "dicionario_de_filosofia.txt",
	_("Psychology by Raul Mesquita and  other (in portuguese)") : "dicionario_de_psicologia.txt",
	_("Spanish - RAE (in spanish)") : "diccionario-de-la-lengua-espanhola-rae.txt",
	_("Tecnical Informatic (in portuguese)") : "dicionario_tecnico_de_informatica.txt",
	_("Englis synonyms dictionary)") : "ingles-sinonimos.txt",
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
		#. Translators Dialog title
		title = _("Dictionaries")
		# Calling the update process...
		_MainWindows = Initialize()
		_MainWindows.start()

	#defining a script with decorator:
	@script(
		gesture="kb:Control+shift+F6",
		description= _("Main window to access several dictionaries"),
		category= _("Dictionaries")
	)
	def script_exp1(self, event):
		#Calling the class "MyDialog" to select the dictionary to use or to download more.
		gui.mainFrame._popupSettingsDialog(MyDialog)


class MyDialog(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		#. Translators Dialog title
		self.SetTitle(_("Dictionaries"))

		#Filter the dictionaries present on dicts folder
		global missingDicts, availableDictsList, dictList
		availableDictsList = os.listdir(filepath)
		missingDicts = []
		dictList = list(dict.keys())
		n = 0
		while n < len(dictList):
			if dict.get(dictList[n]) not in availableDictsList: # If true dict is not present...
				missingDicts.append(dictList[n]) # Join to missing dicts list...
				del dictList[n] # Delete from available dicts list
				n -= 1 # To allow to check all dicts since we have deleted the item with number n...
			n += 1

		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		#. Translators StaticText with instructions for the user:
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

		#. Translators Button to allow the download of more dictionmaries
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

		self.Bind(wx.EVT_BUTTON, self.allButtons, self.button_1)
		self.Bind(wx.EVT_BUTTON, self.downloadMore, self.button_2)

	def allButtons(self, event):
		global dictToUse, wordToSearch, ourLine
		event.Skip()
		dictToUse = choice_1.GetStringSelection() # Get the selected dictionary
		var3 = os.path.join(filepath, dict.get(choice_1.GetStringSelection())) # Get the path of selected dictionary
		#. Translators Asking user to enter the text to search
		wordToSearch = "€" + wx.GetTextFromUser(_("Enter the word or expression to search for:"), _("Dictionaries"))
		with open(var3, "r", encoding = "UTF-8") as f: # Open the selected dictionary file
			ourLine = f.readline()  # Reads the first line where it is the length of the file
			totalLines = int(ourLine)   # convverts to a numerical value
			x = 0 # Line counter
			ourLine = ""
			while not ourLine.startswith(wordToSearch.lower()) and x<totalLines: #Read all lines untill find our word or get to file end
				x += 1 # Counter increment
				ourLine = f.readline().lower() # When the line starts with our word ends the search
			if x==totalLines:  # Found the end of file and the word do not exists...
				#. Translators message informing the word do not exist
				if gui.messageBox(
					_("%s not found in the dictionary of %s.\n") %(wordToSearch[1:], dictToUse)+
					"\n"+_("Do you want to search another word?"),
					caption = _("Dictionaries"),
					style = wx.YES | wx.NO) == wx.YES:
					MyDialog.allButtons(self, event)
				else:
					return
			else:  # If the word was found, lets get the meaning.
				line1 = ""
				while "---" not in line1 and x<totalLines: # Get all lines untill find "---" or at the end of file
					x += 1 # increment the counter to start in next line
					line1 = f.readline(x)
					if "---" not in line1: # When false end of cycle
						ourLine = ourLine + line1 # As it is not the end of the definition, add to variable
				y = len(wordToSearch) # To remove the desired word of the first line
				ourLine = ourLine[y:].strip() # To clean the string for garbage in begining and ending
				# Call the window showing the results
				gui.mainFrame._popupSettingsDialog(MyDialog1)

	def downloadMore(self, event):
		event.Skip()
		#self.Destroy()
		# Calling the download window
		gui.mainFrame._popupSettingsDialog(MyDialog2)


class MyDialog1(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		#. Translators Dialog title
		self.SetTitle(_("Dictionaries"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		#. Translators Static text announcing the results
		label_1 = wx.StaticText(self, wx.ID_ANY, _("Here is the meaning of %s in the dictionary %s:") %(wordToSearch[1:], dictToUse))
		sizer_1.Add(label_1, 0, 0, 0)

		self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, ourLine, size = (550, 300), style=wx.TE_MULTILINE | wx.TE_READONLY)
		self.text_ctrl_1.SetFocus()
		sizer_1.Add(self.text_ctrl_1, 0, 0, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		#. Translators Name of button to perform another search
		self.button_1 = wx.Button(self, wx.ID_ANY, _("Search again"))
		self.button_1.SetDefault()
		sizer_2.Add(self.button_1, 0, 0, 0)

		#. Translators Name of button that allows to copy results to clipboard
		self.button_SAVE = wx.Button(self, wx.ID_ANY, _("Copy to clipboard"))
		sizer_2.Add(self.button_SAVE, 0, 0, 0)

		self.button_CLOSE = wx.Button(self, wx.ID_CLOSE, "")
		sizer_2.AddButton(self.button_CLOSE)

		sizer_2.Realize()

		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetAffirmativeId(self.button_1.GetId())
		self.Bind(wx.EVT_BUTTON, self.searchAgain, self.button_1)
		self.SetEscapeId(self.button_CLOSE.GetId())
		self.Bind(wx.EVT_BUTTON, self.copyToClip, self.button_SAVE)

		self.Layout()
		self.CentreOnScreen()

	def searchAgain(self, event):
		event.Skip()
		# Calling the window to search another entry
		MyDialog.allButtons(self, event)

	def copyToClip(self, event):
		event.Skip()
		# Copy result to clipboard
		api.copyToClip(ourLine)


class MyDialog2(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		#. Translators Dialog title
		self.SetTitle(_("Dictionaries"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		#. Translators Asking user to choose the dictionary to download
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
		urlRepos = "https://www.tiflotecnia.net/dict/" # Online repository of dicts
		urlN = dict.get(self.choice_2.GetStringSelection()) # Get the file name of selected dictionary to download
		urlName = urlRepos + urlN # Complete URL of the dictionary file...
		file = os.path.join(filepath, urlN) # Complete path where to save the dictionary

		self.dialogActive = True
		#. Translators: Message dialog box asking confirmation to download
		if gui.messageBox(_("Are you sure you want to download the %s dictionary from %s?") %(self.choice_2.GetStringSelection(), urlName), _("Dictionaries"), style=wx.ICON_QUESTION|wx.YES_NO) == wx.YES:
			opener = urllib.request.build_opener()
			opener.addheaders = [('User-agent', 'Mozilla/5.0')]
			urllib.request.install_opener(opener)
			urllib.request.urlretrieve(urlName, file)
			ui.message(_("Downloading... Please wait..."))
		# Calling the main window to choose the dict to use or to download more
		gui.mainFrame._popupSettingsDialog(MyDialog)

	def quit(self, event):
		event.Skip()
		# Calling the main window to choose the dict to use or to download more
		gui.mainFrame._popupSettingsDialog(MyDialog)
