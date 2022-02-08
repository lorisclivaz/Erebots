/**
 * Used to map a month index to the month name
 *
 * Example:
 *
 * ```javascript
 * monthName[new Date().getMonth()]
 * ```
 *
 * will return the name of the current month
 */
const monthName = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December'
];

/**
 * Used to map a day index to the weekday name
 *
 * Example:
 *
 * ```javascript
 * weekDayName[new Date().getDay()]
 * ```
 *
 * will return the name of the current week day
 */
const weekDayName = [
  'Sunday',
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday'
];

const ONE_HOUR_IN_MILLIS = 3.6e+6;
const ONE_DAY_IN_MILLIS = 8.64e+7;
const ONE_WEEK_IN_MILLIS = 6.048e+8;
const ONE_MONTH_IN_MILLIS = 2.628e+9;
const ONE_YEAR_IN_MILLIS = 3.154e+10;

/** A function taking a data object and making it become a pretty string, optionally showing time or date */
function dateToPrettyString(dateObj, time = true, date = true) {
  if (typeof dateObj === 'number')
    dateObj = new Date(dateObj)

  if (time && date)
    return dateObj.toLocaleString('en-GB', {timeZone: 'UTC'});
  else if (time)
    return dateObj.toLocaleTimeString('en-GB', {timeZone: 'UTC'});
  else
    return dateObj.toLocaleDateString('en-GB', {timeZone: 'UTC'})
}

export {
  weekDayName,
  monthName,
  ONE_HOUR_IN_MILLIS,
  ONE_DAY_IN_MILLIS,
  ONE_WEEK_IN_MILLIS,
  ONE_MONTH_IN_MILLIS,
  ONE_YEAR_IN_MILLIS,
  dateToPrettyString
}
