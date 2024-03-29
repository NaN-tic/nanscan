##############################################################################
#
# Copyright (c) 2008 Albert Cervera i Areny <albert@nan-tic.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import base64
from Koo import Rpc
from NanScan.Scanner import *
from NanScan.ScanDialog import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.uic import *
from Koo.Plugins import Plugins

def scan(datas):
	s = ScanDialog()
        s.scan()
        s.exec_()

class RpcSaveThreaded(SaveThreaded):
	def run(self):
		tempFile = QTemporaryFile()
		tempFile.setAutoRemove( False )
		tempFile.open( QIODevice.WriteOnly )
		self.item.image.save( tempFile, "PNG" )
		fileName = unicode( tempFile.fileName() )
		tempFile.close()
	
		datas = open( fileName, 'rb' ).read()
		datas = base64.encodestring(datas)
		tempFile.remove()
	
		fields = {}
		fields['name'] = unicode( self.item.name )
		fields['datas'] = datas
		id = Rpc.session.execute('/object', 'execute', 'nan.document', 'create', fields )
		if id:
			self.error = False

Plugins.register( 'scanner', 'nan.document', _('Scan Documents'), scan )
