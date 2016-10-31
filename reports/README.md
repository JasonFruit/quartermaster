Report format
======================================================================

The report format is valid SQL, with a top comment that has on its
first line a title, then a blank line, and then any number of
succeeding lines of description.  Everything after the final comment
line (including later, non-contiguous comments) is treated as the SQL
to generate the report.

For example:

    -- This is the report title
	--
	-- Here is the description of the report.  It can be as
	-- many lines as you would like.  There can even be
	-- blank lines like the following:
	--
	-- And other non-blank lines afterwards.  Now comes the SQL:
	select a as [A nice header], ...
	
Note that the column names are used as headers in the visible report,
so please try to make them meaningful and human-readable.
