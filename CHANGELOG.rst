=========
Changelog
=========


0.3.3 (2025-08-11)
=======================================

| This patch improve the workflow of the project.

Added
-----
- Full automation has been achieved for the software life cycle.


0.3.2 (2025-05-01)
=======================================

| This patch release improves tox.

Improved
--------
- Tox is simplified and improved.
- Things that were not needed are removed.


0.3.1 (2025-04-24)
=======================================

| This release fixs the bugs and issues faced in the previous version.
| The dmcview is now executable from the command line.

Added
-----
- Added flag for the simulator and is now executable from the cli "dmcview -s Y".

Fixed
-----
- The --version flag is now working well from the cli.
- Dmcview is now executable from the command line. 


0.3.0 (2025-04-13)
=======================================

| This release brings the new 3D acceleration support to the **dmcview** Python Package.

Added
-----
- Added a 3D graph to the left of the compass display.
- This visualizes real-time acceleration along the X, Y, Z axes.
- Acceleration values will also be printed under the information section.
- The simulator is improved to visualize this new 3D acceleration in action.

**Note:** This release requires new data input:

- 3 acceleration vectors: **X**, **Y** , **Z** 


Changed
-------
- Replaced the old video and picture of the dmcview in the readme with a new video that includes the new 3D acceleration.
- Improved the documentation to include the new added feature.


Fixed
-----
- Removed duplicated and broken badges that show in PyPI and github.


0.0.1 (2024-08-04)
=======================================

| This is the first ever release of the **dmcview** Python Package.
| The package is open source and is part of the **DMC View** Project.
| The project is hosted in a public repository on github at https://github.com/iso-techdev/dmc-view
| The project was scaffolded using the `Cookiecutter Python Package`_ (cookiecutter) Template at https://github.com/boromir674/cookiecutter-python-package/tree/master/src/cookiecutter_python

| Scaffolding included:

- **CI Pipeline** running on Github Actions at https://github.com/iso-techdev/dmc-view/actions
- `Test Workflow` running a multi-factor **Build Matrix** spanning different `platform`'s and `python version`'s
    1. Platforms: `ubuntu-latest`, `macos-latest`
    2. Python Interpreters: `3.6`, `3.7`, `3.8`, `3.9`, `3.10`

- Automated **Test Suite** with parallel Test execution across multiple cpus.
- Code Coverage
- **Automation** in a 'make' like fashion, using **tox**
- Seamless `Lint`, `Type Check`, `Build` and `Deploy` *operations*


.. LINKS

.. _Cookiecutter Python Package: https://python-package-generator.readthedocs.io/en/master/
