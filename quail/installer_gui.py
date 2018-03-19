#!/usr/bin/python3

import sys
from PyQt5.QtCore import (QObject, QThread, pyqtSlot, pyqtSignal)
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton, QApplication, QLabel, QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QFont    
from .installer import Installer

class Gui(QWidget):
    def __init__(self, installer, app):
        super().__init__()
        self.installer = installer
        self.app = app
        self._initUI()
        self.thread = QThread()
        
    def _initUI(self):
        
        self.state = QLabel('Not installed', self)

        self.btn = QPushButton('Install', self)
        self.btn.clicked.connect(self._startInstall)
        
        self.btn_exit = QPushButton('Exit', self)
        self.btn_exit.clicked.connect(self._exit)
        
        hbox_bottom = QHBoxLayout()
        hbox_bottom.addWidget(self.btn)
        hbox_bottom.addWidget(self.btn_exit)
        
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.state)
        vbox.addLayout(hbox_bottom)
        self.setLayout(vbox)
        
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Quail')
        
        self.installer.sig_done.connect(self._on_install_done)
        self.app.aboutToQuit.connect(self._atexit)
        self.show()
        
    def _startInstall(self):
        self.btn.setDisabled(True)
        self.btn_exit.setDisabled(True)
        self.state.setText('Installing...')
        self.installer.moveToThread(self.thread)
        self.thread.started.connect(self.installer._runInstall)
        self.thread.start()
    
    def _exit(self):
        self._on_exit()
        self.app.quit()
    
    def _on_install_done(self):
        self.state.setText('Installed')
        self.btn_exit.setEnabled(True)
        self._on_exit()
    
    def _atexit(self):
        self._on_exit()
    
    def _on_exit(self):
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()


class InstallerGui(Installer, QObject):
    
    sig_done = pyqtSignal()

    def __init__(self, *args, **kwargs):
        Installer.__init__(self, *args, **kwargs)
        QObject.__init__(self)
        
    def install(self):
        app = QApplication([])
        gui = Gui(self, app)
        app.exec_()
    
    def _runInstall(self):
        Installer.install(self)
        self.sig_done.emit()

