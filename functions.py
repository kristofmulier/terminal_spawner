# -*- coding: utf-8 -*-
"""
Copyright 2018-2023 Johan Cockx, Matic Kukovec and Kristof Mulier.
"""
# SUMMARY:
# Functions to be used by any script in the project.
from __future__ import annotations
from typing import *
import sys, os, subprocess, platform, time, shlex, shutil
q = "'"


#^                                       SPAWN NEW TERMINAL                                       ^#
#% ============================================================================================== %#
#%                                                                                                %#
#%                                                                                                %#
linux_shells = ('sh', 'bash', 'dash', 'zsh', 'ksh', 'fish', 'xonsh', 'nushell', )
linux_terminal_emulators = ('gnome-terminal', 'x-terminal-emulator', 'xterm', 'konsole',
                            'xfce4-terminal', 'qterminal', 'lxterminal', 'alacritty', 'rxvt',
                            'terminator', 'termit', )

def spawn_new_terminal(script_or_exe_path:str, argv:List[str], **kwargs) -> Callable:
    '''
    Spawn a new terminal and launch the given script (python or shell script) or executable in that
    terminal. This function returns a callable 'wait_function()' that the parent process (which
    invoked this function) can use to wait for the child process (which runs in the newly spawned
    terminal) to complete. That 'wait_function()' returns the 'returncode', which is 0 if all was
    good.

    :param script_or_exe_path:  The script (python or shell script) or executable to be launched in
                                the newly spawned terminal. For example:
                                  - 'C:/users/krist/child.py'  or '/home/krist/child.py'
                                  - 'C:/users/krist/child.bat' or '/home/krist/child.sh'
                                  - 'C:/users/krist/child.exe' or '/home/krist/child'

    :param argv:                The arguments to be passed to the script or executable. Do not
                                include the (path to the) script file or executable in here. Just
                                the arguments.
    '''
    if 'verbose' in kwargs:
        del kwargs['verbose']
    #& WINDOWS
    if platform.system().lower() == 'windows':
        #$ shell script
        if script_or_exe_path.endswith(('.cmd', '.bat')):
            return __spawn_terminal_windows(script_or_exe_path, argv, **kwargs)
        #$ python script
        if script_or_exe_path.endswith('.py'):
            return __spawn_terminal_windows(__get_python_executable(), [script_or_exe_path, *argv], **kwargs)
        #$ executable
        if script_or_exe_path.endswith('.exe'):
            return __spawn_terminal_windows(script_or_exe_path, argv, **kwargs)
        # Reaching this point, the file has no known extension. The file is probably an executable.
        return __spawn_terminal_windows(script_or_exe_path, argv, **kwargs)

    #& LINUX
    assert platform.system().lower() == 'linux'
    #$ shell script
    if script_or_exe_path.endswith('.sh'):
        return __spawn_terminal_linux(script_or_exe_path, argv, **kwargs)
    #$ python script
    if script_or_exe_path.endswith('.py'):
        return __spawn_terminal_linux(__get_python_executable(), [script_or_exe_path, *argv], **kwargs)
    #$ executable
    if script_or_exe_path.endswith('.exe'):
        # Normally, executables on Linux don't end in '.exe'. But you never know.
        return __spawn_terminal_linux(script_or_exe_path, argv, **kwargs)
    # Try to find shebang
    try:
        with open(script_or_exe_path, 'r', encoding='utf-8', newline='\n') as f:
            content = f.read()
        # Look for a shebang with a for-loop, to ignore empty lines at the start of the file. If
        # a non-empty line is found, and it is not a shebang, then stop looping.
        for line in content.splitlines():
            if line.strip() == '':
                continue
            #$ shell script
            if line.startswith(tuple(f'#!/bin/{s}' for s in linux_shells)):
                return __spawn_terminal_linux(script_or_exe_path, argv, **kwargs)
            if line.startswith(tuple(f'#!/usr/bin/{s}' for s in linux_shells)):
                return __spawn_terminal_linux(script_or_exe_path, argv, **kwargs)
            break
        # No shebang found
    except:
        # The file is probably not a script, but an executable
        pass
    #$ executable
    # Reaching this point, the file has no known extension, nor could a shebang be found. The
    # file is probably an executable.
    return __spawn_terminal_linux(script_or_exe_path, argv, **kwargs)

def __get_python_executable() -> str:
    '''
    Return the path to the python interpreter executable.
    '''
    interpreter_path:Optional[str] = None
    if getattr(sys, 'frozen', False):
        # Frozen, running as compiled code
        if platform.system().lower() == 'linux':
            # On Linux, first give 'python3' a try
            interpreter_path = shutil.which('python3')
        if interpreter_path is None:
            interpreter_path = shutil.which('python')
    else:
        # Running from interpreter
        interpreter_path = sys.executable
    assert interpreter_path is not None
    return interpreter_path.replace('\\', '/')

def __get_terminal_emulator_name_and_executable() -> Tuple[str, str]:
    '''
    Return the name and path to the default terminal emulator on this system. For example:
    ('gnome-terminal', '/usr/bin/gnome-terminal')
    '''
    assert platform.system().lower() == 'linux'
    for terminal in linux_terminal_emulators:
        if shutil.which(terminal):
            return str(terminal), str(shutil.which(terminal))
        continue
    raise RuntimeError('No terminal emulator found!')

def __spawn_terminal_windows(program:str, argv:List[str], **kwargs) -> Callable:
    '''

    '''
    #& RUN
    arguments = [program, *argv]
    print(
        f'subprocess.Popen(\n'
        f'    {arguments},'
        f'    creationflags = subprocess.CREATE_NEW_CONSOLE,\n'
        f'    {kwargs},\n'
        f')'
    )
    time.sleep(1)
    p = subprocess.Popen(
        arguments,
        creationflags = subprocess.CREATE_NEW_CONSOLE,
        **kwargs,
    )
    #& RETURN WAIT FUNCTION
    def wait_function() -> int:
        return p.wait()
    return wait_function

def __spawn_terminal_linux(program:str, argv:List[str], **kwargs) -> Callable:
    '''

    '''
    #& RUN
    terminal_name, terminal_path = __get_terminal_emulator_name_and_executable()
    # The 'gnome-terminal' requires a '--wait' argument to let it not return until its child process
    # has completed. Also, this terminal needs the '--' argument instead of '-e', which is depre-
    # cated.
    if terminal_name == 'gnome-terminal':
        arguments = [terminal_path, '--wait', '--', program, *argv]
        print(
            f'subprocess.Popen(\n'
            f'    {arguments},\n'
            f'    env={os.environ},'
            f'    {kwargs},\n'
            f')'
        )
        time.sleep(1)
        p = subprocess.Popen(
            arguments,
            env=os.environ,
            **kwargs,
        )
    # The 'xfce4-terminal' and 'terminator' terminal emulators don't work if you pass the program
    # and arguments as separate list elements. So you need to join them with shlex.
    elif terminal_name in ('xfce4-terminal', 'terminator'):
        arguments = [terminal_path, '-e', shlex.join([program, *argv])]
        print(
            f'subprocess.Popen(\n'
            f'    {arguments},\n'
            f'    env={os.environ},'
            f'    {kwargs},\n'
            f')'
        )
        time.sleep(1)
        p = subprocess.Popen(
            arguments,
            env=os.environ,
            **kwargs,
        )
    # For all other terminal emulators, the approach is the same.
    else:
        arguments = [terminal_path, '-e', program, *argv]
        print(
            f'subprocess.Popen(\n'
            f'    {arguments},\n'
            f'    env={os.environ},'
            f'    {kwargs},\n'
            f')'
        )
        time.sleep(1)
        p = subprocess.Popen(
            arguments,
            env=os.environ,
            **kwargs,
        )
    #& RETURN WAIT FUNCTION
    def wait_function() -> int:
        return p.wait()
    return wait_function
