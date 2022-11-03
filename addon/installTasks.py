#-*- coding: utf-8 -*-
# Part of Dictionaries add-on for NVDA.
# written by Rui Fontes <rui.fontes@tiflotecnia.com>, Ângelo Abrantes and Abel Passos do Nascimento Jr. <abel.passos@gmail.com>

import os
import shutil
import globalVars
import addonHandler

def onInstall():
	configFilePath = os.path.abspath(os.path.join(globalVars.appArgs.configPath, "addons", "dictionaries", "globalPlugins", "dictionaries", "dicionarios"))
	if os.path.isdir(configFilePath):	
		shutil.rmtree(os.path.abspath(os.path.join(globalVars.appArgs.configPath, "addons", "dictionaries" + addonHandler.ADDON_PENDINGINSTALL_SUFFIX, "globalPlugins", "dictionaries", "dicionarios")))
		os.rename(configFilePath, os.path.abspath(os.path.join(globalVars.appArgs.configPath, "addons", "dictionaries" + addonHandler.ADDON_PENDINGINSTALL_SUFFIX, "globalPlugins", "dictionaries", "dicionarios")))
