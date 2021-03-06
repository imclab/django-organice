=============
Configuration
=============

django Organice comes with sensible defaults for almost anything.  Yet still, you can customize its behavior with the
help of the settings listed in this section.

.. _settings:

Settings
========

You may define any of the following options in your project's ``settings`` to override the default value.

ORGANICE_URL_PATH_ADMIN
-----------------------
:Default: ``admin``

The URL path for accessing the Django Administration backend (e.g. ``www.example.com/admin``).  Must be non-empty.
Use an identifier only, no white space, no leading or trailing slash.

ORGANICE_URL_PATH_BLOG
----------------------
:Default: ``blog``

The URL path for the blog's start page (e.g. ``www.example.com/blog``).  Must be non-empty.  Use an identifier only,
no white space, no leading or trailing slash.

ORGANICE_URL_PATH_NEWSLETTER
----------------------------
:Default: ``newsletter``

The URL path for accessing newsletter functionality on the front-end (e.g. ``www.example.com/newsletter``).  Must
be non-empty.  Use an identifier only, no white space, no leading or trailing slash.
