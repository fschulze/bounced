bounced
=======

A library to determine info on bounced email messages.


Why another one?
----------------

With `flufl.bounce`_ one only gets a list of email addresses without any further info.
The API of `bounce_email`_ isn't Pythonic and inefficient for several use cases, like when you already have email message objects.

.. _flufl.bounce: https://pypi.org/project/flufl.bounce/
.. _bounce_email: https://pypi.org/project/bounce_email/

References
----------

http://www.serversmtp.com/en/smtp-error



Changelog
=========

0.2.0 - 2018-03-31
------------------

* Support ``local`` recipient kind.
  [fschulze]

* Support longer status codes like ``5.1.10``.
  [fschulze]


0.1.0 - 2018-03-30
------------------

* Initial release.
  [fschulze]
