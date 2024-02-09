# -*- coding: utf-8 -*-
"""
Copyright 2018-2023 Johan Cockx, Matic Kukovec and Kristof Mulier.
"""
# SUMMARY:
# This is a simply PyQt6 application that creates a window with a button.
from __future__ import annotations
from typing import *
import sys, os, inspect
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
q = "'"

def get_script_filepath() -> str:
    '''
    Get the path to the script or executable that is running right now.
    '''
    if is_frozen():
        # Frozen (executing via cx_freeze or Nuitka)
        script_filepath = os.path.realpath(sys.executable).replace('\\', '/')
    else:
        script_filepath = os.path.realpath(
            inspect.getfile(
                inspect.currentframe()
            )
        ).replace('\\', '/')
    return script_filepath

def get_terminal_spawner_folderpath() -> str:
    '''
    Get the path to the 'terminal_spawner' folder.
    '''
    folderpath = os.path.dirname(get_script_filepath()).replace('\\', '/')
    if folderpath.endswith('terminal_spawner'):
        pass
    else:
        folderpath = os.path.dirname(folderpath).replace('\\', '/')
    assert folderpath.endswith('terminal_spawner')
    return folderpath

def is_frozen() -> bool:
    '''
    Return whether the script or executable running right now is frozen.
    '''
    return getattr(sys, 'frozen', False)

def get_info() -> Dict[str, str]:
    '''
    Return info about the way this app runs.
    '''
    return {
        # Path to the script or executable running right now
        'This file is running from: '.ljust(30): str(get_script_filepath()),

        # Is the script or executable running right now frozen?
        'Frozen: '.ljust(30): str(is_frozen()),
    }

def print_info() -> None:
    '''
    Function to be called when the button is clicked.
    '''
    #$ Print info
    for k, v in get_info().items():
        print(f'{k} {v}')
    return

# Main application class
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        # Set the main window size
        self.setMinimumSize(QSize(1000, 300))
        if is_frozen():
            self.setStyleSheet('background-color: #729fcf;')
        else:
            self.setStyleSheet('background-color: #d3d7cf;')

        # Set the window title
        self.setWindowTitle('CHILD APP')

        # Set the font to monospace, size 12
        monospace_font = QFont('Monospace')
        monospace_font.setStyleHint(QFont.StyleHint.Monospace)
        monospace_font.setPointSize(12)

        # Create central widget and layout
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        # Prevent the widgets from stretching vertically by adding a stretch at the end of the layout
        layout.addStretch(1)

        #& Labels
        # Create labels and text fields, placing them next to each other
        for label_text, text_content in get_info().items():
            # Create a horizontal layout for each label-text field pair
            horizontal_layout = QHBoxLayout()

            label = QLabel(str(label_text), self)
            label.setFont(monospace_font)
            text_field = QLineEdit(str(text_content), self)
            text_field.setFont(monospace_font)
            text_field.setReadOnly(True)
            text_field.setStyleSheet('background-color: #ffffff;')

            # Add the label and text field to the horizontal layout
            horizontal_layout.addWidget(label)
            horizontal_layout.addWidget(text_field)

            # Add the horizontal layout to the main vertical layout
            layout.insertLayout(layout.count() - 1, horizontal_layout)

        #& Buttons
        #$ PRINT INFO
        self.info_btn: QPushButton = QPushButton(' PRINT INFO TO CONSOLE', self)
        self.info_btn.setMinimumHeight(70)
        self.info_btn.setMaximumWidth(400)
        self.info_btn.setFont(monospace_font)
        self.info_btn.setStyleSheet('text-align:left; background-color: #eeeeec;')
        self.info_btn.clicked.connect(print_info)

        # Add stretch to push everything to the top, then add the button
        layout.addStretch(1)
        layout.addWidget(self.info_btn)

        # Adjust size to content
        self.adjustSize()

def main() -> int:
    '''
    Main entry point.
    '''
    # Create the application instance
    app: QApplication = QApplication(sys.argv)
    # Create the main window instance
    window: MainWindow = MainWindow()
    window.show()
    # Start the application's event loop and exit
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())