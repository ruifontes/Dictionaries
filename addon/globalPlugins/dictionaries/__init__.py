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
# For update process
from . update import *
# Necessary For translation
from scriptHandler import script
import addonHandler
addonHandler.initTranslation()

#Global variables
filepath = os.path.join (os.path.dirname(__file__), "dictionaries")    #caminho da pasta dos dicionários
dict = {
	_("english-portuguese") : "inglês-português.TXT",
	_("french-portuguese") : "francês-português.txt",
	_("german-portuguese") : "alemão-português.txt",
	_("italian-portuguese") : "italiano-português.txt",
	_("spanish-portuguese") : "espanhol-português.txt",
	_("portuguese-english") : "português-inglês.txt",
	_("portuguese-french") : "português-francês.txt",
	_("portuguese-german") : "português-alemão.TXT",
	_("portuguese-italian") : "português-italiano.txt",
	_("portuguese-spanish") : "português-espanhol.txt",
	_("Englis (Concise Oxford dictionary)") : "azdictionary.txt",
	_("portuguese - meanings (in portuguese)") : "português-significados.txt",
	_("portuguese - synonyms (in portuguese)") : "português-sinómimos.txt",
	_("Chemical (in portuguese)") : "dicionário de química.txt",
	_("Medical (in portuguese)") : "Dicionário Médico.txt",
	_("Philosophy by Nicola Abbagnano (in portuguese)") : "Dicionário de Filosofia - Nicola Abbagnano.txt",
	_("Psychology by Raul Mesquita and  other (in portuguese)") : "dicionário de psicologia - Raul Mesquita e outro.txt"
}
dictList = list(dict.keys())


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# Creating the constructor of the newly created GlobalPlugin class.
	def __init__(self):
		# Call of the constructor of the parent class.
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		title = _("Dictionaries")
		_MainWindows = Initialize()
		_MainWindows.start()

	#defining a script with decorator:
	@script(
		gesture="kb:Control+shift+F6",
		description= _("LEARNING with NVDA"),
		category= _("Dictionaries")
	)
	def script_exp1(self, event):
		#To call the class "MyDialog":
		gui.mainFrame._popupSettingsDialog(MyDialog)


class MyDialog(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		#. Translators Dialog title
		self.SetTitle(_("Dictionaries"))

		#. Translators StaticText with instructions for the user:
		label_1 = wx.StaticText(self, wx.ID_ANY, _("Choose the dictionary and press Enter"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		self.choice_1 = wx.Choice(self, wx.ID_ANY, choices = dictList)
		self.choice_1.SetFocus()
		self.choice_1.SetSelection(0)
		sizer_1.Add(self.choice_1, 0, 0, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		self.button_OK = wx.Button(self, wx.ID_OK, "")
		self.button_OK.SetDefault()
		sizer_2.AddButton(self.button_OK)

		self.button_CANCEL = wx.Button(self, wx.ID_CANCEL, "")
		sizer_2.AddButton(self.button_CANCEL)

		sizer_2.Realize()

		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetAffirmativeId(self.button_OK.GetId())
		self.SetEscapeId(self.button_CANCEL.GetId())

		self.Layout()
		self.CentreOnScreen()

		self.Bind(wx.EVT_BUTTON, self.allButons, self.button_OK)

	def allButons(self, event):
		event.Skip()
		var3 = os.path.join(filepath, dict.get(self.choice_1.GetStringSelection())) # Get the path of selected dictionary
		#. Translators Asking user to enter the text to search
		wordToSearch = "€" + wx.GetTextFromUser(_("Enter the word or expression to search for:"), _("Dictionaries"))
		with open(var3, "r", encoding = "UTF-8") as f: # Open the selected dictionary file
			ourLine = f.readline()  # Reads the first line where it is the length of the file
			totalLines = int(ourLine)   # convverts to a numerical value
			x = 0 # Line counter
			ourLine = ""
			while not ourLine.startswith(wordToSearch) and x<totalLines: #Read all lines untill find our word or get to file end
				x += 1 # Counter increment
				ourLine = f.readline() # When the line starts with our word ends the search
			if x==totalLines:  # Found the end of file and the word do not exists...
				#. Translators message informing the word do not exist
				if gui.messageBox(
					_("%s not found in the dictionary of %s.\nPlease note that some dictionaries may have the terms first letter in uppercase or even the all word...\n") %(wordToSearch[1:], self.choice_1.GetStringSelection())+
					"\n"+_("Do you want to search another word?"),
					caption = _("Dictionaries"),
					style = wx.YES | wx.NO) == wx.YES:
					self.allButons(event)
				else:
					return
			else:  # If the word was found, lets get the meaning.
				line1 = ""
				while "---" not in line1 and x<totalLines: # Get all lines untill find "---" or at the end of file
					x += 1 # increment the counter to start in next line
					line1 = f.readline(x)
					if "---" not in line1: # When false end of cycle
						ourLine = ourLine + line1 # As it is not the end of the definition, add to variable
				x = len(wordToSearch) # To remove the desired word of the first line
				#. Translators Message with the meaning of the word searched.
				msgTitle = _("Here is the meaning of %s in the dictionary %s:") %(wordToSearch[1:], self.choice_1.GetStringSelection())
				ui.browseableMessage(ourLine[x:], title = msgTitle)
				api.copyToClip(ourLine[x:])
