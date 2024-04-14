PyCommence - Python vs Commence RM
====================================================

`Commence RM <https://commence.com/information-for-customers-81/>`_ is a powerful and flexible database application for customer relationship management, but it is decidedly dated, and its API is not very user-friendly.

Commence Designer Edition is a particuarly cranky beast that demands super-brittle VBS and DDE approaches to integration and offers little support for modern tooling.

This package wraps the Commence API in a python interface for convenience; a complete installation of Commence is required.

PyCommence is built atop :mod:`pycommence.wrapper._icommence` - a makepy generated Com-Object wrapper, via the `win32com` package.


.. toctree::
    :maxdepth: 2

    pycommence_api
    pycommence_wrapper
    cmc_api


Index
-----------

* :ref:`modindex`