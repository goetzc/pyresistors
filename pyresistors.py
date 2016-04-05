#!/usr/bin/python3
"""
Calculate resistors value and tolerance by their color codes.
"""

import os
import sys
from time import sleep
from threading import Thread
from collections import OrderedDict

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QComboBox, QLabel, QHBoxLayout,
                             QVBoxLayout, QWidget)

PATH = os.path.dirname(os.path.abspath(sys.argv[0]))

class MainWindow(QWidget):
    """Generate the GUI in Qt"""
    def __init__(self):
        super().__init__()

        self.gui()

    def gui(self):
        self.setWindowTitle('Resistors Calculator')
        self.setWindowIcon(QIcon(os.path.join(PATH, 'icons','pyresistors.png')))

        # Layout
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()

        label_1 = QLabel("Choose resistor's colors")

        vbox.addWidget(label_1)
        vbox.addLayout(hbox)

        # Use custom colors because some Qt's color names look bad
        bands_colors = (('Black', '#000000'), ('Brown', '#844200'), ('Red', '#FF0000'), 
                        ('Orange', '#FF7F00'), ('Yellow', '#FFFF00'), ('Green', '#00FF00'), 
                        ('Blue', '#0000FF'), ('Violet', '#AA55FF'), ('Grey', '#808080'), 
                        ('White', '#FFFFFF'), ('Gold', '#DCBA00'), ('Silver', '#DBDBDB'))
        bands_colors = OrderedDict(bands_colors)

        tolerance_colors = ('Brown', 'Red', 'Green', 'Blue', 'Violet', 
                            'Grey', 'Gold', 'Silver', 'No color')

        # Create four comboboxes
        self.combobox = (('combo_1', None), ('combo_2', None), ('combo_3', None), ('combo_4', None))
        self.combobox = OrderedDict(self.combobox)

        # First add the objects to the odict
        for k in self.combobox.keys():
            self.combobox[k] = QComboBox()
            hbox.addWidget(self.combobox[k])

            if k in ('combo_1', 'combo_2'):
                for c in tuple(bands_colors)[:-2]:
                    self.combobox[k].addItem(self.colorIcon(bands_colors[c]), c)
            elif k == 'combo_3':
                [self.combobox[k].addItem(self.colorIcon(val), key) for key, val in bands_colors.items()]
            elif k == 'combo_4':
                for c in tolerance_colors:
                    if c == 'No color':
                        self.combobox[k].addItem(c)
                    else:
                        self.combobox[k].addItem(self.colorIcon(bands_colors[c]), c)
        
        # Then connect the signal and slot
        for k in self.combobox.keys():
            self.combobox[k].currentIndexChanged.connect(self.calculate)


        # Ω (Ohm)
        self.equal = QLabel('=')
        self.total = QLabel()
        self.tolerance = QLabel()
        hbox.addWidget(self.total)
        hbox.addWidget(self.tolerance)

    def calculate(self):
        # Resistor value in Ohm
        digit1 = str(self.combobox['combo_1'].currentIndex())
        digit2 = str(self.combobox['combo_2'].currentIndex())
        digit3 = self.combobox['combo_3'].currentIndex()

        digits = int(digit1 + digit2)
        multi = " "

        if digit3 in (0, 1, 2):
            value = digits * 10 ** digit3
        elif digit3 in (3, 4, 5):
            multi = ' k'
            if digit3 == 3:
                value = digits
            elif digit3 == 4:
                value = digits * 10 ** 1
            elif digit3 == 5:
                value = digits * 10 ** 2
        elif digit3 in (6, 7, 8):
            multi = ' M'
            if digit3 == 6:
                value = digits
            elif digit3 == 7:
                value = digits * 10 ** 1
            elif digit3 == 8:
                value = digits * 10 ** 2
        elif digit3 == 9:
            multi = ' G'
            value = digits
        elif digit3 == 10:
            value = digits * 10 ** -1
        elif digit3 == 11:
            value = digits * 10 ** -2

        self.total.setText('= ' + str(value) + multi + 'Ω')

        # Tolerance ±X%
        digit4 = self.combobox['combo_4'].currentIndex()
        
        tolerance = ('1% (F)', '2% (G)', '0.5% (D)', '0.25% (C)', '0.1% (B)', 
                     '0.05% (A)', '5% (J)', '10% (K)', '20% (M)')

        self.tolerance.setText('± ' + tolerance[digit4])

    def colorIcon(self, color):
        pix = QPixmap(32,32)
        pix.fill(QColor(color))
        return QIcon(pix)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
