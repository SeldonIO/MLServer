# Module `mlserver.logging`


## Class `ModelLoggerFormatter`


**Description:**
Log formatter incorporating model details, e.g. name and version.

### Method `format`


**Signature:** `format(self, record: logging.LogRecord) -> str`


**Description:**
Format the specified record as text.
The record's attribute dictionary is used as the operand to a
string formatting operation which yields the returned string.
Before formatting the dictionary, a couple of preparatory steps
are carried out. The message attribute of the record is computed
using LogRecord.getMessage(). If the formatting string uses the
time (as determined by a call to usesTime(), formatTime() is
called to format the event time. If there is exception information,
it is formatted using formatException() and appended to the message.

### Method `formatException`


**Signature:** `formatException(self, ei)`


**Description:**
Format and return the specified exception information as a string.
This default implementation just uses
traceback.print_exception()

### Method `formatMessage`


**Signature:** `formatMessage(self, record)`


**Description:**
*No docstring available.*

### Method `formatStack`


**Signature:** `formatStack(self, stack_info)`


**Description:**
This method is provided as an extension point for specialized
formatting of stack information.

The input data is a string as returned from a call to

### Method `formatTime`


**Signature:** `formatTime(self, record, datefmt=None)`


**Description:**
Return the creation time of the specified LogRecord as formatted text.
This method should be called from format() by a formatter which
wants to make use of a formatted time. This method can be overridden
in formatters to provide for any specific requirement, but the
basic behaviour is as follows: if datefmt (a string) is specified,
it is used with time.strftime() to format the creation time of the
record. Otherwise, an ISO8601-like (or RFC 3339-like) format is used.
The resulting string is returned. This function uses a user-configurable
function to convert the creation time to a tuple. By default,
time.localtime() is used; to change this for a particular formatter
instance, set the 'converter' attribute to a function with the same
signature as time.localtime() or time.gmtime(). To change it for all
formatters, for example if you want all logging times to be shown in GMT,
set the 'converter' attribute in the Formatter class.

### Method `usesTime`


**Signature:** `usesTime(self)`


**Description:**
Check if the format uses the creation time of the record.

## Function `apply_logging_file`


**Signature:** `apply_logging_file(logging_settings: Union[str, Dict])`


**Description:**
*No docstring available.*

## Function `configure_logger`


**Signature:** `configure_logger(settings: Optional[mlserver.settings.Settings] = None)`


**Description:**
*No docstring available.*

## Function `get_logger`


**Signature:** `get_logger()`


**Description:**
*No docstring available.*
