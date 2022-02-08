const DATE_OBJECT_FIELD_NAME = "$date";

/** A function to check whether the provided value is a datetime object received from python server backend */
function checkDatetimeValue(datetimeFieldValue) {
  return (typeof datetimeFieldValue == 'object' && typeof datetimeFieldValue[DATE_OBJECT_FIELD_NAME] == 'number')
}

/**
 * A function to extract the datetime field value from Server received objects
 *
 * If the given value is not a datetime field value, then the value is returned untouched
 */
function extractDateObject(datetimeFieldValue) {
  if (checkDatetimeValue(datetimeFieldValue))
    return new Date(datetimeFieldValue[DATE_OBJECT_FIELD_NAME]);
  else
    return datetimeFieldValue
}

/** Converts a non UTC date obj or millis, to millis in UTC time */
function convertToUTCMillis(date) {
  if (typeof date === 'number')
    return date + new Date().getTimezoneOffset() * 60 * 1000;
  else
    return date.getTime() + date.getTimezoneOffset() * 60 * 1000;
}

/** Converts anUTC date obj or millis, to millis in local time */
function convertToLocalMillis(date) {
  if (typeof date == 'number')
    return date - new Date().getTimezoneOffset() * 60 * 1000;
  else
    return date.getTime() - date.getTimezoneOffset() * 60 * 1000
}

export {checkDatetimeValue, extractDateObject, convertToUTCMillis, convertToLocalMillis, DATE_OBJECT_FIELD_NAME}
