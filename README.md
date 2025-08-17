Spyderman
=========

A launcher for the Spyder IDE that lets you set the python interpreter at launch.
Looks for Spyder's transient.ini config file in the user's home directory, and modifies the
interpreter path prior to launching the IDE.

Note: If the program can't find the .ini file, it will fail. You will need to have
launched Spyder normally at least once so the files are available for this tool to
modify.

To use, make sure you have Spyder installed and available on your PATH.
You will also need to manually set to "use the following
interpreter" in Spyder's preferences. 

```
uv tool install spyder
```

Install this package as a tool

```
uv tool install https://github.com/d-c-gray/spyderman.git
```

From the root of a project that contains a virtual environment:

```
spyderman
```

You may need to restart the kernel in the IDE for the changes to take effect with `CTRL` + `.`