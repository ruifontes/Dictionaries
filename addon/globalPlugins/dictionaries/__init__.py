# -*- coding: utf-8 -*-
# dictionaries add-on
# Provides quick access to several dictionaries.
# Shortcut: Control+shift+F6
# written by Rui Fontes <rui.fontes@tiflotecnia.com>, Ângelo Abrantes <ampa4374@gmail.com> and Abel Passos do Nascimento Jr. <abel.passos@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# import the necessary modules.
import globalPluginHandler
import core
import api
import os
import wx
import gui
import ui
from . import sqlite3
import threading
import urllib.request
# For update process
from .update import *
import time
# Necessary For translation
from scriptHandler import script
import addonHandler
addonHandler.initTranslation()

#Global variables
#Path of dictionaries folder
filepath = os.path.join (os.path.dirname(__file__), "dicionarios")
dictToUse = ""
dictToDownload = ""
dict = {
	# Translators: Name of a dictionary
	_("Dutch-French") : "neerlandes-frances.db",
	# Translators: Name of a dictionary
	_("English-French") : "ingles-frances.db",
	# Translators: Name of a dictionary
	_("English-Italian") : "inglese-italiano.db",
	# Translators: Name of a dictionary
	_("English-Portuguese") : "ingles-portugues.db",
	# Translators: Name of a dictionary
	_("English-Spanish") : "ingles-espanhol.db",
	# Translators: Name of a dictionary
	_("French-Arabic") : "frances-arabe.db",
	# Translators: Name of a dictionary
	_("French-Dutch") : "frances-neerlandes.db",
	# Translators: Name of a dictionary
	_("French-English") : "frances-ingles.db",
	# Translators: Name of a dictionary
	_("French-German") : "frances-alemao.db",
	# Translators: Name of a dictionary
	_("French-Italian") : "frances-italiano.db",
	# Translators: Name of a dictionary
	_("French-Portuguese") : "frances-portugues.db",
	# Translators: Name of a dictionary
	_("french-Spanish") : "frances-espanhol.db",
	# Translators: Name of a dictionary
	_("German-French") : "alemao-frances.db",
	# Translators: Name of a dictionary
	_("German-Portuguese") : "alemao-portugues.db",
	# Translators: Name of a dictionary
	_("Icelandic-French") : "islandes-frances.db",
	# Translators: Name of a dictionary
	_("Italian-English") : "italiano-inglese.db",
	# Translators: Name of a dictionary
	_("Italian-French") : "italiano-frances.db",
	# Translators: Name of a dictionary
	_("Italian-Portuguese") : "italiano-portugues.db",
	# Translators: Name of a dictionary
	_("Portuguese-English") : "portugues-ingles.db",
	# Translators: Name of a dictionary
	_("Portuguese-French") : "portugues-frances.db",
	# Translators: Name of a dictionary
	_("Portuguese-German") : "portugues-alemao.db",
	# Translators: Name of a dictionary
	_("Portuguese-Italian") : "portugues-italiano.db",
	# Translators: Name of a dictionary
	_("Portuguese-Spanish") : "portugues-espanhol.db",
	# Translators: Name of a dictionary
	_("Spanish-French") : "espanhol-frances.db",
	# Translators: Name of a dictionary
	_("Spanish-Portuguese") : "espanhol-portugues.db",
	# Translators: Name of a dictionary
	_("English (Concise Oxford dictionary)") : "azdictionary.db",
	# Translators: Name of a dictionary
	_("English synonyms dictionary)") : "ingles-sinonimos.db",
	# Translators: Name of a dictionary
	_("French common nouns with new ortography (in french)") : "frances-significados-nao-comuns(nova-ortografia).db",
	# Translators: Name of a dictionary
	_("French common nouns (in french)") : "frances-significados-nao-comuns.db",
	# Translators: Name of a dictionary
	_("French encyclopedie (in french)") : "Encyclopedie.db",
	# Translators: Name of a dictionary
	_("French proper nouns (in french)") : "frances-nomes-proprios.db",
	# Translators: Name of a dictionary
	_("French synonyms (in French)") : "frances-sinonimos.db",
		# Translators: Name of a dictionary
	_("Portuguese language difficulties (in portuguese)") : "Dicionario-de-dificuldades-da-lingua-portuguesa.db",
	# Translators: Name of a dictionary
	_("Portuguese - meanings (in portuguese)") : "grande-dicionario-portugues.db",
	# Translators: Name of a dictionary
	_("Portuguese - synonyms (in portuguese)") : "portugues-sinomimos.db",
	# Translators: Name of a dictionary
	_("Spanish - RAE (in spanish)") : "diccionario-de-la-lengua-espanhola-rae.db",
	# Translators: Name of a dictionary
	_("Spanish - RAE New version (in spanish)") : "Diccionario_de_la_Lengua_Espanhola-RAE2.db",
	# Translators: Name of a dictionary
	_("Alchemy (in portuguese)") : "Dicionario_Alquimico.db",
	# Translators: Name of a dictionary
	_("Botany (in portuguese)") : "Glossario-de-Botanica.db",
	# Translators: Name of a dictionary
	_("Chemical (in portuguese)") : "dicionario-de-quimica.db",
	# Translators: Name of a dictionary
	_("Clinical Practice (in portuguese)") : "Terminologia-pratica-clinica.db",
	# Translators: Name of a dictionary
	_("Finantial terms (in portuguese pt_br)") : "Glossario_financeiro(InfoMoney).db",
	# Translators: Name of a dictionary
	_("Finantial terms (in portuguese pt_pt)") : "Glossario_300611.db",
	# Translators: Name of a dictionary
	_("Geography and surroundings (in portuguese)") : "glossario-de-geografia.db",
	# Translators: Name of a dictionary
	_("Geology (in portuguese)") : "Glossario-de-Geologia.db",
	# Translators: Name of a dictionary
	_("Health (in portuguese)") : "Dicionario_Ilustrado_de_Saude.db",
	# Translators: Name of a dictionary
	_("Historical concepts (in portuguese)") : "dicionario-de-conceitos-historicos.db",
	# Translators: Name of a dictionary
	_("Information society (in portuguese)") : "GLOSSARIO-SOCIEDADE-INFORMACAO.db",
	# Translators: Name of a dictionary
	_("Law glossary (in portuguese pt_pt)") : "Glossario_juridico-OA.db",
	# Translators: Name of a dictionary
	_("Mathematic elementar (in portuguese)") : "glossario-elementar-de-matematica.db",
	# Translators: Name of a dictionary
	_("Medical (in french)") : "dicionario-medico(frances).db",
	# Translators: Name of a dictionary
	_("Medical popular (in portuguese)") : "dicionario-medico.db",
	# Translators: Name of a dictionary
	_("Medical technical (in portuguese)") : "Dicionario_Medico_Pro.db",
	# Translators: Name of a dictionary
	_("Nursing (in portuguese)") : "Termos_tecnicos_de_enfermagem_mais_usados.db",
	# Translators: Name of a dictionary
	_("Philosophy (Cambridge)") : "cambridge-dictionary-of-philosophy.db",
	# Translators: Name of a dictionary
	_("Philosophy (in portuguese)") : "dicionario-de-filosofia.db",
	# Translators: Name of a dictionary
	_("Phonetics (in spanish)") : "diccionario_fonetico(espanhol).db",
	# Translators: Name of a dictionary
	_("Politic (in portuguese)") : "dicionario-de-politica.db",
	# Translators: Name of a dictionary
	_("Psychology (in portuguese)") : "dicionario-de-psicologia.db",
		# Translators: Name of a dictionary
	_("Tecnical of Informatic (english-french)") : "informatica-ingles-frances.db",
	# Translators: Name of a dictionary
	_("Tecnical of Informatic (in portuguese)") : "dicionario-tecnico-de-informatica.db",
	# Translators: Name of a dictionary
	_("Veterinary medicin (in portuese)") : "Dicionario_Medicina_Veterinaria.db",
}

totalDictList = list(dict.keys())
thematics = [
	"Dicionario-de-dificuldades-da-lingua-portuguesa.db",
	"Dicionario_Alquimico.db",
	"Glossario-de-Botanica.db",
	"Terminologia-pratica-clinica.db",
	"dicionario-de-quimica.db",
	"Glossario_financeiro(InfoMoney).db",
	"Glossario_300611.db",
	"glossario-de-geografia.db",
	"Dicionario_Ilustrado_de_Saude.db",
	"dicionario-de-conceitos-historicos.db",
	"GLOSSARIO-SOCIEDADE-INFORMACAO.db",
	"Glossario_juridico-OA.db",
	"glossario-elementar-de-matematica.db",
	"dicionario-medico(frances).db",
	"dicionario-medico.db",
	"Termos_tecnicos_de_enfermagem_mais_usados.db",
	"cambridge-dictionary-of-philosophy.db",
	"dicionario-de-filosofia.db",
	"diccionario_fonetico(espanhol).db",
	"dicionario-de-politica.db",
	"dicionario-de-psicologia.db",
	"informatica-ingles-frances.db",
	"dicionario-tecnico-de-informatica.db",
		"Dicionario_Medicina_Veterinaria.db"
]

missingDicts = []
availableDictsList = []
dictToUse = ""
selectedDict = ""
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
		category= _("Dictionaries"))
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
		global missingDicts, availableDictsList, dictList, selectedDict
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

		self.Bind(wx.EVT_BUTTON, self.searchWindow, self.button_1)
		self.Bind(wx.EVT_BUTTON, self.downloadMore, self.button_2)
		self.Bind(wx.EVT_BUTTON, self.quit, self.button_CANCEL)

		self.Layout()
		self.CentreOnScreen()

	def searchWindow(self, event):
		self.Close()
		event.Skip()
		global dictToUse, selectedDict
		# Get the path of selected dictionary
		dictToUse = os.path.join(filepath, dict.get(choice_1.GetStringSelection()))
		# Get the name of the dict to use
		selectedDict = dict.get(choice_1.GetStringSelection())
		# We have the dict, so call the search window
		gui.mainFrame._popupSettingsDialog(SearchWindow)

	def downloadMore(self, event):
		self.Close()
		event.Skip()
		# Calling the download window
		gui.mainFrame._popupSettingsDialog(DictDownload)

	def quit(self, event):
		self.Close()
		event.Skip()


class SearchWindow(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		self.SetTitle(_("Dictionaries"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		# Choose what to ask the user...
		if selectedDict in thematics:
			# For translators: Choose a term from list to search
			label_1 = wx.StaticText(self, wx.ID_ANY, _("Select what to search  from the list."))
			sizer_1.Add(label_1, 0, 0, 0)
		else:
			# For translators: Asking to enter a letter, word or expression to search
			label_1 = wx.StaticText(self, wx.ID_ANY, _("Enter the first letter, a word or an expression to search."))
			sizer_1.Add(label_1, 0, 0, 0)

		# Selecting what to present to the user, text entry field or a index list
		if selectedDict not in thematics:
			self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, "")
			self.text_ctrl_1.SetFocus()
			sizer_1.Add(self.text_ctrl_1, 0, 0, 0)
		else:
			self.list_ctrl_1 = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES)
			sizer_1.Add(self.list_ctrl_1, 1, wx.EXPAND, 0)

			# Get the index with all entries
			# Open the selected dictionary file
			self.dbDict = sqlite3.connect(dictToUse, check_same_thread=False)
			self.dbCursor = self.dbDict.cursor()
			# Select all itens from the data base
			self.dbCursor.execute("select verbete from dicionario")
			occurs = self.dbCursor.fetchall()
			self.dbDict.close()
			ui.message(_("Please wait untill the index is created..."))
			# Cleaning the list and inserting one column to hold the itens
			self.list_ctrl_1.ClearAll()
			self.list_ctrl_1.InsertColumn(0, "Verbetes")
			# Now, inserting all itens
			i=0
			for dbRow  in occurs:
				self.list_ctrl_1.InsertItem(i, dbRow[0])
				i+=1
			# Select and focusing first item
			self.list_ctrl_1.Focus(0)
			self.list_ctrl_1.Select(0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		self.button_OK = wx.Button(self, wx.ID_OK, "")
		self.button_OK.SetDefault()
		sizer_2.AddButton(self.button_OK)

		self.button_CLOSE = wx.Button(self, wx.ID_CLOSE, "")
		sizer_2.AddButton(self.button_CLOSE)

		sizer_2.Realize()

		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetAffirmativeId(self.button_OK.GetId())
		self.SetEscapeId(self.button_CLOSE.GetId())

		self.Bind(wx.EVT_BUTTON, self.performSearch, self.button_OK)
		self.Bind(wx.EVT_BUTTON, self.quit, self.button_CLOSE)
		# If we present a list, allow to press Enter on the list...
		if selectedDict in thematics:
			self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.performSearch, self.list_ctrl_1)

		self.Layout()
		self.CentreOnScreen()

	def performSearch(self, event):
		self.Close()
		event.Skip()
		global wordToSearch, ourLine
		# Define what to search
		if selectedDict in thematics:
			wordToSearch = self.list_ctrl_1.GetItemText(self.list_ctrl_1.GetFocusedItem())
		else:
			wordToSearch = self.text_ctrl_1.GetValue()
		if selectedDict in thematics:
			# Open the selected dictionary file
			self.dbDict = sqlite3.connect(dictToUse, check_same_thread=False)
			self.dbCursor = self.dbDict.cursor()
			self.dbCursor.execute("select descricao	 from dicionario where verbete=:word", {"word": wordToSearch})
			# We only have an entry, so get it...
			ourLine = self.dbCursor.fetchone()
			self.dbDict.close()
			# Call the window showing the results
			gui.mainFrame._popupSettingsDialog(ShowResults)
		else:
			# Call the window showing the index
			gui.mainFrame._popupSettingsDialog(IndexWindow)

	def quit(self, event):
		self.Close()
		event.Skip()


class IndexWindow(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		self.SetTitle(_("Dictionaries"))
		global wordToSearch, ourLine

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		# For translators: Asking to choose what to search
		label_1 = wx.StaticText(self, wx.ID_ANY, _("Select what to search  from the list."))
		sizer_1.Add(label_1, 0, 0, 0)

		self.list_ctrl_1 = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES | wx.LC_SORT_ASCENDING)
		sizer_1.Add(self.list_ctrl_1, 1, wx.EXPAND, 0)

		# Preparing the pattern to search in data base
		wordToSearch1 = "'" + wordToSearch + "%'"
		# Open the selected dictionary file
		self.dbDict = sqlite3.connect(dictToUse, check_same_thread=False)
		self.dbCursor = self.dbDict.cursor()
		self.dbCursor.execute("select verbete from dicionario where upper(verbete) like " + wordToSearch1)
		# Get all entries matching the search query
		occurs = self.dbCursor.fetchall()
		#self.dbDict.close()
		# Check how many occurrences...
		if len(occurs) == 1:
			# There are only one result, so gave immediatly the result and not a one element list...
			# First pair of brackets to gave the first item of tupple and second pair to gave us only the expression to search...
			wordToSearch1 = occurs[0][0]
			self.dbCursor.execute("select descricao	 from dicionario where verbete=:word", {"word": wordToSearch1})
			ourLine = self.dbCursor.fetchone()
			self.dbDict.close()
			# To destroy the window in construction because it is unnecessary...
			self.Destroy()
			# Calling the show results window
			gui.mainFrame._popupSettingsDialog(ShowResults)
		elif len(occurs) >=2:
			# There are several items to choose from, so show a list of them...
			self.list_ctrl_1.ClearAll()
			self.list_ctrl_1.InsertColumn(0, "Verbetes")
			i=0
			for dbRow  in occurs:
				self.list_ctrl_1.InsertItem(i, dbRow[0])
				i+=1
			self.list_ctrl_1.Focus(0)
			self.list_ctrl_1.Select(0)
			self.dbDict.close()
		else:
			# No item was found, so ask user if wants to search again...
			self.dbDict.close()
			# To destroy the window in construction because it is unnecessary...
			self.Destroy()
			# Call a window to ask if user wants to search again...
			gui.mainFrame._popupSettingsDialog(NewSearch)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		self.button_OK = wx.Button(self, wx.ID_OK, "")
		self.button_OK.SetDefault()
		sizer_2.AddButton(self.button_OK)

		self.button_CLOSE = wx.Button(self, wx.ID_CLOSE, "")
		sizer_2.AddButton(self.button_CLOSE)

		sizer_2.Realize()

		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetAffirmativeId(self.button_OK.GetId())
		self.SetEscapeId(self.button_CLOSE.GetId())

		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.performSearch, self.list_ctrl_1)
		self.Bind(wx.EVT_BUTTON, self.performSearch, self.button_OK)
		self.Bind(wx.EVT_BUTTON, self.quit, self.button_CLOSE)

		self.Layout()
		self.CentreOnScreen()

	def performSearch(self, event):
		self.Close()
		event.Skip()
		global wordToSearch, ourLine
		wordToSearch = self.list_ctrl_1.GetItemText(self.list_ctrl_1.GetFocusedItem())
		# Open the selected dictionary file
		self.dbDict = sqlite3.connect(dictToUse, check_same_thread=False)
		self.dbCursor = self.dbDict.cursor()
		self.dbCursor.execute("select descricao	 from dicionario where verbete=:word", {"word": wordToSearch})
		# We only have an entry, so get it...
		ourLine = self.dbCursor.fetchone()
		self.dbDict.close()
		# Call the window showing the results
		gui.mainFrame._popupSettingsDialog(ShowResults)

	def quit(self, event):
		self.Close()
		event.Skip()


class NewSearch(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		self.SetTitle(_("dictionaries"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		text_1 = (
			# Translators: message informing the word do not exist
			_("%s not found in the dictionary of %s.\n") %(wordToSearch, totalDictList[list(dict.values()).index(selectedDict)])+
			# Translators: message asking user if he wants to search again
			_("Do you want to search another word?"))

		label_1 = wx.StaticText(self, wx.ID_ANY, text_1)
		sizer_1.Add(label_1, 0, 0, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		self.button_YES = wx.Button(self, wx.ID_YES, "")
		self.button_YES.SetDefault()
		sizer_2.AddButton(self.button_YES)

		self.button_NO = wx.Button(self, wx.ID_NO, "")
		sizer_2.AddButton(self.button_NO)

		sizer_2.Realize()

		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetAffirmativeId(self.button_YES.GetId())
		self.SetEscapeId(self.button_NO.GetId())

		self.Layout()
		self.CentreOnScreen()
		self.Bind(wx.EVT_BUTTON, self.searchAgain, self.button_YES)

	def searchAgain(self, event):
		event.Skip()
		# Calling the window to search another entry
		gui.mainFrame._popupSettingsDialog(SearchWindow)


class ShowResults(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		self.SetTitle(_("Dictionaries"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		# Translators: Static text announcing the results
		label_1 = wx.StaticText(self, wx.ID_ANY, _("Here is the result of your search:"))
		sizer_1.Add(label_1, 0, 0, 0)

		self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, ourLine[0], size = (550, 350), style=wx.TE_MULTILINE | wx.TE_READONLY)
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
		self.Close()
		event.Skip()
		# Calling the window to search another entry
		gui.mainFrame._popupSettingsDialog(SearchWindow)

	def copyToClip(self, event):
		event.Skip()
		# Copy result to clipboard
		api.copyToClip(ourLine[0])

	def quit(self, event):
		self.Close()
		event.Skip()


class DictDownload(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		# Translators: Dialog title
		self.SetTitle(_("Dictionaries"))
		self._thread = None

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

		self.progressBar = None
		self.countProgressBar = 0

	def download(self, event):
		#self.Close()
		event.Skip()
		global dictToDownload, dictDownloading
		dictDownloading = self.choice_2.GetStringSelection()
		dictToDownload = dict.get(self.choice_2.GetStringSelection())
		# Name of dictionariy
		urlN = dict.get(self.choice_2.GetStringSelection())
		# Online repository of dicts
		urlRepos = "https://www.tiflotecnia.net/dictdb/"
		# Complete URL of the dictionary file...
		urlName = urlRepos + urlN
		# Complete path where to save the dictionary
		file = os.path.join(filepath, urlN)

		# Translators: Message dialog box asking confirmation to download
		if gui.messageBox(_("Are you sure you want to download the %s dictionary from %s?") %(self.choice_2.GetStringSelection(), urlRepos[:-8]), _("Dictionaries"), style=wx.ICON_QUESTION|wx.YES_NO) == wx.YES:
			self.progressBar = wx.ProgressDialog(_("Downloading %s") %(self.choice_2.GetStringSelection(),), _("Please wait..."), 100, style=wx.PD_CAN_ABORT | wx.PD_APP_MODAL )
			# Thread to download file
			# t = threading.Thread(target=threadDownload) # # dwnl()
			# t.daemon = True
			# t.start()
			progressUpdate(self, file, dictToDownload)
			# After the correct download, update the dictionaries listes
			global missingDicts
			missingDicts.remove(dictDownloading)
			# Calling the window to download more
			gui.mainFrame._popupSettingsDialog(DictDownload)
		else:
			self.Close()

	def updateProgressBar(self):
		self.countProgressBar+=1
		if self.countProgressBar==100:
			self.countProgressBar=0
		keepgoing = self.progressBar.Update(self.countProgressBar)

	def finishProgressBar(self):
		self.progressBar.Destroy()
		dlg = wx.MessageDialog(self, _("File downloaded successfully!"), _("Success!"), wx.OK).ShowModal()

	def msgError(self):
		self.progressBar.Destroy()
		dlg = wx.MessageDialog(self, _("It was not possible to download the file."), _("Error!"), wx.OK).ShowModal()

	def quit(self, event):
		event.Skip()
		# Calling the main window to choose the dict to use, to download more or to quit the add-on
		gui.mainFrame._popupSettingsDialog(MainWindow)

class progressUpdate(Thread):
	def __init__(self, frame, file, dictToDownload):
		super(progressUpdate, self).__init__()

		self.frame = frame
		self.file = file
		self.dictToDownload = dictToDownload
		self.flagDownloadOK = True
		self.daemon = True
		self.start()

	def run(self):
		# Start download file process
		downloadFile(self, self.dictToDownload)
		# keep going until file be put on right local
		while not  os.path.exists(self.file) and self.flagDownloadOK:
			time.sleep(0.05)
			self.frame.updateProgressBar()
			if not self.flagDownloadOK:
				break
		if os.path.exists(self.file):
			self.frame.finishProgressBar()
		else:
			self.frame.msgError()

	def stopProgress(self):
		self.flagDownloadOK = False

class downloadFile(Thread):
	def __init__(self, upLevel, dictToDownload):
		super(downloadFile, self).__init__()

		self.upLevel = upLevel
		self.dictToDownload = dictToDownload
		self.daemon = True
		self.start()

	def run(self):
		# Online repository of dicts
		urlRepos = "https://www.tiflotecnia.net/dictdb/"
		# Get the file name of selected dictionary to download
		urlN = self.dictToDownload
		# Complete URL of the dictionary file...
		urlName = urlRepos + urlN
		# Complete path where to save the dictionary
		file = os.path.join(filepath, urlN)

		try: 
			req = urllib.request.Request(urlName, headers={'User-Agent': 'Mozilla/5.0'})
			response = urllib.request.urlopen(req)
			fileContents = response.read()
			response.close()
		except:
			self.upLevel.stopProgress()
		else:
			f = open(file, "wb")
			f.write(fileContents)
			f.close()

