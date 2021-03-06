.. image:: https://raw.githubusercontent.com/collective/behavior.richpreview/master/docs/preview.png
    :align: left
    :alt: Rich Link Preview
    :height: 100px
    :width: 100px

*****************
Rich Link Preview
*****************

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

A behavior for Dexterity-based content types to show previews on hover over hyperlinks in content area.

Mostly Harmless
===============

.. image:: http://img.shields.io/pypi/v/collective.behavior.richpreview.svg
   :target: https://pypi.python.org/pypi/collective.behavior.richpreview

.. image:: https://img.shields.io/travis/collective/behavior.richpreview/master.svg
    :target: http://travis-ci.org/collective/behavior.richpreview

.. image:: https://img.shields.io/coveralls/collective/behavior.richpreview/master.svg
    :target: https://coveralls.io/r/collective/behavior.richpreview

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/collective/behavior.richpreview/issues

Don't Panic
===========

Installation
------------

To enable this package in a buildout-based installation:

Edit your buildout.cfg and add the following to it:

.. code-block:: ini

    [buildout]
    ...
    eggs =
        collective.behavior.richpreview

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to 'Rich Link Preview' and click the 'Activate' button.

Usage
-----

TBD.

How Does It Work?
-----------------

For every ``<a>`` tag in the content area of a page,
we fetch the remote URL (the one referred in the ``src`` attribute) and parse it searching for `Open Graph <http://ogp.me/>`_ metadata describing it.
We do this in Python with a helper browser view,
as is not possible in JavaScript because of the `CORS <https://en.wikipedia.org/wiki/Cross-origin_resource_sharing>`_ mechanism.
We accept only encrypted URLs to avoid misuse of this browser view.

We encrypt URLs in a transform using `public-key cryptography <https://en.wikipedia.org/wiki/Public-key_cryptography>`_.
A pair of cryptographic keys is generated automatically on package installation.
These keys are only available to Administrators in the control panel configlet.

Development
-----------

We use `webpack <https://webpack.js.org/>`_ to process static resources on this package.
Webpack processes SCSS and JS files, minifies the resulting CSS and JS, and optimizes all images.
The final JS file is also a UMD package, which provides compatibility with most popular script loaders.

To contribute, you should start the instance in one shell and start webpack watcher on another with the following command:

.. code-block:: bash

    $ bin/watch-richpreview

Then go to ``webpack/app`` folder and edit SCSS and JS files;
Webpack watcher will automatically create the final resources in the right place.

There are also other commands added to handle more complex scenarios.
The following command will set the buildout node installation in the system PATH, this way you can use webpack as described on its documentation.

.. code-block:: bash

    $ bin/env-richpreview

The following command generates JS and CSS without the minify step (it can be used to check the code being generated in a human readable way).

.. code-block:: bash

    $ bin/debug-richpreview

The following command rebuilds static files and exit (insted of keep watching the changes):

.. code-block:: bash

    $ bin/build-richpreview

Releasing using zest.releaser
-----------------------------

Static resources on this package are generated using `webpack`_ and aren't included in VCS.
If you release using zest.releaser you have to `upload manually the files to PyPI <https://github.com/zestsoftware/zest.releaser/issues/261>`_ or you will end with a broken distribution:

* run ``longtest`` and ``fullrelease``, as usually
* answer "no" when asked to upload to PyPI and continue normally
* do a checkout to the tag you're releasing
* run ``bin/build-richpreview`` to update static files
* create the distribution files using ``python setup.py sdist bdist_wheel`` as usual
* upload the files using ``twine upload dist/*``

In case of errors you will have to create a new release as the PyPI Warehouse `doesn't allow for a filename to be reused <https://upload.pypi.org/help/#file-name-reuse>`_.
