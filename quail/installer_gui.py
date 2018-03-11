#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton, QApplication)
from PyQt5.QtGui import QFont    
from .installer import Installer

class Gui(QWidget):
    def __init__(self, installer):
        super().__init__()
        self.installer = installer
        self.initUI()
        
    def initUI(self):
        
        QToolTip.setFont(QFont('SansSerif', 10))
        
        btn = QPushButton('Install', self)
        btn.clicked.connect(self.installer._installButton)
        btn.setToolTip('install the application')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Quail')    
        self.show()

class InstallerGui(Installer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def install(self):
        app = QApplication([])
        gui = Gui(self)
        sys.exit(app.exec_())
    
    def _installButton(self):
        super().install()
