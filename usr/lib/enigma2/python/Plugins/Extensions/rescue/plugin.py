# -*- coding: utf-8 -*-
# Plugin Modo rescue Dreambox by linuxbox.tv
from Screens.Screen import Screen
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap
from Components.Console import Console as iConsole
from Components.ActionMap import ActionMap
from Components.Sources.List import List
from Components.Label import Label
from Plugins.Plugin import PluginDescriptor
from Components.Language import language
from Tools.LoadPixmap import LoadPixmap
import os
import enigma
from Plugins.SystemPlugins.SoftwareManager.BackupRestore import BackupScreen, RestoreScreen, BackupSelection, getBackupPath, getBackupFilename
from Screens.MessageBox import MessageBox
from Components.Console import Console as iConsole

	
class dreambox_rescue(Screen):

	skin = """
		<screen position="center,center" size="1000,600" backgroundColor="white" title="Dreambox Rescue" >
		<widget source="header" render="Label" position="200,30" size="700,300" foregroundColor="black" backgroundColor="white" font="Regular; 40" halign="left" transparent="1" />
		<widget source="contenido" render="Label" position="200,200" size="700,300" foregroundColor="#848484" backgroundColor="white" font="Regular; 30" halign="left" transparent="1" />
		<eLabel name="line" position="200,490" size="750,1" backgroundColor="#aba7a6" />
		<ePixmap name="menu" position="5,5" size="158,600" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/rescue/imagenes/menu.png" zPosition="-5" />
		<ePixmap name="continuar" position="750,520" size="230,61" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/rescue/imagenes/green.png" zPosition="-5" />
		<ePixmap name="salir" position="190,520" size="230,61" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/rescue/imagenes/red.png" zPosition="-5" />
		<widget source="key_green" render="Label" position="770,530" size="200,50" zPosition="1" font="Regular; 30" transparent="1" foregroundColor="white" noWrap="1" />
		<widget source="key_red" render="Label" position="270,530" size="200,50" zPosition="1" font="Regular; 30" transparent="1" foregroundColor="white" noWrap="1" />
		<ePixmap name="ayuda" position="470,520" size="230,61" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/rescue/imagenes/blue.png" zPosition="-5" />
<widget source="key_blue" render="Label" position="520,530" size="200,50" zPosition="1" font="Regular; 30" transparent="1" foregroundColor="white" noWrap="1" />
		</screen>"""

	
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.skinName = "dreambox_rescue"
		self.setTitle(_("Asistente Dreambox Rescue"))
		self.indexpos = None
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"blue": self.informacion,
			"green": self.backup,
			
			
		})

		self["key_red"] = StaticText(_("Cancelar"))
		self["key_blue"] = StaticText(_("Ayuda"))
		self["key_green"] = StaticText(_("Continuar"))
		self["header"] = StaticText(_("Bienvenido al Asistente de Activacion Modo Rescue Dreambox"))
		self["contenido"] = StaticText(_("Has accedido al asistente de activacion del modo Rescue en su receptor Dreambox, para proceder a la actualizacion de su receptor a traves del navegador web de su ordenador, pulse <CONTINUAR> si estas seguro, o de lo contrario pulse <CANCELAR>"))
		
	def exit(self):
		self.close()

			
	def backup(self):
		self.session.open(backup)

	def informacion(self):
		self.session.open(ayuda)

######################################################################################

class backup(Screen):

	skin = """
		<screen position="center,center" size="1000,600" backgroundColor="white" title="Dreambox Rescue" >
		<widget source="header" render="Label" position="200,30" size="700,300" foregroundColor="black" backgroundColor="white" font="Regular; 40" halign="left" transparent="1" />
		<widget source="contenido" render="Label" position="200,200" size="700,300" foregroundColor="#848484" backgroundColor="white" font="Regular; 30" halign="left" transparent="1" />
		<eLabel name="line" position="200,490" size="750,1" backgroundColor="#aba7a6" />
		<ePixmap name="menu" position="5,5" size="158,600" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/rescue/imagenes/menu.png" zPosition="-5" />
		<ePixmap name="continuar" position="750,520" size="230,61" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/rescue/imagenes/green.png" zPosition="-5" />
		<ePixmap name="salir" position="190,520" size="230,61" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/rescue/imagenes/red.png" zPosition="-5" />
		<widget source="key_green" render="Label" position="770,530" size="200,50" zPosition="1" font="Regular; 30" transparent="1" foregroundColor="white" noWrap="1" />
		<widget source="key_red" render="Label" position="270,530" size="200,50" zPosition="1" font="Regular; 30" transparent="1" foregroundColor="white" noWrap="1" />
		</screen>"""
	
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.skinName = "backup"
		self.setTitle(_("Asistente Dreambox Rescue"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.paso2,
			
			
		})
		self["header"] = StaticText(_("Realizar copia de Seguridad de la configuracion de nuestro Receptor"))
		self["contenido"] = StaticText(_("Antes de proceder a la activacion del modo rescue, tienes la posibilidad de realizar una copia de seguridad de archivos de configuracion de su receptor, si lo desea pulse boton <CONTINUAR> para seguir con el asistente, o puedes optar por pulsar <CANCELAR> para no continuar"))
		self["key_red"] = StaticText(_("Cancelar"))
		self["key_green"] = StaticText(_("Continuar"))
		
	def exit(self):
		self.close()

	def paso2(self):
		self.session.openWithCallback(self.backupDone,BackupScreen, runBackup = True)
		

	def backupDone(self,retval = None):
		if retval is True:
			self.session.open(paso2)
		else:
			self.session.open(MessageBox, _("Backup failed."), MessageBox.TYPE_INFO, timeout = 10)

	def startRestore(self, ret = False):
		if (ret == True):
			self.exe = True
			self.session.open(RestoreScreen, runRestore = True)

class paso2(Screen):

	skin = """
		<screen position="center,center" size="1000,600" backgroundColor="white" title="Dreambox Rescue" >
		<widget source="header" render="Label" position="200,30" size="700,300" foregroundColor="black" backgroundColor="white" font="Regular; 40" halign="left" transparent="1" />
		<widget source="contenido" render="Label" position="200,200" size="700,300" foregroundColor="#848484" backgroundColor="white" font="Regular; 30" halign="left" transparent="1" />
		<eLabel name="line" position="200,490" size="750,1" backgroundColor="#aba7a6" />
		<ePixmap name="menu" position="5,5" size="158,600" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/rescue/imagenes/menu.png" zPosition="-5" />
		<ePixmap name="continuar" position="750,520" size="230,61" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/rescue/imagenes/green.png" zPosition="-5" />
		<ePixmap name="salir" position="190,520" size="230,61" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/rescue/imagenes/red.png" zPosition="-5" />
		<widget source="key_green" render="Label" position="770,530" size="200,50" zPosition="1" font="Regular; 30" transparent="1" foregroundColor="white" noWrap="1" />
		<widget source="key_red" render="Label" position="270,530" size="200,50" zPosition="1" font="Regular; 30" transparent="1" foregroundColor="white" noWrap="1" />
		</screen>"""
	
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.skinName = "dreambox_rescue"
		self.setTitle(_("Asistente Dreambox Rescue"))
		self.indexpos = None
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.paso4,
			
			
		})
		self["header"] = StaticText(_("El asistente de Mode Rescue ha finalizado"))
		self["contenido"] = StaticText(_("Se ha creado copia seguridad de configuracion en unidad montada, dentro de carpeta <BACKUP>, ahora vamos a realizar el ultimo paso, ahora debe pulsar <TERMINAR> y el receptor se reiniciara automaticamente en modo rescue, apareciendo en la pantalla de su televisor la IP a la que se debe conectar desde navegador de su ordenador,si desea cancelar esta operacion <CANCELAR>"))
		self["key_red"] = StaticText(_("Cancelar"))
		self["key_green"] = StaticText(_("Terminar"))
		
	def exit(self):
		self.close()

	def paso4(self):
		os.system("to-the-rescue")


class ayuda(Screen):

	skin = """
		<screen position="center,center" size="1000,600" backgroundColor="white" title="Dreambox Rescue" >
		<widget source="header" render="Label" position="200,30" size="700,300" foregroundColor="black" backgroundColor="white" font="Regular; 40" halign="left" transparent="1" />
		<widget source="contenido" render="Label" position="200,200" size="700,300" foregroundColor="#848484" backgroundColor="white" font="Regular; 30" halign="left" transparent="1" />
		<eLabel name="line" position="200,490" size="750,1" backgroundColor="#aba7a6" />
		<ePixmap name="menu" position="5,5" size="158,600" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/rescue/imagenes/menu.png" zPosition="-5" />
		<ePixmap name="salir" position="190,520" size="230,61" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/rescue/imagenes/red.png" zPosition="-5" />
		<widget source="key_red" render="Label" position="270,530" size="200,50" zPosition="1" font="Regular; 30" transparent="1" foregroundColor="white" noWrap="1" />
		<widget source="HardwareLabel" render="Label" position="460,135" zPosition="2" size="180,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#03307dc3" transparent="1" />
		<widget source="Hardware" render="Label" position="675,135" zPosition="2" size="390,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		
		</screen>"""

	
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.skinName = "dreambox_rescue"
		self.setTitle(_("Asistente Dreambox Rescue"))
		self.indexpos = None
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			
			
			
		})

		self["key_red"] = StaticText(_("Cancelar"))
		self["header"] = StaticText(_("Ayuda sobre Asistente configuracion Dreambox"))
		self["contenido"] = StaticText(_("La utilidad Rescue tiene la finalidad de poner su receptor facilmente en modo rescue para realizar la instalacion de una imagen desde su navegador web, recuerde que las imagenes para la instalacion deben ser con extension <<.tar.xz>>, asi como su receptor debe estar conectado a la red interna y tener montado un usb o disco duro para la realizacion del backup"))
		
		
		
	def exit(self):
		self.close()

			
	
	

def main(session, **kwargs):
	session.open(dreambox_rescue)
	
######################################################################################
def sessionstart(reason,session=None, **kwargs):
	if reason == 0:
		pTools.gotSession(session)
######################################################################################

def Plugins(**kwargs):
	list = [PluginDescriptor(name=_("Dreambox Rescue"), description=_("Activar modo Rescue Dreambox"), where = [PluginDescriptor.WHERE_PLUGINMENU], icon="rescue.png", fnc=main)]
	
	return list
