# manven (0.3.0)

Welcome to manven's README.

`manven` is a small CLI wrapping the functionality of `virtualenv` to make **man**aging **v**irtual **env**ironments easier.
Functionalities include creating, activating, removing and listing virtual environments, together with simply ways to quickly create and prune temporary environments.
Follow the documentation below for how to install and how to get started.

Happy venv-ing!

![](manven.gif)

## Installation
To install ``manven`` from pypi do:
```
pip3 install manven
```
`manven` can then directly be used to create, list, remove virtual environments.
However, to also have `manven` active these environments it is recommended that you add this alias to your system (to your rc file):
```
alias smanven='source $(which manven)'
```
`manven` can then be used by calling the command `smanven`.

If you're using [fish](https://fishshell.com/) shell, instead add:
```
alias smanven 'source (which manven.fish)'
```
See [installation](https://acksld.github.io/manven/installation.html) for more details.

## Getting started
Find all commands, arguments and options that `manven` supports by doing
```
smanven --help
```
See [getting started](https://acksld.github.io/manven/usage.html) for more details and examples.

## Configuration
To configure `manven` create a config such as the following which contains the default values.
```
[manven]
envs_path=~/venvs
default_pkgs=[manven, neovim]
ipykernel=false
```
where:
* `envs_path`: Specifies where virtual environments should be stored.
* `default_pkgs`: Default packages that should be installed in any new environment.
* `ipykernel`: Set this to `true` if you want `ipykernel` to be installed and this environment added.

The config file can either be:

1. In the current directory with the name ``.manven.conf``.
2. In the home directory (``~``/``$HOME``), with the name ``.manven.conf``.
3. In the directory ``~/.config/manven/`` with the name ``manven.conf``.

If there is more than one file as above the first in the list will be used.
Any config value can also be specified (overridden) as a flag to `manven`.

## Completions
If you're using `zsh` you can copy (or symlink) the file `completions/_manven` to a folder in your `$fpath` to enable completions of commands and virtual environments to activate. This requires `compinit` to have been activated in your `.zshrc`.

### Choose virtual environment with fzf
Additionally you can add the following functions to your `.zshrc` to trigger fuzzy finding of virtual environments with a trigger sequence (default `**`).
```
_fzf_complete_manven() {
  _fzf_complete --reverse --prompt="venv> " -- "$@" < <(
    manven list
  )
}

_fzf_complete_smanven() {
    _fzf_complete_manven
}
```
With these functions and if you type `smanven activate **<TAB>` you can choose the virtual environment using `fzf`.
