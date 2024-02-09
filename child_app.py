# -*- coding: utf-8 -*-
"""
Copyright 2018-2023 Johan Cockx, Matic Kukovec and Kristof Mulier.
"""
# SUMMARY:
# This is a simply PyQt6 application that creates a window with a button.
from __future__ import annotations
from typing import *
import sys, os, inspect, argparse
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
q = "'"
foo_value: bool = False
bar_value: Optional[str] = None
args_valid: bool = True

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

        # Arguments
        'sys.argv: '.ljust(30): '[\n' + ',\n'.join(f'    \'{item}\'' for item in sys.argv) + '\n]',

        # Original arguments
        'sys.orig_argv: '.ljust(30): '[\n' + ',\n'.join(f'    \'{item}\'' for item in sys.orig_argv) + '\n]',

        # System path
        'sys.path'.ljust(30): '[\n' + ',\n'.join(f'    \'{item}\'' for item in sys.path) + '\n]',

        # Is the script or executable running right now frozen?
        'Frozen: '.ljust(30): str(is_frozen()),

        # Foo argument
        'Foo argument: '.ljust(30): str(foo_value),

        # Bar argument
        'Bar argument: '.ljust(30): str(bar_value),
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
        if not args_valid:
            self.setStyleSheet('background-color: #fccccc;')
        else:
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

        #& Labels
        # Create labels and text fields, placing them next to each other
        if not args_valid:
            label = QLabel('Invalid arguments!', self)
            label.setFont(monospace_font)
            layout.addWidget(label)
            return
        for label_text, text_content in get_info().items():
            # Create a horizontal layout for each label-text field pair
            horizontal_layout = QHBoxLayout()

            #$ LABEL
            txt = str(label_text)
            label = QLabel(txt, self)
            label.setFont(monospace_font)

            #$ TEXT FIELD
            txt = str(text_content)
            if '\n' in txt:
                text_field = QPlainTextEdit(txt, self)
                n = txt.count('\n') + 1
                text_field.setMaximumHeight(
                    min(
                        300,
                        text_field.fontMetrics().lineSpacing() * n + 20,
                    )
                )
            else:
                text_field = QLineEdit(txt, self)
            text_field.setFont(monospace_font)
            text_field.setReadOnly(True)
            text_field.setStyleSheet('background-color: #ffffff;')

            # Add the label and text field to the horizontal layout
            horizontal_layout.addWidget(label)
            horizontal_layout.addWidget(text_field)

            # Add the horizontal layout to the main vertical layout
            layout.addLayout(horizontal_layout)
            continue

        #& Buttons
        #$ PRINT INFO
        self.info_btn: QPushButton = QPushButton(' PRINT INFO TO CONSOLE', self)
        self.info_btn.setMinimumHeight(70)
        self.info_btn.setMaximumWidth(400)
        self.info_btn.setFont(monospace_font)
        self.info_btn.setStyleSheet('text-align:left; background-color: #eeeeec;')
        self.info_btn.clicked.connect(print_info)

        # Add stretch to push everything to the top, then add the button
        layout.addStretch(5)
        layout.addSpacing(60)
        layout.addWidget(self.info_btn)

        # Adjust size to content
        self.adjustSize()
        return

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
    #$ Parse arguments
    parser = argparse.ArgumentParser(description='Child application.')
    parser.add_argument(
        '--foo',
        action = 'store_true',
        help   = 'A boolean flag. Present means True, absent means False.'
    )
    parser.add_argument(
        '--bar',
        type = str,
        help = 'A string argument'
    )
    try:
        args = parser.parse_args()
        foo_value = args.foo
        bar_value = args.bar
    except:
        args_valid = False

    #$ Run GUI and quit after
    sys.exit(main())