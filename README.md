## Warframe application ##
App to handle Warframe data such as owned warframes, weapons, arcanes, etc. Currently only can store users, warframes, and user/warframe combos.

Database stored locally.  
Program must be run using Python Ver 3.14.3+.

## DEPENDENCIES ##
Python Ver 3.14.3+

## TODO ##
Implement propery decorators.  
Implement getter decorators.  
Implement setter decorators.  
Replace lists with generators where possible. If a list is needed regardless, a generator is likely pointless.  
Implement context managers if useful for files/db.  
Adjust docstrings to be more useful.  
Check that all functions show return type.  
Check that all parameters indicate type.  
Look into necessity of asserts.  
Implement multiprocessing if useful. Multithreading unlikely to be much use.  
Look into using Cython or other ways to compile for executable.

## KNOWN BUGS ##
UI won't reflect OR IGNORE on INSERT statements.

## RELEASE NOTES ##
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