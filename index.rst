.. |get_csrname()| replace:: ``get_csrname()``
.. _get_csrname(): https://pawrequest.github.io/pycommence/pycommence_api.html#pycommence.pycommence.get_csrname
.. |HasCursors| replace:: ``HasCursors``
.. _HasCursors: https://pawrequest.github.io/pycommence/pycommence_api.html#pycommence.pycommence.HasCursors
.. |.modindex| replace:: Module Index
.. _.modindex: https://pawrequest.github.io/pycommence/py-modindex.html
.. |PyCommence| replace:: ``PyCommence``
.. _PyCommence: https://pawrequest.github.io/pycommence/pycommence_api.html#pycommence.pycommence.PyCommence
.. |.pycommence.wrapper._icommence| replace:: ``pycommence.wrapper._icommence``
.. _.pycommence.wrapper._icommence: https://github.com/pawrequest/pycommence/blob/main/src/pycommence/wrapper.py
.. |pycommence_context()| replace:: ``pycommence_context()``
.. _pycommence_context(): https://pawrequest.github.io/pycommence/pycommence_api.html#pycommence.pycommence.pycommence_context
.. |pycommences_context()| replace:: ``pycommences_context()``
.. _pycommences_context(): https://pawrequest.github.io/pycommence/pycommence_api.html#pycommence.pycommence.pycommences_context
.. |resolve_csrname()| replace:: ``resolve_csrname()``
.. _resolve_csrname(): https://pawrequest.github.io/pycommence/pycommence_api.html#pycommence.pycommence.resolve_csrname
.. |resolve_row_id()| replace:: ``resolve_row_id()``
.. _resolve_row_id(): https://pawrequest.github.io/pycommence/pycommence_api.html#pycommence.pycommence.resolve_row_id


PyCommence - Python vs Commence RM
====================================================

`Commence RM <https://commence.com/information-for-customers-81/>`_ is a powerful and flexible database application for customer relationship management, but it is decidedly dated, and its API is not very user-friendly.

Commence Designer Edition is a particuarly cranky beast that demands super-brittle VBS and DDE approaches to integration and offers little support for modern tooling.

This package wraps the Commence API in a python interface for convenience; a complete installation of Commence is required.

PyCommence is built atop |.pycommence.wrapper._icommence|_ - a makepy generated Com-Object wrapper - via the `win32com` package.


* `PyCommence <https://pawrequest.github.io/pycommence/pycommence_api.html>`_

  * |HasCursors|_


  * |get_csrname()|_
  * |resolve_csrname()|_
  * |resolve_row_id()|_
  * |PyCommence|_


  * |pycommence_context()|_
  * |pycommences_context()|_

* `Commence Wrapper <https://pawrequest.github.io/pycommence/pycommence_wrapper.html>`_

  * `DB Wrapper <https://pawrequest.github.io/pycommence/pycommence_wrapper.html#module-pycommence.wrapper.cmc_wrapper>`_


  * `Cursor Wrapper <https://pawrequest.github.io/pycommence/pycommence_wrapper.html#module-pycommence.wrapper.cursor_wrapper>`_


  * `RowSet Wrappers <https://pawrequest.github.io/pycommence/pycommence_wrapper.html#module-pycommence.wrapper.row_wrapper>`_


  * `Commence Conversation Wrapper <https://pawrequest.github.io/pycommence/pycommence_wrapper.html#module-pycommence.wrapper.conversation_wrapper>`_


  * `ICommence Interface Wrapper <https://pawrequest.github.io/pycommence/pycommence_wrapper.html#module-pycommence.wrapper._icommence>`_



* `Commence RM API <https://pawrequest.github.io/pycommence/cmc_api.html>`_

  |




Index
-----------

* |.modindex|_
