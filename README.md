# manven (0.5.0)

Welcome to manven's README.

`manven` is a small CLI wrapping the functionality of `virtualenv` to make **man**aging **v**irtual **env**ironments easier.
Functionalities include creating, activating, removing and listing virtual environments, together with simply ways to quickly create and prune temporary environments.
Follow the documentation below for how to install and how to get started.

Happy venv-ing!

![](manven.gif)

## Installation

See [installation](https://acksld.github.io/manven/installation.html).

## Getting started

See [getting started](https://acksld.github.io/manven/usage.html).

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
