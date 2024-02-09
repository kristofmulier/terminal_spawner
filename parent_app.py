# -*- coding: utf-8 -*-
"""
Copyright 2018-2023 Johan Cockx, Matic Kukovec and Kristof Mulier.
"""
# SUMMARY:
# This is a simply PyQt6 application that creates a window with a button.
from __future__ import annotations
from typing import *
import sys, os, inspect, platform, functions
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

def spawn_child_app_python(wait_after_spawn:bool, quit_after_spawn:bool) -> None:
    '''
    Function to be called when the button is clicked.
    '''
    print(quit_after_spawn)
    #$ Spawn child app python script
    print(f'Spawning child app python script ...')
    print(f'Wait after spawn: {wait_after_spawn}')
    print(f'Quit after spawn: {quit_after_spawn}')
    wait_func = functions.spawn_new_terminal(
        script_or_exe_path = f'{get_terminal_spawner_folderpath()}/child_app.py',
        argv = ['--foo', '--bar'],
    )
    if wait_after_spawn:
        wait_func()
    if quit_after_spawn:
        sys.exit(0)
    return

def spawn_child_app_exe(wait_after_spawn:bool, quit_after_spawn:bool) -> None:
    '''
    Function to be called when the button is clicked.
    '''
    print(quit_after_spawn)
    #$ Spawn child app executable
    print(f'Spawning child app executable ...')
    print(f'Wait after spawn: {wait_after_spawn}')
    print(f'Quit after spawn: {quit_after_spawn}')
    executable_path = f'{get_terminal_spawner_folderpath()}/frozen_child_app/child_app'
    if platform.system().lower() == 'windows':
        executable_path += '.exe'
    wait_func = functions.spawn_new_terminal(
        script_or_exe_path = executable_path,
        argv = ['--foo', '--bar'],
    )
    if wait_after_spawn:
        wait_func()
    if quit_after_spawn:
        sys.exit(0)
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
        self.setWindowTitle('PARENT APP')

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
        #$ CHECKBOX
        self.wait_checkbox = QCheckBox('Run waitfunc() after spawning child', self)
        self.wait_checkbox.setFont(monospace_font)
        self.wait_checkbox.setStyleSheet('text-align:left;')
        self.wait_checkbox.setChecked(False)

        self.quit_checkbox = QCheckBox('Quit after spawning child', self)
        self.quit_checkbox.setFont(monospace_font)
        self.quit_checkbox.setStyleSheet('text-align:left;')
        self.quit_checkbox.setChecked(False)

        #$ PRINT INFO
        self.info_btn: QPushButton = QPushButton(' PRINT INFO TO CONSOLE', self)
        self.info_btn.setMinimumHeight(60)
        self.info_btn.setMaximumWidth(400)
        self.info_btn.setFont(monospace_font)
        self.info_btn.setStyleSheet('text-align:left; background-color: #eeeeec;')
        self.info_btn.clicked.connect(print_info)

        #$ SPAWN CHILD APP PYTHON SCRIPT
        self.python_spawn_btn: QPushButton = QPushButton(' SPAWN CHILD (PYTHON)', self)
        self.python_spawn_btn.setMinimumHeight(60)
        self.python_spawn_btn.setMaximumWidth(400)
        self.python_spawn_btn.setFont(monospace_font)
        self.python_spawn_btn.setStyleSheet('text-align:left; background-color: #eeeeec;')
        self.python_spawn_btn.clicked.connect(
            lambda: spawn_child_app_python(
                self.wait_checkbox.isChecked(),
                self.quit_checkbox.isChecked(),
            )
        )

        #$ SPAWN CHILD APP EXECUTABLE
        self.exe_spawn_btn: QPushButton = QPushButton(' SPAWN CHILD (EXECUTABLE)', self)
        self.exe_spawn_btn.setMinimumHeight(60)
        self.exe_spawn_btn.setMaximumWidth(400)
        self.exe_spawn_btn.setFont(monospace_font)
        self.exe_spawn_btn.setStyleSheet('text-align:left; background-color: #eeeeec;')
        self.exe_spawn_btn.clicked.connect(
            lambda: spawn_child_app_exe(
                self.wait_checkbox.isChecked(),
                self.quit_checkbox.isChecked(),
            )
        )

        # Add stretch to push everything to the top, then add the button
        layout.addStretch(5)
        layout.addSpacing(60)
        layout.addWidget(self.wait_checkbox)
        layout.addWidget(self.quit_checkbox)
        layout.addStretch(1)
        layout.addSpacing(20)
        layout.addWidget(self.info_btn)
        layout.addWidget(self.python_spawn_btn)
        layout.addWidget(self.exe_spawn_btn)

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