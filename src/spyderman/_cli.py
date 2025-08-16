import configparser
import click
import json
from pathlib import Path
from enum import Enum
from subprocess import run
__all__ = ["spyderman"]

class SPYDER_CONFIG_PATHS(Enum):
    LINUX = Path.home()/".config/spyder-py3/config/transient.ini"

class COMMON_VENV_PATHS(Enum):
    LINUXDOTVENV = Path('.venv/bin/python')
    LINUX = ('/bin/python')

MAXL_COMMON_PATHS = max([len(str(p.value)) for p in COMMON_VENV_PATHS])
MAXL_COMMON_SPYDER = max([len(str(p.value)) for p in SPYDER_CONFIG_PATHS])

class EMOJIS(Enum):
    CHECK = "✓"
    X = "✗"

VERBOSE = False
def cprint(*args, **kwargs):
    if VERBOSE:
        print(*args,**kwargs)


@click.command(name = 'spyderman')
@click.option('--project-dir','-pd', type = Path, default = Path.cwd())
@click.option('--version','-v',type = str, help = "What version of Spyder to use. latest or semantic version (i.e 6, 5.9, etc)", default = "latest")
@click.option('--verbose', is_flag = True, default = False, help = "Print some info before launching")
def spyderman(
    project_dir:Path =  Path.cwd(),
    verbose: bool = False,
    version: str = 'latest'
    ):
    global VERBOSE
    VERBOSE = verbose
    # try to read th ini file
    cprint('Searching for spyder ini file...')
    config = configparser.ConfigParser()
    read = False
    use_path = None
    for path in SPYDER_CONFIG_PATHS:
        try:
            config.read(path.value)
            read = True
            use_path = path.value
            cprint(f'{EMOJIS.CHECK.value}|{path.value}')
        except FileNotFoundError:
            cprint(f'{EMOJIS.X.value}|{path.value}')
    if not read:
        raise Exception("Couldnt find the spyder.ini file, se with the set command.")
    print(project_dir)
    # try to find the virtual environment
    cprint('Searching for venv in common patterns...')
    use_venv_path = None
    for common_pattern in COMMON_VENV_PATHS:

        possible = (project_dir / common_pattern.value)
        if possible.exists():
            cprint(f'{EMOJIS.CHECK.value}|{possible}')
            use_venv_path = possible
            break
        else:
            cprint(f'{EMOJIS.X.value}|{possible}')
    if use_venv_path is None:
        raise Exception(f'No python interpreter found in directory : {project_dir}')
    
    # edit the config
    clist = config['main_interpreter']['custom_interpreters_list']
    config['main_interpreter']['custom_interpreter'] = str(use_venv_path)
    with open(use_path,'w') as f:
        config.write(f)

    # launch
    spyder_command = f'spyder@{version}'
    run(['uvx',spyder_command])

if __name__ == "__main__":
    spyderman()