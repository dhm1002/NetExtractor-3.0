# -*- coding: utf-8 -*-

from tst import TestUnitarios
from src import Controlador
import unittest

#Pruebas desactualizadas
#runner = unittest.TextTestRunner()
#result = runner.run(unittest.makeSuite(testUnitarios.testUnitarios))

Controlador.app.run(threaded=True)

