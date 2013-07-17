trackkr
=======

django based service for locating gps units licenced under GPLv2


Project status
=======

Currently in deep-deep beta

More info about every release can be found at [RELEASE NOTES](wiki/RELEASE_NOTES) page

HOWTO
=======

You can run trackkr for test purposes:
``./manage.py syncdb``
``./manage.py runserver``

These commands will create sqlite3 db and user, then starts http server on port localhost:8000

You may possibly want to test how trackkr displays units on the map, for such purposes you need to add unit through web interfaces, run trackkrd:

``./trackkrd``

And change IMEI to defined in web interface in tracker_emulator.py before run it.
