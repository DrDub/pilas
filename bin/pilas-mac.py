#!/usr/bin/python
# -*- encoding: utf-8
#
# Este script permite crear una aplicación para Mac OS X con
# el siguiente comando:
#
#     python setup-mac.py py2app
#
# La aplicación se generará dentro del directorio dist.

import sys
import os

sys.path.append('..')

from optparse import OptionParser
import six
import pilas

analizador = OptionParser()

analizador.add_option("-i", "--interprete", dest="interprete",
        action="store_true", default=False,
        help="Abre el interprete interactivo")

(opciones, argumentos) = analizador.parse_args()

if argumentos:
    os.chdir(os.path.dirname(argumentos[0]))
    sys.exit(six.exec_(compile(open(argumentos[0]).read(), argumentos[0], 'exec')))

if opciones.interprete or '-i' in sys.argv:
    from PyQt4 import QtGui
    app = QtGui.QApplication(sys.argv[:1])
    app.setApplicationName("pilas-engine 2")
    pilas.abrir_interprete(do_raise=True)
elif argumentos:
    sys.exit(six.exec_(compile(open(argumentos[0]).read(), argumentos[0], 'exec')))
else:
    pilas.abrir_asistente()
