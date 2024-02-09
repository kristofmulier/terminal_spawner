# terminal_spawner

Spawning a child process from a parent in Python (using the `subprocess` module) is not a walk in the park. There are lots of variables to take into account:

 - Are you running on Windows or Linux?
 - Is the parent process a live Python script (invoked directly with your Python interpreter from a console)? Or is it a frozen executable?
 - How about the child?
 - Should the child process "die" once the parent stops?
 - Should the child process launch its own console?
 - ...

![image](https://github.com/kristofmulier/terminal_spawner/assets/19362684/1ef73b71-50dd-4e5b-9dc9-703a72d78c7e)


To get a better grasp on the situation, I decided to create this `terminal_spawner` repository.

&nbsp;<br>
# 1. Repo overview

This repository contains two Python applications: the **Parent App** and **Child App**. Following Python files are involved:

 - **`parent_app.py`**: Main Python file from the Parent App.
 - **`child_app.py`**: Main Python file from the Child App.
 - **`build.py`**: Run this script to build *both* the parent and child applications with cx_freeze. The parent ends up in the folder `frozen_parent_app/`, the child in `frozen_child_app/`.
 - **`functions.py`**: A help-script containing Python functions used in both the parent and child apps.

![image](https://github.com/kristofmulier/terminal_spawner/assets/19362684/5a51d610-c1d8-4033-ada2-64271c6cd762)

&nbsp;<br>
# 2. Build the Parent and Child Apps

To build both the **Parent App** and **Child App**, simply invoke the `build.py` script:

```sh
$ python build.py [--no-console]
```

This should then create the folders `frozen_parent_app/` and `frozen_child_app/`:

![image](https://github.com/kristofmulier/terminal_spawner/assets/19362684/714f95a3-4914-4480-8b42-fcd5f4a1bdf5)

You can choose to add the `--no-console` parameter when invoking the build script. This parameter should only be used on Windows. It results in passing `base = 'Win32GUI'` to cx_freeze. We'll see further on that the addition of this parameter will have an important impact on the final behavior of the application!

&nbsp;<br>
# 3. Launch the Parent App

## 3.1 Launch as Live Python Script

To launch the **Parent App**, simply invoke it with Python:

```sh
$ python parent_app.py [--foo] [--bar "some text"]
```

You can add two arguments if you wish to do so:
- `--foo`: An optional argument of boolean nature. Either it's present or absent.
- `--bar`: An optional argument that expects a string value.

A simple PyQt6 application starts and prints the arguments you passed - among other things:

![image](https://github.com/kristofmulier/terminal_spawner/assets/19362684/3e6b8739-5e19-4d38-a46f-beb3fdfa6260)

## 3.2 Launch as Executable

Alternatively, you can launch the **Parent App** as a (frozen) executable. Make sure you run the `build.py` script first (see previous chapter). Then navigate into the `frozen_parent_app/` folder and launch the executable from there:

```sh
$ cd frozen_parent_app
$ parent_app.exe [--foo] [--bar "some text"]
```

Again, you can add the `foo` and/or `bar` arguments if you wish. The application starts. This time, the app recognizes that it's running from an executable and shows that by setting its `Frozen` value `True`:

![image](https://github.com/kristofmulier/terminal_spawner/assets/19362684/d00b0341-1a79-442b-b4e3-3b8da96e2a25)

Also, the app colors itself blue to point out that it's ... frozen!

&nbsp;<br>
# 4. Launch the Child App

You can launch the **Child App** in the exact same way as you did for the **Parent App**: either as a live Python script or by invoking its (frozen) executable after a build. But then you'd be missing the point. The whole idea of the **terminal_spawner** project is that you launch the child application from within the parent.

## 4.1 Launch as Live Python Script vs Executable

Suppose the **Parent App** is already running. You'll see two buttons at the bottom:

![image](https://github.com/kristofmulier/terminal_spawner/assets/19362684/acd418a3-1754-46d5-ae22-05e2272c2413)

The first one looks for the child's Python script and runs it as such - invoking your default Python interpreter. The second button searches for the child's application executable in the `frozen_child_app/` subfolder and launches it from there.

## 4.2 Checkboxes

With the checkboxes, you can modify the behavior:

![image](https://github.com/kristofmulier/terminal_spawner/assets/19362684/9781f45c-805a-4a9d-ad13-bbc4b31d332e)

 - **Pass own `foo` and `bar` args to child:** This option is straightforward. Check it to pass the arguments given to the parent also to the child when it spawns.

 - **Run waitfunc() after spawning child:** The `subprocess.Popen()` function returns a subprocess-object. Check this box if you want to invoke the `wait()` function from that subprocess-object right after creating it.

 - **Quit after spawning child:** Check this box if you want the parent application to quit immediately after spawning the child (or after spawning and running the `wait()` function - see previous box). This is a very interesting experiment. It's basically what we do in Embeetle when switching from the main app to the updater tool - and back. The experiment succeeds if the child app stays alive even though the parent app disappears.

&nbsp;<br>
# 5. The --no-console Parameter

Remember the way you could build both the parent and child apps:

```sh
$ python build.py [--no-console]
```

If you add `--no-console` here, the argument `base = 'Win32GUI'` is passed to cx_freeze. This has a profound effect on the behavior of the frozen app. The button `PRINT INFO TO CONSOLE` no longer works - which is pretty normal. However, it also causes the app to crash when you try to spawn a child!

&nbsp;<br>
# 6. How the Parent Spawns its Child

The code to spawn a child process is all in `functions.py`. As you will see, this goes further than simply invoking `supbrocess.Popen()`. There's a whole mechanism to not merely launch the child application, but *launch it in a console*. For Embeetle this is important. The child application doesn't necessarily have a GUI. For example - the Beetle Updater Tool is a terminal-only application.

The main function says it all:

```python
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
    [...]
```

The function `spawn_new_terminal()` needs two arguments:
 - `script_or_exe_path`: The path to the script or executable to be run.
 - `argv`: The arguments to be passed to the script or executable.

The function tries to be as generic as possible. You can pass it a Python script, an executable or even a shell script. It will figure out what it gets and act accordingly. Then it launches said script/exe as a child process in its own dedicated console. On Windows that would be the standard `CMD` console. On Linux it looks for what's available.
