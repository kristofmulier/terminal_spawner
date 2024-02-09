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

# Repo overview

This repository contains two Python applications: the **Parent App** and **Child App**. Following Python files are involved:

 - **`parent_app.py`**: Main Python file from the Parent App.
 - **`child_app.py`**: Main Python file from the Child App.
 - **`build.py`**: Run this script to build *both* the parent and child applications with cx_freeze. The parent ends up in the folder `frozen_parent_app/`, the child in `frozen_child_app/`.
 - **`functions.py`**: A help-script containing Python functions used in both the parent and child apps.

![image](https://github.com/kristofmulier/terminal_spawner/assets/19362684/5a51d610-c1d8-4033-ada2-64271c6cd762)


# Build the Parent and Child Apps

To build both the **Parent App** and **Child App**, simply invoke the `build.py` script:

```sh
$ python build.py [--no-console]
```

This should then create the folders `frozen_parent_app/` and `frozen_child_app/`:

![image](https://github.com/kristofmulier/terminal_spawner/assets/19362684/714f95a3-4914-4480-8b42-fcd5f4a1bdf5)


You can choose to add the `--no-console` parameter when invoking the build script. This parameter should only be used on Windows. It results in passing `base = 'Win32GUI'` to cx_freeze. We'll see further on that the addition of this parameter will have an important impact on the final behavior of the application!

# Launch the Parent App

To launch the **Parent App**, simply invoke it with Python:

```sh
$ python parent_app.py
```
