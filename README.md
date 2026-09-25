## Warframe application ##
App to handle Warframe data such as owned warframes, weapons, arcanes, etc. Currently only can store users, warframes, and user/warframe combos.  

Database stored locally.  
Latest release is constructed via Pyinstaller and allows the program to be extracted and run without installing Python.  

## DEPENDENCIES ##
Python Ver 3.14.3+  

## TODO ##

## KNOWN ISSUES ##

## RELEASE NOTES ##
### Version 1.3.0
Renamed several functions for better use clarity.  
Implemented row factory use for better code legibility.  
Replaced numerous strings with constants for more efficient input.  
Completed set_id function.  
Conversion from string to dataclass completed for add_to_user function.  

### Version 1.2.0
Created function to set dataclass object ids from the database.  
Created function to add dataclass objects to a user in the corresponding lookup table.  
Created function to add users to a dataclass object in the corresponding lookup table.  
Corrected the type annotations of data_objects arguments.  
Created function to return if arg is iterable.  
Created function to return the type of arg or arg's first element.  
Added error to raise when arg isn't iterable and must be.  
Restructured add and get_users_of functions to automate sql statement determination. No longer require a parameter to do so.  

### Version 1.1.0
Created classes.py to contain User, Warframe, and future dataclasses.  
Created exceptions.py to contain custom exceptions.  
Added error to raise when arg doesn't match any case pattern.  
Created function to return tuple of names from dataclass objects.  
Created function to return tuple of ids from dataclass objects.  
Renamed the following string based functions and created replacements that use dataclass objects: get_all, get_from_user, get_users_of, _split_for_sql, add.  
Print error placeholders have been replaced with proper exception raises in new functions.  
Placeholder exceptions and typing added to new functions for future implementation.  

### Version 1.0.0
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