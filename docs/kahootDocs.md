kahootDocs
-----------

Version History
===============

SERVER
------

- v1.0.1: Server and class structure implemented.
- v1.0.2: Small fixes and changes. Inheritance added, with 3 question types.
- v1.0.3: First addition of #signal data (broken so it's hashed out)
- v1.0.4: Fixed #signal, added functionality for checking questions, UUID for questions etc.
- v1.0.5: Moved question code to kModules/kQuestions
- v1.0.6: Sedning data with #signal and client UUIDs added.

CLIENT
------

- v1.0.1: Nothing. Yep.
- v1.0.2: Added #signal to the client.
- v1.0.3: UUID and #signal connection added.

MODULES
-------

- [kQuestions] Code from kahootServer.py moved to this file.
- [kahootTk] Wrapper of tkinter for the kahootGUI.py file
- [printer] Special printing code, soon to be moved to misc. folder
GUI
---

- v1.0.1: Started pygame production.
- v1.0.2: Changed to tkinter. Added wrapper classes for objects

TESTS
-----

- v1.0.1 [Client] Started a non-signal ver. of KahootClient
- v1.0.2 [Client] Small changes to classes.
- v1.0.3 - v1.0.5 [Client] Fixed some printing issues
- 
- v1.0.1 [Server] Started a non-signal ver. of KahootServer
- v1.0.2 [Server] Added sim of lobby to class.
- v1.0.3 - v1.0.5 [Server] Fully simulated a game with points and leaderboard

-----

Other Docs
==========

- Website coming soon!

Implementation
--------------

- Should be packaged as an executable (research pending)
- Music Files coming soon (kahootOST)
