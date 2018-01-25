####################
Minorisa Development
####################

This module includes several utilities to facilitate the development of Odoo addons.

Current utilities are as follows:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Tool
     - Description
   * - Menu Setup
     - Displays current menu tree including XML IDs
   * - Group Setup
     - Displays current groups and XML IDs
   * - Download Translations
     - Downloads .po files for defined languages for selected addon.
       It creates i18n directories & files as needed.
       If properly configured, it commits & pushes in the related GitLab repository.
