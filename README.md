## Warframe application ##
App to handle Warframe data such as owned warframes, weapons, arcanes, etc. Currently only can store users, warframes, and user/warframe combos.

Database stored locally.  
Program can be run using Python Ver 3.14.3+.  
Latest release allows program to be extracted and run without installing Python.

## DEPENDENCIES ##
Python Ver 3.14.3+

## TODO ##
Add exceptions for database interactions so that errors can be shown to user.  
Look into necessity of asserts.  
Would likely be beneficial to switch everything from breaking down strings to using iterables more. Will pause   

## KNOWN ISSUES ##


## RELEASE NOTES ##
### Version 1.0.0-pre-alpha
Adopted Google's docstring styleguide.  
Restructured code for more modularity.  
Identical functions combined utilizing match-case.  
Added sql statements adjusted to unnamed parameters.  
Removed unnecessary plural add statement.  
Added functions utilizing above statements that accept one or more rows to insert.  
Added splitting functions for strings.  
Added function for generating tuple of dictionaries.  
Created tests.py for debug testing with test cases.  
Experimented with PySide6 and Qt Designer for new GUI builder. Related files not uploaded due to irrelevance.

### Version 0.7.3
Rebuilt dist with changes from 0.7.2.  
Final upload for tkinter. Future uploads will be rebuild in preparation for use with Qt or other GUI builder.  
Release v0.7.3 tkinter final uploaded.

### Version 0.7.2
Corrected previous version number.  
Added Sirius & Orion to warframes.txt.  
Moved multiline SQL statements into individual files.  
Renamed functions with clearer names.  
Removed TODOs that are currently unnecessary or may become irrelevant with future changes.

### Version 0.7.1
Implimented Ruff linter to learn better coding practices.  
Adjusted code based on linter messages.  
Replaced f-strings in SQL with placeholders. (As the database is only stored locally with no sensitive information, SQL injection not a concern yet. However, may as well fix it during the linting corrections to remove the warning.)  
Removed unused script files.

### Version 0.7.0
Adjusted warframe.txt file path to use Pathlib.  
Created Pyinstaller build.  
Corrected SQL INSERTs to INSERT IGNOREs.  
Added missing NOT NULL and UNIQUE constraints.  
Fixed setup function comparison.

### Version 0.6.0
Added database table exist check/creation.  
Added warframe table check against warframes.txt to add missing warframes.  
Updated warframes.txt with Follie and Voruna Prime.  
Added function for inserting multiple warframes.

### Version 0.5.0
Removed unused functions from db_interact.py.  
Added sorting to SQL queries.  
Replaced SQL list results with generators.  
Fixed SQL statements with incorrect record returns.  
Adjusted user output formatting to use line breaks.  

### Version 0.4.0
Basic functionality and UI complete.  
Known bug - some SQL not returning accurate records.