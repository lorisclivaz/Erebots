/**
 * A function to convert milliseconds to human readable time duration
 *
 * Taken from: https://gist.github.com/robertpataki/d0b40a1cbbb71764dd94e16cbc99d42f
 * and https://gist.github.com/Erichain/6d2c2bf16fe01edfcffa
 */
function millisToDurationString(millis, delimiter = " : ") {
  const showWith0 = value => (value < 10 ? `0${value}` : value);
  let seconds = Math.floor(millis / 1000);
  let minute = Math.floor(seconds / 60);
  seconds = seconds % 60;
  let hour = Math.floor(minute / 60);
  minute = minute % 60;
  let day = Math.floor(hour / 24);
  hour = hour % 24;

  const dayString = `${day}`
  const hourString = showWith0(hour)
  const minuteString = showWith0(minute)
  const secondsString = showWith0(seconds)
  return `${day ? `${dayString}d${delimiter}` : ""}${hour ? `${hourString}h${delimiter}` : ""}${minuteString}m${delimiter}${secondsString}s`;
}

export {millisToDurationString}
