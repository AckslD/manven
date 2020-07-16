CHANGELOG
=========

For more details refer to the [documentation](https://acksld.github.io/manven/).

Upcoming
--------

2020-07-16 (0.3.0)
--------
* Added possibility to specify default packages to be installed in new environments.
  This can be done by either specifying the entry `DEFAULT_PKGS` in the config-file, e.g. as `[manven, neovim]` or by using the `-i/--install`-flag multiple times for each package.

2020-01-31 (0.2.0)
------------------
* Added functionality to activate last activated environment

2019-11-15 (0.1.4)
------------------
* When removing environments it is now checked that this is not the current one.
* The test printed the first time one uses manven is now not printed in new environments.

2019-11-12 (0.1.3)
------------------
* Fixed bug when using python < 3.7 since capture_output is not an argument to subprocess.run in this case.

2019-11-12 (0.1.2)
------------------
* Fixed bug in bin/manven

2019-10-24 (0.1.1)
------------------
* Fixed requirements and remove print statements when creating an environment.

2019-10-24 (0.1.0)
------------------
* `manven` now supports the same flags as `virtualenv` for the commands `activate`, `create` and `temp`.
