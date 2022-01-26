Getting started
===============

Configure
---------

You can chose where you want ``manven`` to put the virtual environments by adding a file of the form

.. code-block:: text

   [manven]
   ENVS_PATH=path/to/your/dir
   DEFAULT_PKGS=[manven, neovim]
   PIP_INSTALL_FLAGS=

which can either be:

1. In the current directory with the name ``.manven.conf``.
2. In the home directory (``~``/``$HOME``), with the name ``.manven.conf``.
3. In the directory ``~/.config/manven/`` with the name ``manven.conf``.

If there is more than one file as above the first in the list will be used.

The rest of this section assumes that you set the alias ``smanven`` as recommended in the :doc:`installation`.

To find out which path is used by manven, simply do:

.. code-block:: bash

   smanven get path

Create an environment
---------------------

To create and activate an environment, do:

.. code-block:: bash
   
   smanven activate venv

where ``venv`` is the name of your virtual environment.
You now have a working ``virtualenv`` environment which you can start using.
To deactivate the environment, simply type ``deactivate``.

If you just want to create the environment without activating it you can, do:

.. code-block:: bash

   smanven create venv


By default ``manven`` will install itself in the new environment such that you can easily switch to another (without deactivating) by calling ``smanven activate`` again.
However, to not have ``manven`` install itself, give the flag ``--no-manven``.
If you already have the virtual environment ``venv`` and try to activate/create it again your current environment will be kept.
If you instead want to replace the environment with a fresh one, give the flag ``--new````.


Remove an environment
---------------------
To remove an existing environment, do:

.. code-block:: bash

   smanven remove venv

List current environment
------------------------
To list the current virtual environments available, do:

.. code-block:: bash

   smanven list

To also include the temporary environments (see below) pass the flag ``--all`` (or ``-a``).


Temporary environments
----------------------
To quickly create and activate a temporary environments, do:

.. code-block:: bash

   smanven temp

which also accepts the ``--no-manven`` flag as ``create`` and ``activate`` does.
Temorary virtual environment will be put in a folder ``.temp`` next to the other environments and will be given names ``temp_venv_<i>`` where ``i`` is incremental.

To prune all the current temporary environments, do:

.. code-block:: bash

   smanven prune


Completions
-----------
If you're using ``zsh`` you can copy (or symlink) the file ``completions/_manven`` to a folder in your ``$fpath`` to enable completions of commands and virtual environments to activate. This requires ``compinit`` to have been activated in your ``.zshrc``.

Choose virtual environment with fzf
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Additionally you can add the following functions to your ``.zshrc`` to trigger fuzzy finding of virtual environments with a trigger sequence (default ``**``).

.. code-block:: bash

   _fzf_complete_manven() {
     _fzf_complete --reverse --prompt="venv> " -- "$@" < <(
       manven list
     )
   }

   _fzf_complete_smanven() {
       _fzf_complete_manven
   }

With these functions and if you type ``smanven activate **<TAB>`` you can choose the virtual environment using ``fzf``.
