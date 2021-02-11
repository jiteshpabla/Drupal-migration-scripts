# Drupal-migration-scripts

### Instructions for - yml_ordering.py
This script gives us the order in which the migrations should be done for Drupal, when we are doing it manually.
- Just put the .py script into the folder where your generated .yml files are form the migrate_plus module. (Make sure only the migrate_plus yaml files are in the directory)
- Run `python3 yml_ordering.py`
- This will generate .txt files with the commands to run the migrations (the .yml files). These commands should be run in order of their numbering from dep0.txt to dep1.txt and so on.
