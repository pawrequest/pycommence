=================
CMC_FLAG_INTERNET
=================

.. container::

   .. rubric:: Commence Database API
      :name: commence-database-api

   This Guide documents the Commence Database API and the Automation
   objects that it supports. The Reference section details the
   properties and methods of each of the objects.

   Reference

   `ICommenceDB <#chmtopic2>`__

   `ICommenceCursor <#chmtopic11>`__

   `ICommenceConversation <#chmtopic33>`__

   `ICommenceQueryRowset <#chmtopic72>`__

   `ICommenceAddRowset <#chmtopic36>`__

   `ICommenceEditRowset <#chmtopic59>`__

   `ICommenceDeleteRowset <#chmtopic48>`__

   `Constants <#chmtopic82>`__

   `Developer Notes <#chmtopic83>`__

   .. rubric:: ICommenceDB Object
      :name: icommencedb-object

   Represents a Commence Database.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DB.D

   Properties

   String Name

   (read-only) Name of the Commence database.

   String Path

   (read-only) Full path of the Commence database.

   String RegisteredUser

   (read-only) CR/LF delimited string with user name, company name and
   serial number.

   Boolean Shared

   (read-only) TRUE if database is enrolled in a workgroup.

   String Version

   (read-only) Version number in x.y format.

   String VersionExt

   (read-only) Version number in x.y.z.w format.

   Methods

   `ICommenceConversation <#chmtopic33>`__\  GetConversation

   Create a conversation object.

   `ICommenceCursor <#chmtopic11>`__\  GetCursor

   Create a cursor object.

   .. rubric:: ICommenceDB::Name
      :name: icommencedbname

   Data Type

   String

   Description

   (read-only) Name of the Commence database.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DB.D

   See Also

   `ICommenceDB <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceDB::Path
      :name: icommencedbpath

   Data Type

   String

   Description

   (read-only) Full path of the Commence database.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DB.D

   See Also

   `ICommenceDB <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceDB::RegisteredUser
      :name: icommencedbregistereduser

   Data Type

   String

   Description

   (read-only) CR/LF delimited string with user name, company name and
   serial number.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DB.D

   See Also

   `ICommenceDB <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceDB::Shared
      :name: icommencedbshared

   Data Type

   Boolean

   Description

   (read-only) TRUE if database is enrolled in a workgroup.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DB.D

   See Also

   `ICommenceDB <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceDB::Version
      :name: icommencedbversion

   Data Type

   String

   Description

   (read-only) Version number in x.y format.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DB.D

   See Also

   `ICommenceDB <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceDB::VersionExt
      :name: icommencedbversionext

   Data Type

   String

   Description

   (read-only) Version number in x.y.z.w format.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DB.D

   See Also

   `ICommenceDB <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceDB::GetConversation
      :name: icommencedbgetconversation

   ICommenceConversation GetConversation(String pszApplicationName,
   String pszTopic)

   Create a conversation object.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DB.D

   Return Value

   Returns a pointer to conversation object on success, NULL on error.

   Parameters

   pszApplicationName

   DDE Application name.

   The only valid value is "Commence".

    

   pszTopic

   DDE Topic name, must be a valid Commence topic name.

   The DDE.HLP file contains a reference to the allowed DDE topic names.

   Examples include "GetData", "ViewData", etc.

    

   See Also

   | Related Methods and Objects
   | `ICommenceDB <javascript:RelatedTopic0.Click()>`__\ 
   | `ICommenceConversation <javascript:RelatedTopic1.Click()>`__\ 
   | `ICommenceConversation::Execute <javascript:RelatedTopic2.Click()>`__\ 
   | `ICommenceConversation::Request <javascript:RelatedTopic3.Click()>`__\ 

   .. rubric:: ICommenceDB::GetCursor
      :name: icommencedbgetcursor

   ICommenceCursor GetCursor(Long nMode, String pName, Long nFlags)

   Create a cursor object.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DB.D

   Return Value

   Returns a pointer to cursor object on success, NULL on error.

   Parameters

   nMode

   Type of Commence data to access with this cursor.

   Valid values are:

   0 - CMC_CURSOR_CATEGORY

   Use the Commence category specified by pName.

   1 - CMC_CURSOR_VIEW

   Use the Commence view specified by pName.

   2 - CMC_CURSOR_PILOTAB

   Use the Commence category and fields defined from

   Preferences - Other Apps - 3Com Pilot Address Book

   3 - CMC_CURSOR_PILOTMEMO

   Use the Commence category and fields defined from

   Preferences - Other Apps - 3Com Pilot Memo Pad

   5 - CMC_CURSOR_PILOTTODO

   Use the Commence category and fields defined from

   Preferences - Other Apps - 3Com Pilot To Do List

   6 - CMC_CURSOR_PILOTAPPT

   Use the Commence category and fields defined from

   Preferences - Other Apps - 3Com Pilot Date Book

    

   pName

   Name of an object in the database.

   Use determined by nMode:

   For CMC_CURSOR_CATEGORY, pName is the category name.

   For CMC_CURSOR_VIEW, pName is the view name.

   For CMC_CURSOR_PILOTAB, pName is unused.

   For CMC_CURSOR_PILOTMEMO, pName is unused.

   For CMC_CURSOR_PILOTTODO, pName is unused.

   For CMC_CURSOR_PILOTAPPT, pName is unused.

    

   nFlags

   Addition option flags.

   Logical OR of following option flags:

   CMC_FLAG_PILOT - Save Item agents defined for the Pilot

   subsystem will fire.

   CMC_FLAG_INTERNET - Save Itgem agents defined for the

   Internet/intranet will fire.

    

   Comments

   For CMC_CURSOR_CATEGORY, the resulting cursor will have a column set
   composed of all supported fields in the category (in no particular
   order).

   For CMC_CURSOR_VIEW, the resulting cursor will inherit the view's
   filter, sort and column set. ICommenceCursor methods can be used to
   change these attributes.

   For CMC_CURSOR_PILOT\*, the column set for the resulting cursor will
   only include fields defined by the Commence preferences (in no
   particular order). It is not possible to change the filter, sort or
   column set.

   See the Developer Notes for more information about the CMC_FLAG_PILOT
   and CMC_FLAG_INTERNET flags.

   See Also

   | Related Methods and Objects
   | `ICommenceDB <javascript:RelatedTopic0.Click()>`__\ 
   | `ICommenceCursor <javascript:RelatedTopic1.Click()>`__\ 
   | `ICommenceCursor::SetFilter <javascript:RelatedTopic2.Click()>`__\ 
   | `ICommenceCursor::SetLogic <javascript:RelatedTopic3.Click()>`__\ 
   | `ICommenceCursor::SetSort <javascript:RelatedTopic4.Click()>`__\ 
   | `ICommenceCursor::SetColumn <javascript:RelatedTopic5.Click()>`__\ 

   .. rubric:: ICommenceCursor Object
      :name: icommencecursor-object

   Represents a cursor or query that is built to retrieve data

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Properties

   String Category

   (read-only) Name of the underlying Commence category.

   Long ColumnCount

   (read-only) Number of columns in this cursor (-1 on error).

   Long RowCount

   (read-only) Number of rows in this cursor (-1 on error).

   Boolean Shared

   (read-only) TRUE if category is shared in a workgroup.

   Methods

   Boolean SetColumn(Long nColumn, String pName, Long nFlags)

   Defines the column set for the cursor.

   Boolean SetFilter(String pFilter, Long nFlags)

   Defines a filter clause for the cursor.

   Boolean SetLogic(String pLogic, Long nFlags)

   Defines the filter logic for the cursor.

   Boolean SetSort(String pLogic, Long nFlags)

   Defines the sort criteria for the cursor.

   Long SeekRow(Long bkOrigin, Long nRows)

   Seek to a particular row in the cursor.

   Long SeekRowApprox(Long nNumerator, Long nDenom)

   Seek to an approximate position in the cursor.

   `ICommenceQueryRowSet <#chmtopic72>`__\  GetQueryRowSet(Long nCount,
   Long nFlags)

   Create a rowset object with the results of a query.

   `ICommenceQueryRowSet <#chmtopic72>`__\  GetQueryRowSetByID(String
   pRowID, Long nFlags)

   Create a rowset object with a particular row loaded.

   `ICommenceAddRowSet <#chmtopic36>`__\  GetAddRowSet(Long nCount, Long
   nFlags)

   Create a rowset of new items to add to the database.

   `ICommenceEditRowSet <#chmtopic59>`__\  GetEditRowSet(Long nCount,
   Long nFlags)

   Create a rowset of existing items for editing.

   `ICommenceEditRowSet <#chmtopic59>`__\  GetEditRowSetByID(String
   pRowID, Long nFlags)

   Create a rowset for editing a particular row.

   `ICommenceDeleteRowSet <#chmtopic48>`__\  GetDeleteRowSet(Long
   nCount, Long nFlags)

   Create a rowset of existing items for deletion.

   `ICommenceDeleteRowSet <#chmtopic48>`__\  GetDeleteRowSetByID(String
   pRowID, Long nFlags)

   Create a rowset for deleting a particular row.

   Boolean SetActiveItem

   Set active item used for view cursors using a view linking filter.

   Boolean SetActiveDate

   Set active date used for view cursors using a view linking filter.

   Boolean SetActiveDateRange

   Set active date range used for view cursors using a view linking
   filter.

   Boolean SetRelatedColumn

   Adds a related (indirect/connected field) column to the cusor.

   .. rubric:: ICommenceCursor::Category
      :name: icommencecursorcategory

   Data Type

   String

   Description

   (read-only) Name of the underlying Commence category.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   See Also

   `ICommenceCursor <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceCursor::ColumnCount
      :name: icommencecursorcolumncount

   Data Type

   Long

   Description

   (read-only) Number of columns in this cursor (-1 on error).

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   See Also

   `ICommenceCursor <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceCursor::RowCount
      :name: icommencecursorrowcount

   Data Type

   Long

   Description

   (read-only) Number of rows in this cursor (-1 on error).

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   See Also

   `ICommenceCursor <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceCursor::Shared
      :name: icommencecursorshared

   Data Type

   Boolean

   Description

   (read-only) TRUE if category is shared in a workgroup.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   See Also

   `ICommenceCursor <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceCursor::SetFilter
      :name: icommencecursorsetfilter

   Boolean SetFilter(String pFilter, Long nFlags)

   Defines a filter clause for the cursor.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Return Value

   Returns TRUE on success, FALSE on error.

   Parameters

   pFilter

   Text defining the new filter clause. Syntax is identical to the one
   used by the DDE ViewFilter request (qv).

   nFlags

   Unused at present, must be 0.

   Comments

   The pFilter string defines which filter clause is to be replaced. If
   the clause is already defined it will be overwritten.

   If the cursor is opened in CURSOR_VIEW mode, the SetFilter only
   affects the cursor's secondary filter. That is, when building the
   rowset, the view's filter is first evaluated. Items that match are
   then passed through the cursor's secondary filter. The rowset only
   contains items that satisfy both filters.

   See Also

   | `ICommenceCursor <javascript:RelatedTopic0.Click()>`__\ 
   | `SetLogic <javascript:RelatedTopic1.Click()>`__\ 

   .. rubric:: ICommenceCursor::SetLogic
      :name: icommencecursorsetlogic

   Boolean SetLogic(String pLogic, Long nFlags)

   Defines the filter logic for the cursor.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Return Value

   Returns TRUE on success, FALSE on error.

   Parameters

   pLogic

   Text defining the new filter logic. Syntax is identical to the one
   used by the DDE ViewConjunction request (qv).

   nFlags

   Unused at present, must be 0.

   Comments

   Unless otherwise specified, the default logic is AND, AND, AND.

   See Also

   | `ICommenceCursor <javascript:RelatedTopic0.Click()>`__\ 
   | `SetFilter <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceCursor::SetSort
      :name: icommencecursorsetsort

   Boolean SetSort(String pSort, Long nFlags)

   Defines the sort criteria for the cursor.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Return Value

   Returns TRUE on success, FALSE on error.

   Parameters

   pSort

   Text defining the new sort criteria. Syntax is identical to the one
   used by the DDE ViewSort request (qv).

   nFlags

   Unused at present, must be 0.

   Comments

   If the cursor is opened in CMC_CURSOR_VIEW mode, the sort defaults to
   the view's sort. All other cursor modes default to ascending sort by
   the Name field.

   See Also

   `ICommenceCursor <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceCursor::SetColumn
      :name: icommencecursorsetcolumn

   Boolean SetColumn(Long nColumn, String pName, Long nFlags)

   Defines the column set for the cursor.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Return Value

   Returns TRUE on success, FALSE on error.

   Parameters

   nColumn

   The (0-based) index of the column to set.

   pName

   Name of the field to use in this column.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_ALL - create column set of all fields

    

   Comments

   When defining a column set, the columns must be defined in sequential
   order (0, 1, 2, etc.). This is to prevent problems with undefined
   columns (e.g. 0, 1, 3, ...).

   Duplicate columns are not supported. Each column must map to a
   different field.

   Not all Commence field types can be included in the cursor
   definition. The set of supported field types exactly matches those
   fields that can be displayed in a Commence report (minus combined
   fields and indirect fields).

   See Also

   | `ICommenceCursor <javascript:RelatedTopic0.Click()>`__\ 
   | `ICommenceDB::GetCursor <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceCursor::SeekRow
      :name: icommencecursorseekrow

   Long SeekRow(Long bkOrigin, Long nRows)

   Seek to a particular row in the cursor.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Return Value

   Returns Actual number of rows moved, -1 on error.

   Parameters

   bkOrigin

   Position to move from.

   Can be one of the following:

   BOOKMARK_BEGINNING (0) - from first row

   BOOKMARK_CURRENT (1) - from current row

   BOOKMARK_END (2) - from last row

    

   nRows

   Number of rows to move the current row pointer.

   Comments

   For any cursor, there is a 'current row pointer'. When the cursor is
   created, this defaults to the first row. SeekRow will reposition the
   current row pointer. GetQueryRowSet, GetEditRowSet and
   GetDeleteRowSet will also advance the current row pointer.

   See Also

   | `ICommenceCursor <javascript:RelatedTopic0.Click()>`__\ 
   | `RowCount <javascript:RelatedTopic1.Click()>`__\ 
   | `SeekRowApprox <javascript:RelatedTopic2.Click()>`__
   | `GetQueryRowSet <javascript:RelatedTopic3.Click()>`__
   | `GetEditRowSet <javascript:RelatedTopic4.Click()>`__
   | `GetDeleteRowSet <javascript:RelatedTopic5.Click()>`__

   .. rubric:: ICommenceCursor::SeekRowApprox
      :name: icommencecursorseekrowapprox

   Long SeekRowApprox(Long nNumerator, Long nDenominator)

   Seek to an approximate position in the cursor.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Return Value

   Returns Actual number of rows moved, -1 on error.

   Parameters

   nNumerator

   Numerator for fractional position in the cursor.

   nDenominator

   Denominator for the fractional position in the cursor.

   See Also

   | `ICommenceCursor <javascript:RelatedTopic0.Click()>`__\ 
   | `RowCount <javascript:RelatedTopic1.Click()>`__\ 
   | `SeekRow <javascript:RelatedTopic2.Click()>`__\ 
   | `GetQueryRowSet <javascript:RelatedTopic3.Click()>`__\ 
   | `GetEditRowSet <javascript:RelatedTopic4.Click()>`__\ 
   | `GetDeleteRowSet <javascript:RelatedTopic5.Click()>`__\ 

   .. rubric:: ICommenceCursor::GetQueryRowSet
      :name: icommencecursorgetqueryrowset

   ICommenceQueryRowSet GetQueryRowSet(Long nCount, Long nFlags)

   Create a rowset object with the results of a query.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Return Value

   Returns Pointer to rowset object on success, NULL on error.

   Parameters

   nCount

   Maximum number of rows to retrieve.

   nFlags

   Unused at present, must be 0.

   Comments

   The rowset inherits to column set from the cursor.

   The cursor's 'current row pointer' determines the first row to be
   included in the rowset.

   The returned rowset can have fewer than nCount rows (e.g. if the
   current row pointer is near the end). Use ICommenceXRowSet::RowCount
   to determine the actual row count.

   GetQueryRowSet will advance the 'current row pointer' by the number
   of rows in the rowset.

   See Also

   | 
   | `ICommenceCursor <javascript:RelatedTopic0.Click()>`__\ 
   | `ICommenceQueryRowSet <javascript:RelatedTopic1.Click()>`__\ 
   | `RowCount <javascript:RelatedTopic2.Click()>`__
   | `SeekRow <javascript:RelatedTopic3.Click()>`__
   | `SeekRowApprox <javascript:RelatedTopic4.Click()>`__

   .. rubric:: ICommenceCursor::GetQueryRowSetByID
      :name: icommencecursorgetqueryrowsetbyid

   ICommenceQueryRowSet GetQueryRowSetByID(String pRowID, Long nFlags)

   Create a rowset object with a particular row loaded.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Return Value

   Returns Pointer to rowset object on success, NULL on error.

   Parameters

   pRowID

   Unique ID string obtained from GetRowID().

   nFlags

   Unused at present, must be 0.

   Comments

   The rowset inherits to column set from the cursor.

   The cursor's 'current row pointer' is not advanced.

   See Also

   | `ICommenceCursor <javascript:RelatedTopic0.Click()>`__\ 
   | `ICommenceQueryRowSet::GetRowID <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceCursor::GetAddRowSet
      :name: icommencecursorgetaddrowset

   ICommenceAddRowSet GetAddRowSet(Long nCount, Long nFlags)

   Create a rowset of new items to add to the database.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Return Value

   Returns Pointer to rowset object on success, NULL on error.

   (Long nCount, Long nFlags)

   Parameters

   nCount

   Number of rows to create.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_SHARED - all rows default to shared

    

   Comments

   The rowset inherits the column set from the cursor.

   When first created, each row is initialized to field default values.

   See Also

   | `ICommenceCursor <javascript:RelatedTopic0.Click()>`__\ 
   | `ICommenceAddRowSet <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceCursor::GetEditRowSet
      :name: icommencecursorgeteditrowset

   ICommenceEditRowSet GetEditRowSet(Long nCount, Long nFlags)

   Create a rowset of existing items for editing.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Return Value

   Returns Pointer to rowset object on success, NULL on error.

   Parameters

   nCount

   Number of rows to retrieve.

   nFlags

   Unused at present, must be 0.

   Comments

   The rowset inherits the column set from the cursor.

   See Also

   | `ICommenceCursor <javascript:RelatedTopic0.Click()>`__\ 
   | `ICommenceEditRowSet <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceCursor::GetEditRowSetByID
      :name: icommencecursorgeteditrowsetbyid

   ICommenceEditRowSet GetEditRowSetByID(String pRowID, Long nFlags)

   Create a rowset for editing a particular row.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Return Value

   Returns Pointer to rowset object on success, NULL on error.

   Parameters

   pRowID

   Unique ID string obtained from GetRowID().

   nFlags

   Unused at present, must be 0.

   Comments

   The rowset inherits the column set from the cursor.

   The cursor's 'current row pointer' is not advanced.

   See Also

   | `ICommenceCursor <javascript:RelatedTopic0.Click()>`__\ 
   | `ICommenceQueryRowSet::GetRowID <javascript:RelatedTopic1.Click()>`__\ 
   | `ICommenceEditRowSet::GetRowID <javascript:RelatedTopic2.Click()>`__\ 
   | `ICommenceDeleteRowSet::GetRowID <javascript:RelatedTopic3.Click()>`__

   .. rubric:: ICommenceCursor::GetDeleteRowSet
      :name: icommencecursorgetdeleterowset

   ICommenceDeleteRowSet GetDeleteRowSet(Long nCount, Long nFlags)

   Create a rowset of existing items for deletion.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Return Value

   Returns Pointer to rowset object on success, NULL on error.

   Parameters

   nCount

   Number of rows to retrieve.

   nFlags

   Unused at present, must be 0.

   Comments

   The rowset inherits the column set from the cursor.

   See Also

   | `ICommenceCursor <javascript:RelatedTopic0.Click()>`__\ 
   | `ICommenceDeleteRowSet <javascript:RelatedTopic1.Click()>`__\ 

   .. rubric:: ICommenceCursor::GetDeleteRowSetByID
      :name: icommencecursorgetdeleterowsetbyid

   ICommenceDeleteRowSet GetDeleteRowSetByID(String pRowID, Long nFlags)

   Create a rowset for deleting a particular row.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Return Value

   Returns Pointer to rowset object on success, NULL on error.

   Parameters

   pRowID

   Unique ID string obtained from GetRowID().

   nFlags

   Unused at present, must be 0.

   Comments

   The rowset inherits the column set from the cursor.

   The cursor's 'current row pointer' is not advanced.

   See Also

   | `ICommenceCursor <javascript:RelatedTopic0.Click()>`__\ 
   | `ICommenceDeleteRowSet <javascript:RelatedTopic1.Click()>`__\ 
   | `ICommenceQueryRowSet::GetRowID <javascript:RelatedTopic2.Click()>`__\ 
   | `ICommenceEditRowSet::GetRowID <javascript:RelatedTopic3.Click()>`__\ 
   | `ICommenceDeleteRowSet::GetRowID <javascript:RelatedTopic4.Click()>`__\ 

   .. rubric:: ICommenceCursor::SetActiveItem
      :name: icommencecursorsetactiveitem

   Boolean SetActiveItem(String pCategoryName, String pRowID, Long
   flags)

   Set active item used for view cursors using a view linking filter.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Return Value

   Returns TRUE on success, else FALSE on error

   Parameters

   pCategoryName

   Category name of the active item used with view linking filter.

   pRowID

   Unique ID string obtained from GetRowID() indicating the active item
   used with view linking filter.

   flags

   Unused at present, must be 0.

   Comments

   This method is used with a view cursor using view linking by active
   item. This method enables the active item to be set via the API,
   separate from the active item in the Commence UI.

   See Also

   | `ICommenceCursor <javascript:RelatedTopic0.Click()>`__\ 
   | `SetActiveDate <javascript:RelatedTopic1.Click()>`__\ 
   | `SetActiveDateRange <javascript:RelatedTopic2.Click()>`__\ 
   | `ICommenceQueryRowSet::GetRowID <javascript:RelatedTopic3.Click()>`__\ 

   .. rubric:: ICommenceCursor::SetActiveDate
      :name: icommencecursorsetactivedate

   Boolean SetActiveDate(String sDate, Long flags)

   Set active date used for view cursors using a view linking filter.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Return Value

   Returns TRUE on success, else FALSE on error

   Parameters

   sDate

   Date value used with view linking filter; supports AI date values
   such as 'today'.

   flags

   Unused at present, must be 0.

   Comments

   This method is used with a view cursor using view linking by active
   date. This method enables the active date to be set via the API,
   separate from the active date in the Commence UI.

   See Also

   | `ICommenceCursor <javascript:RelatedTopic0.Click()>`__\ 
   | `SetActiveItem <javascript:RelatedTopic1.Click()>`__\ 
   | `SetActiveDateRange <javascript:RelatedTopic2.Click()>`__\ 

   .. rubric:: ICommenceCursor::SetActiveDateRange
      :name: icommencecursorsetactivedaterange

   Boolean SetActiveDateRange(String startDate, String endDate, Long
   flags)

   Set active date range used for view cursors using a view linking
   filter.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Return Value

   Returns TRUE on success, else FALSE on error

   Parameters

   startDate

   Date value of start date used with view linking filter; supports AI
   date values such as 'today'.

   endDate

   Date value of end date used with view linking filter; supports AI
   date values such as 'next monday'.

   flags

   Unused at present, must be 0.

   Comments

   This method is used with a view cursor using view linking by active
   date range. This method enables the active date range to be set via
   the API, separate from the active date range in the Commence UI.

   See Also

   | `ICommenceCursor <javascript:RelatedTopic0.Click()>`__\ 
   | `SetActiveItem <javascript:RelatedTopic1.Click()>`__\ 
   | `SetActiveDate <javascript:RelatedTopic2.Click()>`__\ 

   .. rubric:: ICommenceCursor::SetRelatedColumn
      :name: icommencecursorsetrelatedcolumn

   Boolean SetRelatedColumn(Long nColumn, String pConnName, String
   pCatName, String pName, Long nFlags)

   Adds a related (indirect/connected field) column to the cusor.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CURSOR.D

   Return Value

   Returns TRUE on success, FALSE on error.

   Parameters

   nColumn

   The (0-based) index of the column to set.

   pConnName

   Name of the connection to use in this column.

   pCatName

   Name of the connected Category to use in this column.

   pName

   Name of the field in the connected category to use in this column.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_ALL - create column set of all fields

    

   Comments

   When defining a column set, the columns must be defined in sequential
   order (0, 1, 2, etc.). This is to prevent problems with undefined
   columns (e.g. 0, 1, 3, ...).

   Duplicate columns are not supported. Each column must map to a
   different field.

   Not all Commence field types can be included in the cursor
   definition. The set of supported field types exactly matches those
   fields that can be displayed in a Commence report (minus combined
   fields and indirect fields).

   Sample call: SetRelatedColumn("Relates To", "History", "Date", 0)

   This call will add the Date field to the cursor via the 'Relates to
   History' connection.

   See Also

   | `ICommenceCursor <javascript:RelatedTopic0.Click()>`__\ 
   | `ICommenceDB::GetCursor <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceConversation Object
      :name: icommenceconversation-object

   Represents a DDE conversation.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CONVERSATION.D

   Methods

   Boolean Execute(String pDDECommand)

   Executes the DDE Command.

   String Request(String pDDECommand)

   Processes the DDE Request.

   .. rubric:: ICommenceConversation::Execute
      :name: icommenceconversationexecute

   Boolean Execute(String pDDECommand)

   Executes the DDE Command.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CONVERSATION.D

   Return Value

   Returns TRUE on success, FALSE on error.

   Parameters

   pDDECommand

   Text with the DDE command. Syntax is identical to the commands used
   by the DDE API.

   Comments

   TBD.

   See Also

   `ICommenceConversation <javascript:RelatedTopic0.Click()>`__\ 

   .. rubric:: ICommenceConversation::Request
      :name: icommenceconversationrequest

   String Request(String pDDECommand)

   Processes the DDE Request.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/CONVERSATION.D

   Return Value

   Returns String value on success.

   Parameters

   pDDECommand

   Text with the DDE Request. Syntax is identical to the commands used
   by the DDE API.

   Comments

   TBD.

   See Also

   `ICommenceConversation <javascript:RelatedTopic0.Click()>`__\ 

   .. rubric:: ICommenceAddRowSet Object
      :name: icommenceaddrowset-object

   Represents the set of new items to add to the database

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/ADD.D

   Properties

   Long ColumnCount

   (read-only) Number of columns in this rowset (-1 on error).

   Long RowCount

   (read-only) Number of rows in this rowset (-1 on error).

   Methods

   Long Commit

   Make row modifications permanent (commit to disk).

   `ICommenceCursor <#chmtopic11>`__\  CommitGetCursor

   Make row modifications permanent (commit to disk) and return a cursor

   Long GetColumnIndex

   Search the column set and return the index of the column with the
   given label.

   String GetColumnLabel

   Return the label associated with a paricular column.

   String GetRow

   Returns an entire row's field values.

   String GetRowValue

   Returns the field value at the given (row,column) in text form.

   Long ModifyRow

   Modify a field value in the rowset. for the newly added data.

   Boolean SetShared

   Mark a row to be shared.

   Boolean GetShared

   Return the row's current shared vs. local status.

   .. rubric:: ICommenceAddRowSet::ColumnCount
      :name: icommenceaddrowsetcolumncount

   Data Type

   Long

   Description

   (read-only) Number of columns in this rowset (-1 on error).

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/ADD.D

   See Also

   `ICommenceAddRowSet <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceAddRowSet::RowCount
      :name: icommenceaddrowsetrowcount

   Data Type

   Long

   Description

   (read-only) Number of rows in this rowset (-1 on error).

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/ADD.D

   See Also

   `ICommenceAddRowSet <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceAddRowSet::GetRowValue
      :name: icommenceaddrowsetgetrowvalue

   String GetRowValue(Long nRow, Long nCol, Long nFlags)

   Returns the field value at the given (row,column) in text form.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/ADD.D

   Return Value

   Returns Field value in text form on success, NULL on error.

   Parameters

   nRow

   The (0-based) index of the row.

   nCol

   The (0-based) index of the column.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_CANONICAL - return field value in canonical form

    

   Comments

   See the Developer Notes for more information about the canonical
   format.

   See Also

   | `ICommenceAddRowSet <javascript:RelatedTopic0.Click()>`__
   | `RowCount <javascript:RelatedTopic1.Click()>`__
   | `ColumnCount <javascript:RelatedTopic2.Click()>`__
   | `GetRow <javascript:RelatedTopic3.Click()>`__

   .. rubric:: ICommenceAddRowSet::GetColumnLabel
      :name: icommenceaddrowsetgetcolumnlabel

   String GetColumnLabel(Long nCol, Long nFlags)

   Return the label associated with a paricular column.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/ADD.D

   Return Value

   Returns Column label in text form on success, NULL on error.

   Parameters

   nCol

   The (0-based) index of the column.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_FIELD_NAME - return field label (ignore view labels)

    

   Comments

   If the cursor is created with CMC_CURSOR_VIEW, this will return the
   labels used with the view. Specify the CMC_FLAG_FIELD_NAME to force
   the underlying Commence field name to be returned.

   See Also

   | `ICommenceAddRowSet <javascript:RelatedTopic0.Click()>`__
   | `GetColumnIndex <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceAddRowSet::GetColumnIndex
      :name: icommenceaddrowsetgetcolumnindex

   Long GetColumnIndex(String pLabel, Long nFlags)

   Search the column set and return the index of the column with the
   given label.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/ADD.D

   Return Value

   Returns 0-based column index on success, -1 on error.

   Parameters

   pLabel

   The column label to map.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_FIELD_NAME - return field label (ignore view labels)

    

   Comments

   If the cursor is created with CMC_CURSOR_VIEW, this will first search
   the view labels for a possible match. If not found, the field labels
   will then be searched. Specify the CMC_FLAG_FIELD_NAME to force only
   the underlying Commence field name to be searched.

   See Also

   | `ICommenceAddRowSet <javascript:RelatedTopic0.Click()>`__
   | `GetColumnLabel <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceAddRowSet::ModifyRow
      :name: icommenceaddrowsetmodifyrow

   Long ModifyRow(Long nRow, Long nCol, String pBuf, Long nFlags)

   Modify a field value in the rowset.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/ADD.D

   Return Value

   Returns 0 on success, -1 on error.

   Parameters

   nRow

   The (0-based) index of the row.

   nCol

   The (0-based) index of the column.

   pBuf

   New field value in text form.

   nFlags

   Unused at present, must be 0.

   Comments

   Modifications to the rowset will be reflected by GetRowValue() and
   GetRow() but changes are not permanent until Commit() is called.

   See Also

   | `ICommenceAddRowSet <javascript:RelatedTopic0.Click()>`__
   | `Commit <javascript:RelatedTopic1.Click()>`__
   | `CommitGetCursor <javascript:RelatedTopic2.Click()>`__

   .. rubric:: ICommenceAddRowSet::Commit
      :name: icommenceaddrowsetcommit

   Long Commit(Long nFlags)

   Make row modifications permanent (commit to disk).

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/ADD.D

   Return Value

   Returns 0 on success, -1 on error.

   Parameters

   nFlags

   Unused at present, must be 0.

   Comments

   After Commit(), the ICommenceAddRowSet is no Longer valid and should
   be discarded.

   See Also

   | `ICommenceAddRowSet <javascript:RelatedTopic0.Click()>`__
   | `ModifyRow <javascript:RelatedTopic1.Click()>`__
   | `CommitGetCursor <javascript:RelatedTopic2.Click()>`__

   .. rubric:: ICommenceAddRowSet::CommitGetCursor
      :name: icommenceaddrowsetcommitgetcursor

   ICommenceCursor CommitGetCursor(Long nFlags)

   Make row modifications permanent (commit to disk) and return a cursor
   for the newly added data.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/ADD.D

   Return Value

   Returns ICommenceCursor object on success, NULL on error.

   Parameters

   nFlags

   Unused at present, must be 0.

   Comments

   After Commit(), the ICommenceAddRowSet is no Longer valid and should
   be discarded.

   See Also

   | `ICommenceAddRowSet <javascript:RelatedTopic0.Click()>`__
   | `ModifyRow <javascript:RelatedTopic1.Click()>`__
   | `Commit <javascript:RelatedTopic2.Click()>`__

   .. rubric:: ICommenceAddRowSet::GetRow
      :name: icommenceaddrowsetgetrow

   String GetRow(Long nRow, String pDelim, Long nFlags)

   Returns an entire row's field values.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/ADD.D

   Return Value

   Returns Row values in text form on success, NULL on error.

   Parameters

   nRow

   The (0-based) index of the row.

   pDelim

   Delimiter to use between field values.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_CANONICAL - return field value in canonical form

    

   Comments

   pDelim is used to separate field values. pDelim can be up to 20
   chars.

   Returned string is EOS terminated. Format is:
   <col1><delim><col2><delim>...<coln><EOS>

   See Also

   | `ICommenceAddRowSet <javascript:RelatedTopic0.Click()>`__
   | `GetRowValue <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceAddRowSet::SetShared
      :name: icommenceaddrowsetsetshared

   Boolean SetShared(Long nRow)

   Mark a row to be shared.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/ADD.D

   Return Value

   Returns TRUE on success, FALSE on error.

   Parameters

   nRow

   The (0-based) index of the row.

   Comments

   By default, all rows are marked local. To create a rowset with all
   rows marked as shared, call GetAddRowSet with the CMC_FLAG_SHARED
   flag.

   See Also

   | `ICommenceAddRowSet <javascript:RelatedTopic0.Click()>`__
   | `ICommenceCursor::GetAddRowSet <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceAddRowSet::GetShared
      :name: icommenceaddrowsetgetshared

   Boolean GetShared(Long nRow)

   Return the row's current shared vs. local status.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/ADD.D

   Return Value

   Returns TRUE if row is shared, FALSE otherwise.

   Parameters

   nRow

   The (0-based) index of the row.

   See Also

   `ICommenceAddRowSet <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceDeleteRowSet Object
      :name: icommencedeleterowset-object

   Represents the set of items to delete from the database.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DELETE.D

   Properties

   Long ColumnCount

   (read-only) Number of columns in this rowset (-1 on error).

   Long RowCount

   (read-only) Number of rows in this rowset (-1 on error).

   Methods

   String GetRowValue

   Returns the field value at the given (row,column) in text form.

   String GetColumnLabel

   Return the label associated with a paricular column.

   Long GetColumnIndex

   Search the column set and return the index of the column with the
   given label.

   Long DeleteRow

   Mark a row for deletion.

   Long Commit

   Make row modifications permanent (commit to disk).

   String GetRow

   Returns an entire row's field values.

   String GetRowID

   Returns a unique identifier for a row.

   Boolean GetShared

   Return the row's current shared vs. local status.

   .. rubric:: ICommenceDeleteRowSet::ColumnCount
      :name: icommencedeleterowsetcolumncount

   Data Type

   Long

   Description

   (read-only) Number of columns in this rowset (-1 on error).

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DELETE.D

   See Also

   `ICommenceDeleteRowSet <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceDeleteRowSet::RowCount
      :name: icommencedeleterowsetrowcount

   Data Type

   Long

   Description

   (read-only) Number of rows in this rowset (-1 on error).

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DELETE.D

   See Also

   `ICommenceDeleteRowSet <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceDeleteRowSet::GetRowValue
      :name: icommencedeleterowsetgetrowvalue

   String GetRowValue(Long nRow, Long nCol, Long nFlags)

   Returns the field value at the given (row,column) in text form.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DELETE.D

   Return Value

   Returns Field value in text form on success, NULL on error.

   Parameters

   nRow

   The (0-based) index of the row.

   nCol

   The (0-based) index of the column.

   nFlags

   option flags.

   Logical OR of following option flags:

   CMC_FLAG_CANONICAL - return field value in canonical form

    

   Comments

   See the Developer Notes for more information about the canonical
   format.

   See Also

   | `ICommenceDeleteRowSet <javascript:RelatedTopic0.Click()>`__
   | `RowCount <javascript:RelatedTopic1.Click()>`__
   | `ColumnCount <javascript:RelatedTopic2.Click()>`__
   | `GetRow <javascript:RelatedTopic3.Click()>`__

   .. rubric:: ICommenceDeleteRowSet::GetColumnLabel
      :name: icommencedeleterowsetgetcolumnlabel

   String GetColumnLabel(Long nCol, Long nFlags)

   Return the label associated with a paricular column.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DELETE.D

   Return Value

   Returns Column label in text form on success, NULL on error.

   Parameters

   nCol

   The (0-based) index of the column.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_FIELD_NAME - return field label (ignore view labels)

    

   Comments

   If the cursor is created with CMC_CURSOR_VIEW, this will return the
   labels used with the view. Specify the CMC_FLAG_FIELD_NAME to force
   the underlying Commence field name to be returned.

   See Also

   | `ICommenceDeleteRowSet <javascript:RelatedTopic0.Click()>`__
   | `GetColumnIndex <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceDeleteRowSet::GetColumnIndex
      :name: icommencedeleterowsetgetcolumnindex

   Long GetColumnIndex(String pLabel, Long nFlags)

   Search the column set and return the index of the column with the
   given label.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DELETE.D

   Return Value

   Returns 0-based column index on success, -1 on error.

   Parameters

   pLabel

   The column label to map.

   nFlags

   option flags.

   Logical OR of following option flags:

   CMC_FLAG_FIELD_NAME - return field label (ignore view labels)

    

   Comments

   If the cursor is created with CMC_CURSOR_VIEW, this will first search
   the view labels for a possible match. If not found, the field labels
   will then be searched. Specify the CMC_FLAG_FIELD_NAME to force only
   the underlying Commence field name to be searched.

   See Also

   | `ICommenceDeleteRowSet <javascript:RelatedTopic0.Click()>`__
   | `GetColumnLabel <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceDeleteRowSet::DeleteRow
      :name: icommencedeleterowsetdeleterow

   Long DeleteRow(Long nRow, Long nFlags)

   Mark a row for deletion.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DELETE.D

   Return Value

   Returns 0 on success, -1 on error.

   Parameters

   nRow

   The (0-based) index of the row.

   nFlags

   Unused at present, must be 0.

   Comments

   Deletion is not permanent until Commit() is called.

   See Also

   | `ICommenceDeleteRowSet <javascript:RelatedTopic0.Click()>`__
   | `Commit <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceDeleteRowSet::Commit
      :name: icommencedeleterowsetcommit

   Long Commit(Long nFlags)

   Make row modifications permanent (commit to disk).

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DELETE.D

   Return Value

   Returns 0 on success, -1 on error.

   Parameters

   nFlags

   Unused at present, must be 0.

   Comments

   After Commit(), the ICommenceDeleteRowSet is no Longer valid and
   should be discarded.

   See Also

   | `ICommenceDeleteRowSet <javascript:RelatedTopic0.Click()>`__
   | `DeleteRow <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceDeleteRowSet::GetRow
      :name: icommencedeleterowsetgetrow

   String GetRow(Long nRow, String pDelim, Long nFlags)

   Returns an entire row's field values.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DELETE.D

   Return Value

   Returns Row values in text form on success, NULL on error.

   Parameters

   nRow

   The (0-based) index of the row.

   pDelim

   Delimiter to use between field values.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_CANONICAL - return field value in canonical form

    

   Comments

   pDelim is used to separate field values. pDelim can be up to 20
   chars.

   Returned string is EOS terminated. Format is:
   <col1><delim><col2><delim>...<coln><EOS>

   See Developer Notes for more information on canonical format.

   See Also

   | `ICommenceDeleteRowSet <javascript:RelatedTopic0.Click()>`__
   | `GetRowValue <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceDeleteRowSet::GetRowID
      :name: icommencedeleterowsetgetrowid

   String GetRowID(Long nRow, Long nFlags)

   Returns a unique identifier for a row.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DELETE.D

   Return Value

   Returns a unique ID string (less than 100 chars) on success, NULL on
   error.

   Parameters

   nRow

   The (0-based) index of the row.

   nFlags

   Unused at present, must be 0.

   Comments

   Unlike the row number, this ID value is valid across cursor sessions.

   The 'scope' of the ID value is the Commence database from which it
   was retrieved. The ID value is not valid in other Commence databases,
   even if they are in the same workgroup and sync.

   Do not make any assumptions about the contents of the returned ID
   string. Format may change in the future.

   See Also

   | `ICommenceDeleteRowSet <javascript:RelatedTopic0.Click()>`__
   | `ICommenceCursor::GetEditRowSetByID <javascript:RelatedTopic1.Click()>`__
   | `ICommenceCursor::GetDeleteRowSetByID <javascript:RelatedTopic2.Click()>`__

   .. rubric:: ICommenceDeleteRowSet::GetShared
      :name: icommencedeleterowsetgetshared

   Boolean GetShared(Long nRow)

   Return the row's current shared vs. local status.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/DELETE.D

   Return Value

   Returns TRUE if row is shared, FALSE otherwise.

   Parameters

   nRow

   The (0-based) index of the row.

   See Also

   `ICommenceDeleteRowSet <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceEditRowSet Object
      :name: icommenceeditrowset-object

   Represents the set of items to edit in the database.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/EDIT.D

   Properties

   Long ColumnCount

   (read-only) Number of columns in this rowset (-1 on error).

   Long RowCount

   (read-only) Number of rows in this rowset (-1 on error).

   Methods

   String GetRowValue

   Returns the field value at the given (row,column) in text form.

   String GetColumnLabel

   Return the label associated with a paricular column.

   Long GetColumnIndex

   Search the column set and return the index of the column with the
   given label.

   Long ModifyRow

   Modify a field value in the rowset.

   Long Commit

   Make row modifications permanent (commit to disk).

   `ICommenceCursor <#chmtopic11>`__\  CommitGetCursor

   Make row modifications permanent (commit to disk) and return a cursor
   for the newly added data.

   String GetRow

   Returns an entire row's field values.

   Boolean GetShared

   Return the row's current shared vs. local status.

   Boolean SetShared

   Mark a row to be shared.

   String GetRowID

   Returns a unique identifier for a row.

   .. rubric:: ICommenceEditRowSet::ColumnCount
      :name: icommenceeditrowsetcolumncount

   Data Type

   Long

   Description

   (read-only) Number of columns in this rowset (-1 on error).

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/EDIT.D

   See Also

   `ICommenceEditRowSet <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceEditRowSet::RowCount
      :name: icommenceeditrowsetrowcount

   Data Type

   Long

   Description

   (read-only) Number of rows in this rowset (-1 on error).

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/EDIT.D

   See Also

   `ICommenceEditRowSet <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceEditRowSet::GetRowValue
      :name: icommenceeditrowsetgetrowvalue

   String GetRowValue(Long nRow, Long nCol, Long nFlags)

   Returns the field value at the given (row,column) in text form.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/EDIT.D

   Return Value

   Returns Field value in text form on success, NULL on error.

   Parameters

   nRow

   The (0-based) index of the row.

   nCol

   The (0-based) index of the column.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_CANONICAL - return field value in canonical form

    

   Comments

   See the Developer Notes for more information about the canonical
   format.

   See Also

   | `ICommenceEditRowSet <javascript:RelatedTopic0.Click()>`__
   | `RowCount <javascript:RelatedTopic1.Click()>`__
   | `ColumnCount <javascript:RelatedTopic2.Click()>`__
   | `GetRow <javascript:RelatedTopic3.Click()>`__

   .. rubric:: ICommenceEditRowSet::GetColumnLabel
      :name: icommenceeditrowsetgetcolumnlabel

   String GetColumnLabel(Long nCol, Long nFlags)

   Return the label associated with a paricular column.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/EDIT.D

   Return Value

   Returns Column label in text form on success, NULL on error.

   Parameters

   nCol

   The (0-based) index of the column.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_FIELD_NAME - return field label (ignore view labels)

    

   Comments

   If the cursor is created with CMC_CURSOR_VIEW, this will return the
   labels used with the view. Specify the CMC_FLAG_FIELD_NAME to force
   the underlying Commence field name to be returned.

   See Also

   | `ICommenceEditRowSet <javascript:RelatedTopic0.Click()>`__
   | `GetColumnIndex <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceEditRowSet::GetColumnIndex
      :name: icommenceeditrowsetgetcolumnindex

   Long GetColumnIndex(String pLabel, Long nFlags)

   Search the column set and return the index of the column with the
   given label.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/EDIT.D

   Return Value

   Returns 0-based column index on success, -1 on error.

   Parameters

   pLabel

   The column label to map.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_FIELD_NAME - return field label (ignore view labels)

    

   Comments

   If the cursor is created with CMC_CURSOR_VIEW, this will first search
   the view labels for a possible match. If not found, the field labels
   will then be searched. Specify the CMC_FLAG_FIELD_NAME to force only
   the underlying Commence field name to be searched.

   See Also

   | `ICommenceEditRowSet <javascript:RelatedTopic0.Click()>`__
   | `GetColumnLabel <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceEditRowSet::ModifyRow
      :name: icommenceeditrowsetmodifyrow

   Long ModifyRow(Long nRow, Long nCol, String pBuf, Long nFlags)

   Modify a field value in the rowset.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/EDIT.D

   Return Value

   Returns 0 on success, -1 on error.

   Parameters

   nRow

   The (0-based) index of the row.

   nCol

   The (0-based) index of the column.

   pBuf

   New field value in text form.

   nFlags

   Unused at present, must be 0.

   Comments

   Modifications to the rowset will be reflected by GetRowValue() and
   GetRow() but changes are not permanent until Commit() is called.

   See Also

   | `ICommenceEditRowSet <javascript:RelatedTopic0.Click()>`__
   | `Commit <javascript:RelatedTopic1.Click()>`__
   | `CommitGetCursor <javascript:RelatedTopic2.Click()>`__

   .. rubric:: ICommenceEditRowSet::Commit
      :name: icommenceeditrowsetcommit

   Long Commit(Long nFlags)

   Make row modifications permanent (commit to disk).

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/EDIT.D

   Return Value

   Returns 0 on success, -1 on error.

   Parameters

   nFlags

   Unused at present, must be 0.

   Comments

   After Commit(), the ICommenceEditRowSet is no Longer valid and should
   be discarded.

   See Also

   | `ICommenceEditRowSet <javascript:RelatedTopic0.Click()>`__
   | `ModifyRow <javascript:RelatedTopic1.Click()>`__
   | `CommitGetCursor <javascript:RelatedTopic2.Click()>`__

   .. rubric:: ICommenceEditRowSet::CommitGetCursor
      :name: icommenceeditrowsetcommitgetcursor

   ICommenceCursor CommitGetCursor(Long nFlags)

   Make row modifications permanent (commit to disk) and return a cursor
   for the newly added data.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/EDIT.D

   Return Value

   Returns ICommenceCursor object on success, NULL on error.

   Parameters

   nFlags

   Unused at present, must be 0.

   Comments

   After Commit(), the ICommenceEditRowSet is no Longer valid and should
   be discarded.

   See Also

   | `ICommenceEditRowSet <javascript:RelatedTopic0.Click()>`__
   | `ModifyRow <javascript:RelatedTopic1.Click()>`__
   | `Commit <javascript:RelatedTopic2.Click()>`__

   .. rubric:: ICommenceEditRowSet::GetRow
      :name: icommenceeditrowsetgetrow

   String GetRow(Long nRow, String pDelim, Long nFlags)

   Returns an entire row's field values.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/EDIT.D

   Return Value

   Returns Row values in text form on success, NULL on error.

   Parameters

   nRow

   The (0-based) index of the row.

   pDelim

   Delimiter to use between field values.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_CANONICAL - return field value in canonical form

    

   Comments

   pDelim is used to separate field values. pDelim can be up to 20
   chars.

   Returned string is EOS terminated. Format is:
   <col1><delim><col2><delim>...<coln><EOS>

   See the Developer Notes for more information about the canonical
   format.

   See Also

   | `ICommenceEditRowSet <javascript:RelatedTopic0.Click()>`__
   | `GetRowValue <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceEditRowSet::GetShared
      :name: icommenceeditrowsetgetshared

   Boolean GetShared(Long nRow)

   Return the row's current shared vs. local status.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/EDIT.D

   Return Value

   Returns TRUE if row is shared, FALSE otherwise.

   Parameters

   nRow

   The (0-based) index of the row.

   See Also

   | `ICommenceEditRowSet <javascript:RelatedTopic0.Click()>`__
   | `SetShared <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceEditRowSet::SetShared
      :name: icommenceeditrowsetsetshared

   Boolean SetShared(Long nRow)

   Mark a row to be shared.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/EDIT.D

   Return Value

   Returns TRUE on success, FALSE on error.

   Parameters

   nRow

   The (0-based) index of the row.

   See Also

   | `ICommenceEditRowSet <javascript:RelatedTopic0.Click()>`__
   | `GetShared <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceEditRowSet::GetRowID
      :name: icommenceeditrowsetgetrowid

   String GetRowID(Long nRow, Long nFlags)

   Returns a unique identifier for a row.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/EDIT.D

   Return Value

   Returns a unique ID string (less than 100 chars) on success, NULL on
   error.

   Parameters

   nRow

   The (0-based) index of the row.

   nFlags

   Unused at present, must be 0.

   Comments

   Unlike the row number, this ID value is valid across cursor sessions.

   The 'scope' of the ID value is the Commence database from which it
   was retrieved. The ID value is not valid in other Commence databases,
   even if they are in the same workgroup and sync.

   Do not make any assumptions about the contents of the returned ID
   string. Format may change in the future.

   See Also

   | `ICommenceEditRowSet <javascript:RelatedTopic0.Click()>`__
   | `ICommenceCursor::GetQueryRowSetByID <javascript:RelatedTopic1.Click()>`__
   | `ICommenceCursor::GetEditRowSetByID <javascript:RelatedTopic2.Click()>`__
   | `ICommenceCursor::GetDeleteRowSetByID <javascript:RelatedTopic3.Click()>`__

   .. rubric:: ICommenceQueryRowSet Object
      :name: icommencequeryrowset-object

   Represents a result set from a query

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/QUERY.D

   Properties

   Long ColumnCount

   (read-only) Number of columns in this rowset (-1 on error).

   Long RowCount

   (read-only) Number of rows in this rowset (-1 on error).

   Methods

   String GetRowValue

   Returns the field value at the given (row,column) in text form.

   String GetColumnLabel

   Return the label associated with a paricular column.

   Long GetColumnIndex

   Search the column set and return the index of the column with the
   given label.

   String GetRow

   Returns an entire row's field values.

   String GetRowID

   Returns a unique identifier for a row.

   Boolean GetShared

   Return the row's current shared vs. local status.

   Long GetFieldToFile

   Save the field value at the given (row,column) to a file.

   .. rubric:: ICommenceQueryRowSet::ColumnCount
      :name: icommencequeryrowsetcolumncount

   Data Type

   Long

   Description

   (read-only) Number of columns in this rowset (-1 on error).

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/QUERY.D

   See Also

   `ICommenceQueryRowSet <javascript:RelatedTopic0.Click()>`__\ 

   .. rubric:: ICommenceQueryRowSet::RowCount
      :name: icommencequeryrowsetrowcount

   Data Type

   Long

   Description

   (read-only) Number of rows in this rowset (-1 on error).

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/QUERY.D

   See Also

   `ICommenceQueryRowSet <javascript:RelatedTopic0.Click()>`__\ 

   .. rubric:: ICommenceQueryRowSet::GetRowValue
      :name: icommencequeryrowsetgetrowvalue

   String GetRowValue(Long nRow, Long nCol, Long nFlags)

   Returns the field value at the given (row,column) in text form.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/QUERY.D

   Return Value

   Returns Field value in text form on success, NULL on error.

   Parameters

   nRow

   The (0-based) index of the row.

   nCol

   The (0-based) index of the column.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_CANONICAL - return field value in canonical form

    

   Comments

   See the Developer Notes about canonical format.

   See Also

   | `ICommenceQueryRowSet <javascript:RelatedTopic0.Click()>`__\ 
   | `RowCount <javascript:RelatedTopic1.Click()>`__
   | `ColumnCount <javascript:RelatedTopic2.Click()>`__
   | `GetRow <javascript:RelatedTopic3.Click()>`__
   | `GetFieldToFile <javascript:RelatedTopic4.Click()>`__

   .. rubric:: ICommenceQueryRowSet::GetColumnLabel
      :name: icommencequeryrowsetgetcolumnlabel

   String GetColumnLabel(Long nCol, Long nFlags)

   Return the label associated with a paricular column.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/QUERY.D

   Return Value

   Returns Column label in text form on success, NULL on error.

   Parameters

   nCol

   The (0-based) index of the column.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_FIELD_NAME - return field label (ignore view labels)

    

   Comments

   If the cursor is created with CMC_CURSOR_VIEW, this will return the
   labels used with the view. Specify the CMC_FLAG_FIELD_NAME to force
   the underlying Commence field name to be returned.

   See Also

   | `ICommenceQueryRowSet <javascript:RelatedTopic0.Click()>`__\ 
   | `GetColumnIndex <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceQueryRowSet::GetColumnIndex
      :name: icommencequeryrowsetgetcolumnindex

   Long GetColumnIndex(String pLabel, Long nFlags)

   Search the column set and return the index of the column with the
   given label.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/QUERY.D

   Return Value

   Returns 0-based column index on success, -1 on error.

   Parameters

   pLabel

   The column label to map.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_FIELD_NAME - return field label (ignore view labels)

    

   Comments

   If the cursor is created with CMC_CURSOR_VIEW, this will first search
   the view labels for a possible match. If not found, the field labels
   will then be searched. Specify the CMC_FLAG_FIELD_NAME to force only
   the underlying Commence field name to be searched.

   See Also

   | `ICommenceQueryRowSet <javascript:RelatedTopic0.Click()>`__\ 
   | `GetColumnLabel <javascript:RelatedTopic1.Click()>`__

   .. rubric:: ICommenceQueryRowSet::GetRow
      :name: icommencequeryrowsetgetrow

   String GetRow(Long nRow, String pDelim, Long nFlags)

   Returns an entire row's field values.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/QUERY.D

   Return Value

   Returns Row values in text form on success, NULL on error.

   (Long nRow, String pDelim, Long nFlags)

   Parameters

   nRow

   The (0-based) index of the row.

   pDelim

   Delimiter to use between field values.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_CANONICAL - return field value in canonical form

    

   Comments

   pDelim is used to separate field values. pDelim can be up to 20
   chars.

   Returned string is EOS terminated. Format is:
   <col1><delim><col2><delim>...<coln><EOS>

   See Developer Notes for more information about the canonical format.

   See Also

   | `ICommenceQueryRowSet <javascript:RelatedTopic0.Click()>`__\ 
   | `GetRowValue <javascript:RelatedTopic1.Click()>`__
   | `GetFieldToFile <javascript:RelatedTopic2.Click()>`__

   .. rubric:: ICommenceQueryRowSet::GetRowID
      :name: icommencequeryrowsetgetrowid

   String GetRowID(Long nRow, Long nFlags)

   Returns a unique identifier for a row.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/QUERY.D

   Return Value

   Returns a unique ID string (less than 100 chars) on success, NULL on
   error.

   Parameters

   nRow

   The (0-based) index of the row.

   nFlags

   Unused at present, must be 0.

   Comments

   Unlike the row number, this ID value is valid across cursor sessions.

   The 'scope' of the ID value is the Commence database from which it
   was retrieved. The ID value is not valid in other Commence databases,
   even if they are in the same workgroup and sync.

   Do not make any assumptions about the contents of the returned ID
   string. Format may change in the future.

   Not yet supported but the unique ID will be useful in the future to
   edit/delete a particular item.

   See Also

   `ICommenceQueryRowSet <javascript:RelatedTopic0.Click()>`__\ 

   .. rubric:: ICommenceQueryRowSet::GetShared
      :name: icommencequeryrowsetgetshared

   Boolean GetShared(Long nRow)

   Return the row's current shared vs. local status.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/QUERY.D

   Return Value

   Returns TRUE if row is shared, FALSE otherwise.

   Parameters

   nRow

   The (0-based) index of the row.

   See Also

   `ICommenceQueryRowSet <javascript:RelatedTopic0.Click()>`__

   .. rubric:: ICommenceQueryRowSet::GetFieldToFile
      :name: icommencequeryrowsetgetfieldtofile

   Long GetFieldToFile(Long nRow, Long nCol, String filename, Long
   nFlags)

   Save the field value at the given (row,column) to a file.

   Defined in: E:/DEV/PIM80/DOCS/DBAPI/PIMOA/QUERY.D

   Return Value

   Returns the file size in bytes, or -1 on error.

   Parameters

   nRow

   The (0-based) index of the row.

   nCol

   The (0-based) index of the column.

   filename

   Filename and path where the field value is written.

   nFlags

   option flags

   Logical OR of following option flags:

   CMC_FLAG_CANONICAL - return field value in canonical form

    

   Comments

   If there is no data in the indicated column, the return code is 0 and
   a file is not written. Otherwise, a file is created with the field's
   data and the size of the data is returned.

   See the Developer Notes about canonical format.

   See Also

   | `ICommenceQueryRowSet <javascript:RelatedTopic0.Click()>`__\ 
   | `GetRowValue <javascript:RelatedTopic1.Click()>`__
   | `GetRow <javascript:RelatedTopic2.Click()>`__

   .. rubric:: Constants
      :name: constants

    

   Flags used with GetCursor

   CMC_CURSOR_CATEGORY = 0

   open based on a category

   CMC_CURSOR_VIEW = 1

   open based on a view

   CMC_CURSOR_PILOTAB = 2

   3Com Pilot Address Book

   CMC_CURSOR_PILOTMEMO= 3

   3Com Pilot Memo

   CMC_CURSOR_PILOTTODO= 5

   3Com Pilot to-do list

   CMC_CURSOR_PILOTAPPT= 6

   3Com Pilot appt calendar

   CMC_CURSOR_OUTLOOKAB= 7

   MS Outlook contacts preference

   CMC_CURSOR_OUTLOOKAPPT=8

   MS Outlook calendar preference

   CMC_CURSOR_EMAILLOG=9

   MS Outlook Email Log preference

   CMC_CURSOR_OUTLOOKTASK=10

   MS Outlook Task preference

   CMC_CURSOR_MERGE=11

   open based on the view data used with the Send Letter command

   Flags used with SeekRow

   BOOKMARK_BEGINNING = 0

   Offset from beginning of the rowset.

   BOOKMARK_CURRENT = 1

   Offset from current position.

   BOOKMARK_END = 2

   Offset from end of the rowset.

   Option Flags

   CMC_FLAG_FIELD_NAME = &H0001

   return actual field name

   CMC_FLAG_ALL = &H0002

   include all fields

   CMC_FLAG_SHARED = &H0004

   init as shared

   CMC_FLAG_PILOT = &H0008

   changes from 3Com Pilot

   CMC_FLAG_CANONICAL = &H0010

   data in canonical format

   CMC_FLAG_INTERNET = &H0020

   changes from Internet

   .. rubric:: Developer Notes
      :name: developer-notes

   The following topics contain technical notes about the Database API.

   `3Com Pilot support <#chmtopic84>`__

   `Canonical Format <#chmtopic85>`__

   `CMC_FLAG_PILOT <#chmtopic86>`__

   `CMC_FLAG_INTERNET <#chmtopic87>`__

   .. rubric:: Palm Pilot support
      :name: palm-pilot-support

   For CMC_CURSOR_PILOTx cursor modes, Commence will use the 'Sync
   Condition' field (which must be a checkbox or a connection to the
   "(-me-)" item) to determine which items appear in the cursor. The
   column set only includes fields for which mappings exist.

   For example, if the user did not select a Fax Number field, then it
   will not appear in the column set. This means GetColumIndex("Fax
   Number", 0) can and will fail.

   If 'Sync Condition' is not mapped to a Commence field, then all items
   in the category will appear in the cursor.

   .. rubric:: Canonical Format
      :name: canonical-format

   By default, data values are returned formatted according to the local
   Control Panel settings. Where applicable, specifying
   CMC_FLAG_CANONICAL will return data in a consistent format.

   Data Type Format Notes

    

   Date yyyymmdd

   Time hh:mm military time, 24 hour clock

   Number 123456.78 no separator, period for decimal delimiter

   Checkbox TRUE or FALSE English

   .. rubric:: CMC_FLAG_PILOT
      :name: cmc_flag_pilot

   The Save Item trigger can be configured to fire only if an item is
   added or edited by specific subsystems. As part of Pilot support, the
   Save Item Options dialog box will include a Pilot Link check box
   (SS_PILOT).

   By default, a cursor in CMC_CURSOR_PILOTx mode will assume SS_PILOT
   mode. When using other cursor modes, specifying CMC_FLAG_PILOT will
   force SS_PILOT mode.

   .. rubric:: CMC_FLAG_INTERNET
      :name: cmc_flag_internet

   The Save Item trigger can be configured to fire only if an item is
   added or edited by specific subsystems. As part of Commence Web
   support, the Save Item Options dialog box will include a
   Internet/Intranet check box (SS_INTERNET).

   Specifying CMC_FLAG_INTERNET will allow SS_INTERNET agents to fire.
