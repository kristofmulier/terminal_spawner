# -*- coding: utf-8 -*-
"""
Copyright 2018-2023 Johan Cockx, Matic Kukovec and Kristof Mulier.
"""
# SUMMARY:
# This script should be invoked to build the main application in 'main.py' with cx_freeze.
from __future__ import annotations
import sys, os, platform, functions, shutil, inspect
q = "'"

def build(main_script_path:str,
          executable_name:str,
          output_freeze_folder:str,
          ) -> None:
    '''
    Build the main python script with cx_freeze into an executable.

    :param main_script_path:     The path to the main python script.

    :param executable_name:      The name of the executable to be created. Should be '<application>'
                                 or '<application>.exe'.

    :param output_freeze_folder: The folder where the build output will be placed.
    '''
    import cx_Freeze

    #& Delete previous build
    if os.path.isdir(output_freeze_folder):
        shutil.rmtree(output_freeze_folder)

    #& Additional modules
    modules = [
        'PyQt6',
        'PyQt6.Qsci',
        'PyQt6.QtTest',
        'PyQt6.QtWebEngineWidgets',
    ]
    if platform.system().lower() == 'windows':
        modules.extend(
            [
                'win32api',
                'win32con',
                'win32file',
                'winpty',
                'winshell',
                'winreg',
            ]
        )
    else:
        modules.extend(
            [
                'ptyprocess',
                'pwd',
            ]
        )

    #& Executables
    executables = [
        cx_Freeze.Executable(
            main_script_path,
            init_script = None,
            base        = 'Win32GUI' if platform.system().lower() == 'windows' else None,
            icon        = f'{os.path.dirname(main_script_path)}/icon.ico'.replace('\\', '/'),
            target_name = executable_name,
        ),
    ]

    #& Search paths
    search_paths = [p.replace('\\', '/') for p in sys.path]
    search_paths.append(os.path.dirname(main_script_path).replace('\\', '/'))

    #& Invoke Freezer()
    freezer = cx_Freeze.Freezer(
        executables   = executables, # noqa
        includes      = modules,
        excludes      = ['tkinter'],
        replace_paths = [],
        compress      = True,
        optimize      = 2,
        path          = search_paths,
        target_dir    = output_freeze_folder,
        include_files = [],
        zip_includes  = [],
        silent        = False,
        include_msvcr = True,
    )
    freezer.freeze()
    return

if __name__ == '__main__':
    #$ Path to parent folder 'terminal_testapp'
    _terminal_testapp_folderpath = os.path.dirname(
        os.path.realpath(
            inspect.getfile(
                inspect.currentframe()
            )
        )
    ).replace('\\', '/')

    #$ Build Parent App
    build(
        main_script_path     = f'{_terminal_testapp_folderpath}/parent_app.py',
        executable_name      = 'parent_app.exe' if platform.system().lower() == 'windows' else 'parent_app',
        output_freeze_folder = f'{_terminal_testapp_folderpath}/frozen_parent_app'.replace('\\', '/'),
    )

    #$ Build Child App
    build(
        main_script_path     = f'{_terminal_testapp_folderpath}/child_app.py',
        executable_name      = 'child_app.exe' if platform.system().lower() == 'windows' else 'child_app',
        output_freeze_folder = f'{_terminal_testapp_folderpath}/frozen_child_app'.replace('\\', '/'),
    )

    input('Press any key to exit ...')
    sys.exit(0)