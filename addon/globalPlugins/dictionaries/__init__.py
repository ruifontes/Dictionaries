# -*- coding: utf-8 -*-
# dictionaries add-on
# Provides quick access to several dictionaries.
# written by Rui Fontes <rui.fontes@tiflotecnia.com>, Ângelo Abrantes <ampa4374@gmail.com> and Abel Passos do Nascimento Jr. <abel.passos@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import globalPluginHandler
import globalVars
import core
import api
import os
import threading
import wx
import gui
from gui.settingsDialogs import NVDASettingsDialog, SettingsPanel
from gui import guiHelper
import ui
import versionInfo
if versionInfo.version_year < 2024:
	from . import sqlite3
else:
	from . import sqlite311 as sqlite3
import urllib.request
import socket
from scriptHandler import script
# Necessary For translation
import addonHandler
addonHandler.initTranslation()

# Global variables
filepath = os.path.join(os.path.dirname(__file__), "dicionarios")
os.makedirs(filepath, exist_ok=True)
available = os.path.join(globalVars.appArgs.configPath, "availableDictsList.ini")
availableDictsList = []
missingDicts = []
defaultDict = ""
selectedDict = ""
dictToUse = ""
wordToSearch = ""
ourLine = ""

# Mapping of display name → sqlite filename
dictMap = {
	# Translators: Name of a dictionary
	_("Dutch-French") : "neerlandes-frances.db",
	# Translators: Name of a dictionary
	_("English-Amharic") : "amharic.db",
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
	_("Otoman-Turkish") : "Otomano-turco.db",
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
	_("Tetun-Portuguese") : "Dicionario_tetun-portugues.db",
	# Translators: Name of a dictionary
	_("English (Concise Oxford dictionary)") : "azdictionary.db",
	# Translators: Name of a dictionary
	_("English synonyms dictionary)") : "ingles-sinonimos.db",
	# Translators: Name of a dictionary
	_("English Wikcionary") : "English_Wikctionary.db",
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
	_("Portuguese Wikcionary") : "Portugues_Wikctionary.db",
	# Translators: Name of a dictionary
	_("Spanish - RAE (in spanish)") : "diccionario-de-la-lengua-espanhola-rae.db",
	# Translators: Name of a dictionary
	_("Spanish - RAE New version (in spanish)") : "Diccionario_de_la_Lengua_Espanhola-RAE2.db",
	# Translators: Name of a dictionary
	_("Turkish (in turkish)") : "tk.db",
	# Translators: Name of a dictionary
	_("Alchemy (in portuguese)") : "Dicionario_Alquimico.db",
	# Translators: Name of a dictionary
	_("Biblical (in portuguese)") : "Dicionario_biblico-Italo_Fernando_Brevi.db",
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
	_("Music (in portuguese)") : "dicionario_de_musica.db",
	# Translators: Name of a dictionary
	_("Music (in turkish)") : "Turkish_Music_Terms.db",
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
	_("Portuguese musicians (in portuguese)") : "dicionario_de_musicos_portugueses.db",
	# Translators: Name of a dictionary
	_("Psychology (in portuguese)") : "dicionario-de-psicologia.db",
	# Translators: Name of a dictionary
	_("Slang and idioms (in portuguese)") : "dicionario_de_calao_e_expressoes_idiomaticas_2022.db",
		# Translators: Name of a dictionary
	_("Tecnical of Informatic (english-french)") : "informatica-ingles-frances.db",
	# Translators: Name of a dictionary
	_("Tecnical of Informatic (in portuguese)") : "dicionario-tecnico-de-informatica.db",
	# Translators: Name of a dictionary
	_("Veterinary medicin (in portuguese)") : "Dicionario_Medicina_Veterinaria.db",
}

totalDictList = list(dictMap.keys())

thematics = [
	"Dicionario-de-dificuldades-da-lingua-portuguesa.db",
	"Dicionario_Alquimico.db",
	"Dicionario_biblico-Italo_Fernando_Brevi.db",
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
	"dicionario_de_musica.db",
	"Turkish_Music_Terms.db",
	"Termos_tecnicos_de_enfermagem_mais_usados.db",
	"cambridge-dictionary-of-philosophy.db",
	"dicionario-de-filosofia.db",
	"diccionario_fonetico(espanhol).db",
	"dicionario-de-politica.db",
	"dicionario_de_musicos_portugueses.db",
	"dicionario-de-psicologia.db",
	"dicionario_de_calao_e_expressoes_idiomaticas_2022.db",
	"informatica-ingles-frances.db",
	"dicionario-tecnico-de-informatica.db",
	"Dicionario_Medicina_Veterinaria.db"
]


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		if globalVars.appArgs.secure:
			return

	#defining a script with decorator:
	@script(
		gesture="kb:Control+shift+F6",
		# Translators: Message to be announced during Keyboard Help	 
		description= _("Main window to access several dictionaries"),
		# For translators: Name of the section in "Input gestures" dialog.	
		category= _("Dictionaries")
	)
	def script_openMainWindow(self, event):
		dialog0 = MainWindow(gui.mainFrame)
		if not dialog0.IsShown():
			gui.mainFrame.prePopup()
			dialog0.Show()
			gui.mainFrame.postPopup()

	@script(
		gesture="kb:Control+windows+F6",
		# Translators: Message to be announced during Keyboard Help	 
		description= _("Opens the dictionary search window using the default dict"),
		# For translators: Name of the section in "Input gestures" dialog.	
		category= _("Dictionaries")
	)
	def script_searchOnDefaultDict(self, event):
		global selectedDict, dictToUse
		# load default if set, otherwise first available from INI
		if defaultDict == "":
			if os.path.isfile(available):
				dictList = []
				with open(available, "r", encoding="utf-8") as f:
					for line in f:
						dictList.append(line.strip())
			selectedDict = dictMap.get(dictList[1])
			dictToUse = os.path.join(filepath, selectedDict)
		else:
			selectedDict = defaultDict
			dictToUse = os.path.join(filepath, selectedDict)
		dialog1 = SearchWindow(gui.mainFrame)
		if not dialog1.IsShown():
			gui.mainFrame.prePopup()
			dialog1.Show()
			gui.mainFrame.postPopup()


class MainWindow(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		super(MainWindow, self).__init__(*args, **kwds)
		# Translators: Dialog title
		self.SetTitle(_("Dictionaries"))

		global missingDicts, availableDictsList, dictList
		availableDictsList = os.listdir(filepath)
		missingDicts = []
		dictList = list(dictMap.keys())
		# filter out missing
		n = 0
		while n < len(dictList):
			if dictMap.get(dictList[n]) not in availableDictsList:
				missingDicts.append(dictList[n])
				del dictList[n]
				n -= 1
			n += 1
		# build INI if needed
		if not os.path.isfile(available):
			with open(available, "w", encoding="utf-8") as f:
				f.write(str(len(dictList)) + "\n")
				for L in dictList:
					f.write(L + "\n")
		# read user ordering
		dictList = []
		with open(available, "r", encoding="utf-8") as f:
			for L in f:
				dictList.append(L.strip())
		try:
			del dictList[0]
		except:
				pass

		sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
		label_1 = wx.StaticText(self, wx.ID_ANY,
			# Translators: StaticText with instructions for the user:
			_("Choose the dictionary and press Enter or Tab for other options."))
		sizer_1.Add(label_1, 0, 0, 0)

		global choice_1
		choice_1 = wx.Choice(self, wx.ID_ANY, choices=dictList)
		choice_1.SetFocus()
		choice_1.SetSelection(0)
		sizer_1.Add(choice_1, 0, 0, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALL, 4)

		self.button_1 = wx.Button(self, wx.ID_OK, "")
		self.button_1.SetDefault()
		sizer_2.Add(self.button_1, 0, 0, 0)

		# Translators: Button to open the Manage dicts window
		self.button_2 = wx.Button(self, wx.ID_ANY, _("Manage dictionaries..."))
		sizer_2.Add(self.button_2, 0, 0, 0)

		# Translators: Button to set a dictionnary as default
		self.button_3 = wx.Button(self, wx.ID_ANY, _("Set dictionary as Default"))
		sizer_2.Add(self.button_3, 0, 0, 0)

		self.button_CANCEL = wx.Button(self, wx.ID_CANCEL, "")
		sizer_2.AddButton(self.button_CANCEL)

		sizer_2.Realize()
		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetAffirmativeId(self.button_1.GetId())
		self.SetEscapeId(self.button_CANCEL.GetId())

		self.Bind(wx.EVT_BUTTON, self.searchWindow, self.button_1)
		self.Bind(wx.EVT_BUTTON, self.manageDicts, self.button_2)
		self.Bind(wx.EVT_BUTTON, self.setAsDefaultDict, self.button_3)
		self.Bind(wx.EVT_BUTTON, self.quit, self.button_CANCEL)

		self.Layout()
		self.CentreOnScreen()

	def searchWindow(self, event):
		self.Close()
		event.Skip()
		global selectedDict, dictToUse
		selectedDict = dictMap.get(choice_1.GetStringSelection())
		dictToUse = os.path.join(filepath, selectedDict)
		dialog1 = SearchWindow(gui.mainFrame)
		if not dialog1.IsShown():
			gui.mainFrame.prePopup()
			dialog1.Show()
			gui.mainFrame.postPopup()

	def setAsDefaultDict(self, event):
		global defaultDict
		defaultDict = dictMap.get(choice_1.GetStringSelection())
		# Translators: Announce dictionary has been set  as default
		ui.message(choice_1.GetStringSelection() + _(" set as default dictionary."))

	def manageDicts(self, event):
		event.Skip()
		dialog2 = ManageDicts(gui.mainFrame)
		if not dialog2.IsShown():
			gui.mainFrame.prePopup()
			dialog2.Show()
			gui.mainFrame.postPopup()

	def quit(self, event):
		self.Destroy()
		event.Skip()


class SearchWindow(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		super(SearchWindow, self).__init__(*args, **kwds)
		# Translators: Dialog title
		self.SetTitle(_("Dictionaries"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		if selectedDict in thematics:
			# Use a list for thematic dictionaries
			# For translators: Asking to choose what to search
			label_1 = wx.StaticText(self, wx.ID_ANY, _("Select what to search from the list."))
			sizer_1.Add(label_1, 0, 0, 0)

			# Create and populate the list control
			self.list_ctrl_1 = wx.ListCtrl(
				self, wx.ID_ANY,
				style=wx.LC_HRULES 
				      | wx.LC_REPORT 
				      | wx.LC_SINGLE_SEL 
				      | wx.LC_VRULES
			)
			sizer_1.Add(self.list_ctrl_1, 1, wx.EXPAND, 0)

			# Translators: Message asking the user to wait for the list...
			ui.message(_("Please wait until the index is created..."))

			db = sqlite3.connect(dictToUse, check_same_thread=False)
			cursor = db.cursor()
			cursor.execute("select verbete from dicionario")
			occurs = cursor.fetchall()
			db.close()

			# Set up column once
			self.list_ctrl_1.InsertColumn(0, _("Verbetes"))
			for i, (verbete,) in enumerate(occurs):
				self.list_ctrl_1.InsertItem(i, verbete)

			self.list_ctrl_1.Focus(0)
			self.list_ctrl_1.Select(0)

		else:
			# Use text entry for non‐thematic dictionaries
			# For translators: Asking to enter a letter, word or expression to search
			label_1 = wx.StaticText(self, wx.ID_ANY, _("Enter the first letter, a word or an expression to search."))
			sizer_1.Add(label_1, 0, 0, 0)

			self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, "")
			self.text_ctrl_1.SetFocus()
			sizer_1.Add(self.text_ctrl_1, 0, 0, 0)

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
		if selectedDict in thematics:
			self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.performSearch, self.list_ctrl_1)

		self.Layout()
		self.CentreOnScreen()

	def performSearch(self, event):
		self.Close()
		event.Skip()
		global wordToSearch, ourLine
		if selectedDict in thematics:
			wordToSearch = self.list_ctrl_1.GetItemText(self.list_ctrl_1.GetFocusedItem())
			self.dbDict = sqlite3.connect(dictToUse, check_same_thread=False)
			self.dbCursor = self.dbDict.cursor()
			self.dbCursor.execute(
				"select descricao from dicionario where verbete=:word",
				{"word": wordToSearch}
			)
			ourLine = self.dbCursor.fetchone()
			self.dbDict.close()
			dialog3 = ShowResults(gui.mainFrame)
			if not dialog3.IsShown():
				gui.mainFrame.prePopup()
				dialog3.Show()
				gui.mainFrame.postPopup()
		else:
			wordToSearch = self.text_ctrl_1.GetValue()
			dialog4 = IndexWindow(gui.mainFrame)
			if not dialog4.IsShown():
				gui.mainFrame.prePopup()
				dialog4.Show()
				gui.mainFrame.postPopup()

	def quit(self, event):
		self.Close()
		event.Skip()


class IndexWindow(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		super(IndexWindow, self).__init__(*args, **kwds)
		# Translators: Dialog title
		self.SetTitle(_("Dictionaries"))
		global wordToSearch, ourLine

		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		# For translators: Asking to choose what to search
		label_1 = wx.StaticText(self, wx.ID_ANY, _("Select what to search  from the list."))
		sizer_1.Add(label_1, 0, 0, 0)

		self.list_ctrl_1 = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES | wx.LC_SORT_ASCENDING)
		sizer_1.Add(self.list_ctrl_1, 1, wx.EXPAND, 0)

		pattern = "'" + wordToSearch + "%'"
		self.dbDict = sqlite3.connect(dictToUse, check_same_thread=False)
		self.dbCursor = self.dbDict.cursor()
		self.dbCursor.execute(
			"select verbete from dicionario where upper(verbete) like " + pattern
		)
		occurs = self.dbCursor.fetchall()

		if len(occurs) == 1:
			word = occurs[0][0]
			self.dbCursor.execute(
				"select descricao from dicionario where verbete=:word", {"word": word})
			ourLine = self.dbCursor.fetchone()
			self.dbDict.close()
			self.Destroy()
			dialog3 = ShowResults(gui.mainFrame)
			if not dialog3.IsShown():
				gui.mainFrame.prePopup()
				dialog3.Show()
				gui.mainFrame.postPopup()
		elif len(occurs) >= 2:
			self.list_ctrl_1.ClearAll()
			self.list_ctrl_1.InsertColumn(0, "Verbetes")
			for i, row in enumerate(occurs):
				self.list_ctrl_1.InsertItem(i, row[0])
			self.list_ctrl_1.Focus(0)
			self.list_ctrl_1.Select(0)
			self.dbDict.close()
		else:
			self.dbDict.close()
			self.Destroy()
			dialog5 = NewSearch(gui.mainFrame)
			if not dialog5.IsShown():
				gui.mainFrame.prePopup()
				dialog5.Show()
				gui.mainFrame.postPopup()

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
		wordToSearch = self.list_ctrl_1.GetItemText(self.list_ctrl_1.GetFocusedItem()		)

		self.dbDict = sqlite3.connect(dictToUse, check_same_thread=False)
		self.dbCursor = self.dbDict.cursor()
		self.dbCursor.execute(
			"select descricao from dicionario where verbete=:word",
			{"word": wordToSearch}
		)
		ourLine = self.dbCursor.fetchone()
		self.dbDict.close()
		dialog3 = ShowResults(gui.mainFrame)
		if not dialog3.IsShown():
			gui.mainFrame.prePopup()
			dialog3.Show()
			gui.mainFrame.postPopup()

	def quit(self, event):
		self.Destroy()
		event.Skip()


class NewSearch(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		super(NewSearch, self).__init__(*args, **kwds)
		# Translators: Dialog title
		self.SetTitle(_("Dictionaries"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		text_1 = (
			# Translators: message informing the word do not exist
			_("%s not found in the dictionary of %s.\n") % (
				wordToSearch,
				totalDictList[list(dictMap.values()).index(selectedDict)]
			)
			# Translators: message asking user if he wants to search again
			+ _("Do you want to search another word?")
		)
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
		dialog1 = SearchWindow(gui.mainFrame)
		if not dialog1.IsShown():
			gui.mainFrame.prePopup()
			dialog1.Show()
			gui.mainFrame.postPopup()


class ShowResults(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		super(ShowResults, self).__init__(*args, **kwds)
		# Translators: Dialog title
		self.SetTitle(_("Dictionaries"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		label_1 = wx.StaticText(self, wx.ID_ANY,
			# Translators: Static text announcing the results
			_("Here is the result of your search:"))
		sizer_1.Add(label_1, 0, 0, 0)

		self.text_ctrl_1 = wx.TextCtrl(
			self, wx.ID_ANY, ourLine[0],
			size=(550, 350),
			style=wx.TE_MULTILINE | wx.TE_READONLY
		)
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
		self.Destroy()
		event.Skip()
		dialog1 = SearchWindow(gui.mainFrame)
		if not dialog1.IsShown():
			gui.mainFrame.prePopup()
			dialog1.Show()
			gui.mainFrame.postPopup()

	def copyToClip(self, event):
		event.Skip()
		api.copyToClip(ourLine[0])

	def quit(self, event):
		self.Destroy()
		event.Skip()


class ManageDicts(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		super(ManageDicts, self).__init__(*args, **kwds)
		# Translators: Dialog title
		self.SetTitle(_("Dictionaries"))

		# download state (guard flags)
		self.progressBar = None
		self._progressActive = False
		self._progressToken = 0  # increments per download session
		self.thread = None

		# Progress driven by a GUI timer (runs only on main thread)
		self._pulseTimer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self._onPulse, self._pulseTimer)

		# Handle window close to abort active downloads safely
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)

		sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
		self.notebook_Manage = wx.Notebook(self, wx.ID_ANY, style=wx.NB_LEFT)
		sizer_1.Add(self.notebook_Manage, 1, wx.EXPAND, 0)

		# Manage page
		self.notebook_1_pane_2 = wx.Panel(self.notebook_Manage, wx.ID_ANY)
		# Translators: Name of page of dialog allowing ordering and deletion of dictionaries
		self.notebook_Manage.AddPage(self.notebook_1_pane_2, _("Manage"))
		sizer_4 = wx.BoxSizer(wx.VERTICAL)
		# Translators: Static text announcing what to do in this dialog
		label_1 = wx.StaticText(self.notebook_1_pane_2, wx.ID_ANY, _("Order or delete existing dictionaries"))
		sizer_4.Add(label_1, 0, 0, 0)

		self.list_box_1 = wx.ListBox(self.notebook_1_pane_2, wx.ID_ANY, choices=dictList)
		if self.list_box_1.GetCount() > 0:
			self.list_box_1.SetSelection(0)
		sizer_4.Add(self.list_box_1, 0, 0, 0)

		# Translators: Name of button to move up a dictionary
		self.button_1 = wx.Button(self.notebook_1_pane_2, wx.ID_ANY, _("Move up"))
		sizer_4.Add(self.button_1, 0, 0, 0)
		# Translators: Name of button to move down  a dictionary
		self.button_2 = wx.Button(self.notebook_1_pane_2, wx.ID_ANY, _("Move down"))
		sizer_4.Add(self.button_2, 0, 0, 0)
		# Translators: Name of button to delete  a dictionary
		self.button_3 = wx.Button(self.notebook_1_pane_2, wx.ID_ANY, _("Delete"))
		sizer_4.Add(self.button_3, 0, 0, 0)
		self.notebook_1_pane_2.SetSizer(sizer_4)

		# Download page
		self.notebook_1_pane_1 = wx.Panel(self.notebook_Manage, wx.ID_ANY)
		# Translators: Name of page of dialog allowing download of dictionaries
		self.notebook_Manage.AddPage(self.notebook_1_pane_1, _("Download"))
		sizer_3 = wx.BoxSizer(wx.VERTICAL)
		# Translators: Information about the download page
		label_2 = wx.StaticText(self.notebook_1_pane_1, wx.ID_ANY, _("Choose the dictionary to download and press Enter"))
		sizer_3.Add(label_2, 0, 0, 0)

		self.choice_2 = wx.ListBox(self.notebook_1_pane_1, wx.ID_ANY, choices=missingDicts, style=wx.LB_SINGLE)
		if self.choice_2.GetCount() > 0:
			self.choice_2.SetSelection(0)
		sizer_3.Add(self.choice_2, 0, 0, 0)

		# Translators: Name of button to download  a dictionary
		self.button_4 = wx.Button(self.notebook_1_pane_1, wx.ID_ANY, _("Download"))
		sizer_3.Add(self.button_4, 0, 0, 0)
		self.notebook_1_pane_1.SetSizer(sizer_3)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALL, 4)
		self.button_CLOSE = wx.Button(self, wx.ID_CLOSE, "")
		sizer_2.AddButton(self.button_CLOSE)
		sizer_2.Realize()

		self.SetSizer(sizer_1)
		sizer_1.Fit(self)
		self.SetEscapeId(self.button_CLOSE.GetId())

		# event bindings
		self.Bind(wx.EVT_BUTTON, self.moveUp, self.button_1)
		self.Bind(wx.EVT_BUTTON, self.moveDown, self.button_2)
		self.Bind(wx.EVT_BUTTON, self.deleteDict, self.button_3)
		self.Bind(wx.EVT_BUTTON, self.download, self.button_4)
		self.Bind(wx.EVT_BUTTON, self.onClose, self.button_CLOSE)
		self.list_box_1.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
		self.choice_2.Bind(wx.EVT_KEY_DOWN, self.onKeyPress1)
		self.notebook_Manage.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self._onPageChanged)
		self.choice_2.Bind(wx.EVT_SET_FOCUS, self._onListFocus)
		self.list_box_1.Bind(wx.EVT_CHAR_HOOK, self._manageCharHook)

		# download state (guard flags)
		self.progressBar = None
		self._progressActive = False
		self._progressToken = 0  # increments per download session

		self.Layout()
		self.CentreOnScreen()

	def _onPageChanged(self, evt):
		# When entering in the Download page, set  default button and set focus on choice_2
		if self.notebook_Manage.GetPage(evt.GetSelection()) is self.notebook_1_pane_1:
			self.button_4.SetDefault()
			try:
				self.SetAffirmativeId(self.button_4.GetId())
			except Exception:
				pass
		evt.Skip()

	def _onListFocus(self, evt):
		# se a lista ganhar foco, garante que Download é o default
		self.button_4.SetDefault()
		try:
			self.SetAffirmativeId(self.button_4.GetId())
		except Exception:
			pass
		evt.Skip()

	def moveUp(self, event):
		event.Skip()
		global dictList
		itemIndex = self.list_box_1.GetSelection()
		if itemIndex == 0:
			# Translators: Announcing the first item can not be moved up
			ui.message(_("The first item can not be moved up!"))
			return
		itemName = self.list_box_1.GetString(itemIndex)
		# Translators: Announcing that the item was moved to the new position
		ui.message(itemName + _(" moved to position ") + str(itemIndex))
		dictList.insert(itemIndex - 1, itemName)
		del dictList[itemIndex + 1]
		with open(available, "w", encoding="utf-8") as f:
			f.write(str(len(dictList)) + "\n")
			for L in dictList:
				f.write(L + "\n")
		self.list_box_1.Set(dictList)
		self.list_box_1.SetFocus()
		self.list_box_1.SetSelection(itemIndex - 1)

	def moveDown(self, event):
		event.Skip()
		global dictList
		itemIndex = self.list_box_1.GetSelection()
		x = len(dictList)
		if itemIndex == x - 1:
			# Translators: Announcing the last  item can not be moved down
			ui.message(_("The last item can not be moved down!"))
			return
		itemName = self.list_box_1.GetString(itemIndex)
		# Translators: Announcing that the item was moved to the new position
		ui.message(itemName + _(" moved to position ") + str(itemIndex + 2))
		del dictList[itemIndex]
		dictList.insert(itemIndex + 1, itemName)
		with open(available, "w", encoding="utf-8") as f:
			f.write(str(len(dictList)) + "\n")
			for L in dictList:
				f.write(L + "\n")
		self.list_box_1.Set(dictList)
		self.list_box_1.SetFocus()
		self.list_box_1.SetSelection(itemIndex + 1)

	def onKeyPress(self, event):
		if event.GetKeyCode() == wx.WXK_DELETE:
			self.deleteDict(event)
		if event.GetKeyCode() in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER, 13):
			# Swallow Enter on Manage tab to avoid triggering the dialog's default button
			return
		event.Skip()

	def _manageCharHook(self, event):
		key = event.GetKeyCode()
		if key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER, 13):
			# Swallow  Enter to do not ative the default button of dialog
			return
		event.Skip()

	def deleteDict(self, event):
		event.Skip()
		global dictList, missingDicts
		itemIndex = self.list_box_1.GetSelection()
		name = dictMap.get(self.list_box_1.GetStringSelection())
		file = os.path.join(filepath, name)
		if gui.messageBox(
			# Translators: Message dialog box asking confirmation to delete the dictionary
			_("Are you sure you want to delete the %s dictionary file?") % self.list_box_1.GetStringSelection(),
			_("Dictionaries"),
			style=wx.ICON_QUESTION | wx.YES_NO
		) == wx.YES:
			missingDicts.append(dictList[itemIndex])
			del dictList[itemIndex]
			try:
				os.remove(file)
			except Exception:
				pass
			with open(available, "w", encoding="utf-8") as f:
				f.write(str(len(dictList)) + "\n")
				for L in dictList:
					f.write(L + "\n")
		self.list_box_1.Set(dictList)
		self.list_box_1.SetFocus()
		if self.list_box_1.GetCount():
			self.list_box_1.SetSelection(0)
		self.choice_2.Set(missingDicts)

	def onKeyPress1(self, event):
		if event.GetKeyCode() == wx.WXK_RETURN:
			self.download(event)
		event.Skip()

	def download(self, event):
		# Called when user clicks "Download"
		self.dictIndex = self.choice_2.GetSelection()
		self.dictName = self.choice_2.GetStringSelection()
		self.fileName = dictMap.get(self.dictName)
		url = "https://www.tiflotecnia.net/dictdb/" + self.fileName
		dest = os.path.join(filepath, self.fileName)
		# Translators: Message dialog box asking confirmation to download
		if gui.messageBox(_("Are you sure you want to download the %s dictionary from %s?") %(self.dictName, "https://www.tiflotecnia.net"), _("Dictionaries"), style=wx.ICON_QUESTION|wx.YES_NO) == wx.YES:
			# new session
			self._progressToken += 1
			self._progressActive = True

			self.progressBar = wx.ProgressDialog(
				# Translators: Message dialog box informing  the downloading of a dictionary
				_("Downloading %s") % self.dictName,
				# Translators: Dialog title of downloading dialog
				_("Please wait..."),
				maximum=100,
				style=wx.PD_APP_MODAL | wx.PD_CAN_ABORT
			)
			# Start GUI-only pulsing (no worker updates)
			self._pulseTimer.Start(150, oneShot=False)

			self.thread = DownloadThread(self, url, dest, self._progressToken)
			self.thread.start()
		else:
			self.choice_2.SetFocus()

	def _onPulse(self, evt):
		"""
		Timer callback on GUI thread: safely pulse the progress dialog.
		No worker thread calls Update/Pulse directly.
		"""
		if not self._progressActive:
			return
		dlg = self.progressBar
		if dlg is None:
			return
		try:
			res = dlg.Pulse()
			# wx Classic: bool; Phoenix: (keepGoing, skip)
			keepGoing = res[0] if isinstance(res, tuple) else res
		except Exception:
			# dialog is gone; stop pulsing
			self._progressActive = False
			self._pulseTimer.Stop()
			self.progressBar = None
			return
		if not keepGoing and self.thread:
			# user pressed Cancel
			self.thread.abort()

	def updateProgressBar(self, token, pct):
		"""
		Called in the GUI thread via wx.CallAfter.
		Guard against stale tokens and dead dialogs. Handle bool/tuple return.
		"""
		# session inactive? ignore
		if not self._progressActive:
			return
		# stale update from previous session? ignore
		if token != self._progressToken:
			return
		dlg = self.progressBar
		if dlg is None:
			return
		try:
			res = dlg.Update(int(pct))
			# wx Classic returns bool; wx Phoenix returns (keepGoing, skip)
			keepGoing = res[0] if isinstance(res, tuple) else res
		except Exception:
			# dialog likely destroyed; hard stop further updates
			self._progressActive = False
			self.progressBar = None
			return
		if not keepGoing and self.thread:
			# user clicked Cancel on ProgressDialog
			self.thread.abort()

	def stopProgress(self):
		# error path
		self._progressActive = False
		self._progressToken += 1
		self._pulseTimer.Stop()
		dlg = self.progressBar
		self.progressBar = None
		if dlg is not None:
			try:
				dlg.Destroy()
			except Exception:
				pass
		self.thread = None

	def finishProgressBar(self, token):
		# success path
		if token != self._progressToken:
			return
		self._progressActive = False
		self._progressToken += 1
		self._pulseTimer.Stop()
		dlg = self.progressBar
		self.progressBar = None
		if dlg is not None:
			try:
				dlg.Destroy()
			except Exception:
				pass
		self.thread = None
		# Translators: Message dialog box announcing the successfull download
		dlg = wx.MessageDialog(self, _("File downloaded successfully!"), _("Success!"), wx.OK).ShowModal()
		# update lists/persist
		global missingDicts, dictList
		if 0 <= self.dictIndex < len(missingDicts):
			del missingDicts[self.dictIndex]
		self.choice_2.Set(missingDicts)
		self.choice_2.SetFocus()
		if self.choice_2.GetCount():
			self.choice_2.SetSelection(0)
		dictList.append(self.dictName)
		self.list_box_1.Set(dictList)
		with open(available, "w", encoding="utf-8") as f:
			f.write(str(len(dictList)) + "\n")
			for L in dictList:
				f.write(L + "\n")

	def msgError(self, errorMsg):
		self._progressActive = False
		self._progressToken += 1
		self._pulseTimer.Stop()
		dlg = self.progressBar
		self.progressBar = None
		if dlg is not None:
			try:
				dlg.Destroy()
			except Exception:
				pass
		self.thread = None
		# Translators: Message dialog box announcing an error on downloading
		wx.MessageBox(_("Error during download:\n%s") % errorMsg, _("Download Error"), wx.OK | wx.ICON_ERROR)

	def onClose(self, evt):
		self._progressActive = False
		self._progressToken += 1
		self._pulseTimer.Stop()
		if self.thread:
			self.thread.abort()
		dlg = self.progressBar
		self.progressBar = None
		if dlg is not None:
			try:
				dlg.Destroy()
			except Exception:
				pass
		self.thread = None
		# Refresh & focus main window
		wx.CallAfter(self._refreshMainWindow)
		evt.Skip()

	def onDestroy(self, evt):
		self._progressToken += 1
		self._progressActive = False
		self._pulseTimer.Stop()
		if self.thread:
			self.thread.abort()
		self.progressBar = None
		self.thread = None
		evt.Skip()

	def _refreshMainWindow(self):
		"""Refresh main window list and restore focus safely."""
		try:
			# Update choices with current list
			choice_1.Set(dictList)
			# Ensure a valid selection
			if choice_1.GetSelection() == wx.NOT_FOUND and choice_1.GetCount():
				choice_1.SetSelection(0)
			# Bring main window to front and focus the chooser
			mainWin = choice_1.GetParent()
			try:
				mainWin.Raise()
			except Exception:
				pass
			choice_1.SetFocus()
		except Exception:
			# If main window/control no longer exists, ignore
			pass


class DownloadThread(threading.Thread):
	"""
	Background thread downloads file and reports only completion/error.
	No direct GUI updates; GUI shows progress via a timer (Pulse).
	"""
	def __init__(self, parent, url, destPath, token):
		super(DownloadThread, self).__init__(daemon=True)
		self.parent = parent
		self.url = url
		self.destPath = destPath
		self.token = token
		self._abort = False

	def run(self):
		try:
			socket.setdefaulttimeout(30)
			req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
			with urllib.request.urlopen(req) as resp, open(self.destPath, 'wb') as out:
				while not self._abort:
					chunk = resp.read(8192)
					if not chunk:
						break
					out.write(chunk)
				if self._abort:
					raise Exception("Download cancelled by user")
			# success
			wx.CallAfter(self.parent.finishProgressBar, self.token)
		except Exception as e:
			try:
				if os.path.exists(self.destPath):
					os.remove(self.destPath)
			except Exception:
				pass
			wx.CallAfter(self.parent.stopProgress)
			wx.CallAfter(self.parent.msgError, str(e))

	def abort(self):
		self._abort = True
