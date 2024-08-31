![Screenshot from 2024-08-31 08-29-54](https://github.com/user-attachments/assets/c2183d2f-c8c1-4ade-9fdb-5c0f2d29dd8a)

# LXPPAL is under development. Information will populate here in the coming weeks.
To install it, place "LX assistant.desktop" into ".local/share/applications/"
inside the file (text editor), replace "Your-home-folder-name-here" with the name of your home folder. 
And put the other files in the home folder.

Finally, make the command "LXM.sh" go on autostart.
Dependencies: python3, python3-gi, python3-socket, python3-webbrowser, python3-subprocess,python3-threading, python3-difflib, bs4-beautifulsoup, googlesearch ---- if you are using the latest version of LX OS 3.0, you shouldn't have to install any of the dependincies shown execpt in bold.

# But it didn't work!
-
It's ok. Several things may have happened, but to be sure of what happened, run LXM.sh direcly from the terminal.
Observe any errors. If its saying things like:

   Traceback (most recent call last):
   File "/home/password-is-513720lx/myapp.py", line 1, in <module>
    import gi
   ModuleNotFoundError: No module named 'gi'

This could indicate dependencies not being found. Try to install all dependencies before moving on.
If it's saying things like:

   Traceback (most recent call last):
   File "/home/password-is-513720lx/LXM0.2.py", line 108, in <module>
    start_server()
   File "/home/password-is-513720lx/LXM0.2.py", line 99, in start_server
    server.bind(('localhost', 9999))
   OSError: [Errno 98] Address already in use

This could indicate that there is already an LX agent running on your computer, or some other localhost app, at the same time. The only way to use them both at a time to to change the port on the LXPPal. That is not feasible right now, but if you are up for the challenge, go into both .py files and change the number "9999" to something else - 9998?
This will make both of them work at the same time.

# LX, I CAN'T INSTALL PYTHON DEPENDENCIES!!!!

If , when you go to install the dependencies (e.g, you run "pip install wikipiedia-api") you get something like this:

    error: externally-managed-environment

    × This environment is externally managed
    ╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    If you wish to install a non-Debian packaged Python application,
    it may be easiest to use pipx install xyz, which will manage a
    virtual environment for you. Make sure you have pipx installed.
    
    See /usr/share/doc/python3.12/README.venv for more information.

   note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
   hint: See PEP 668 for the detailed specification.

first. try using apt (or whatever your package manager is) with python3-xyz, where xyz is the dependencie(s) you want to install. If that gives you something like this:

   Reading package lists... Done
   Building dependency tree... Done
   Reading state information... Done
   E: Unable to locate package python3-xyz

Then you may have to create a vurtual envirorment and run the LXM0.2.py script in there. 
Run this command to create a vurtual enviorment:

   python -m venv /path/to/new/virtual/environment

Replace "path/to/new/vurtual/environment" with the location on your hard drive you'd like to put it in.
You may have to run it with sudo (sudo python -m venv /path/to/new/virtual/environment), where it'll ask for your password first.
Once you've done that, go ahead and install your dependencies. It should now work as intended. Now, in the LXM.sh file, place this command: "soruce myenv/bin/activate" into the 5th line of text. It should look like this when finished:

   #!/bin/bash
   .# First command
   python3 myapp.py
   .# Place the "soruce myenv/bin/activate" Below this text.
   soruce myenv/bin/activate
   .# Place the "source myenv/bin/activate" on top of this text..

   python3 LXM0.2.py
   .# Second command

# That's all, folks!
Have fun with your new lightwheight AI assistant!
And remember, ||LX Corp is a part of the future.||

Cc Copyright 2024-2025 LX Corp. All rights reserved.
