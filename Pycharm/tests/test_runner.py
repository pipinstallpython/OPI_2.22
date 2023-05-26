#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import test_routes

prodTestSuite = unittest.TestSuite()
prodTestSuite.addTest(unittest.makeSuite(test_routes.RoutesTests))
runner = unittest.TextTestRunner(verbosity=2)
runner.run(prodTestSuite)