Installation
============

.. note::

   To use ``manven`` you need to be using ``bash``, ``fish`` or similar as a shell (it should work also for ``zsh`` and ``dash`` but not yet tested).

Install from pypi
-----------------

To install ``manven`` from pypi do:

.. code-block:: bash
   
   pip3 install manven

``manven`` can then directly be used to create, list, remove virtual environments.
However, to also have ``manven`` active these environments it is recommended that you add this alias to your system (to your rc file):

.. code-block:: bash

   alias smanven='source $(which manven)'

``manven`` can then be used by calling the command ``smanven``.

If you're using `fish <https://fishshell.com/>`_ shell, instead add:

.. code-block:: bash

   alias smanven 'source (which manven.fish)'

.. note::

   If you are using `pyenv <https://github.com/pyenv/pyenv>`_ you should instead add the alias

   .. code-block:: bash

      alias smanven='source $(pyenv which manven)'

   and similarly if you are using fish.


Install from source
-------------------

To install ``manven`` from source, clone the `repo <https://github.com/AckslD/manven>`_, cd into the folder and do:

.. code-block:: bash

   make install

To verify the installation, do:

.. code-block:: bash

   make verify


As above, it is recommended to add the alias ``smanven`` to have the full power of ``manven``.
