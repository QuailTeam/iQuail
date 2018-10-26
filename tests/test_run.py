import unittest.mock
import os
import iquail
import tempfile
from contextlib import suppress
from unittest.mock import patch
from .base_test_case import BaseTestCase

class TestRun(BaseTestCase):

    @patch.object(iquail.controller.controller_console.ControllerConsole,
                    'press_to_exit')
    @patch.object(iquail.controller.controller_console.ControllerConsole,
                    '_ask_validate', return_value=True)
    def test_run_valid(self, mock_ask, mock_press):
            testargs = [self.path('Allum1.zip')]
            installer = iquail.Installer(
                name='TestQuail',
                icon='noicon',
                binary='allum1'
            )
            solution = iquail.SolutionLocal(self.path('Allum1'))
            with unittest.mock.patch('sys.argv', testargs):
                iquail.run(solution, installer)
                self.assertTrue(installer._registered())

            testargs = [self.path('Allum1.zip'), '--quail_uninstall']
            with unittest.mock.patch('sys.argv', testargs):
                iquail.run(solution, installer)
                self.assertFalse(installer._registered())

            self.assertEqual(mock_press.call_count, 2)
            self.assertEqual(mock_ask.call_count, 1)

    def test_run_solution_not_valid(self):
            testargs = [self.path('emptyfile')]
            installer = iquail.Installer(
                name='TestQuail',
                icon='noicon',
                binary='void'
            )
            solution = iquail.SolutionLocal(self.path('emptyfile'))
            with unittest.mock.patch('sys.argv', testargs):
                with suppress(iquail.errors.SolutionUnreachableError):
                    iquail.run(solution, installer)

    @patch.object(iquail.controller.controller_console.ControllerConsole,
                    '_ask_validate', return_value=True)
    @patch.object(iquail.controller.controller_console.ControllerConsole,
                    'press_to_exit')
    def test_remove_solution_not_found(self, mock_ask, mock_press):
            testargs = [self.path('emptyfile'), '--quail_uninstall']
            installer = iquail.Installer(
                name='TestQuail2',
                icon='noicon',
                binary='void'
            )
            solution = iquail.SolutionLocal(self.path('emptyfile'))
            with unittest.mock.patch('sys.argv', testargs):
                    iquail.run(solution, installer)

            self.assertEqual(mock_press.call_count, 1)
            self.assertEqual(mock_ask.call_count, 1)

    @patch('platform.system', return_value='Windows')
    def test_build_zip_valid(self, mock_windows):
            testargs = [self.path('Allum1.zip'), '--quail_build']
            installer = iquail.Installer(
                name='TestQuail',
                icon='noicon',
                binary='allum1'
            )
            solution = iquail.SolutionLocal(self.path('Allum1'))
            with unittest.mock.patch('sys.argv', testargs):
                    iquail.run(solution, installer)
