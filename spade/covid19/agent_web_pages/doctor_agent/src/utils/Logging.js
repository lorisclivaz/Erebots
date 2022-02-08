/** Internal function refactoring common logging logic */
function _log(logger, currentScriptName, text, object = undefined) {
  if (object === undefined)
    logger("[" + currentScriptName + "]: " + text);
  else {
    logger("[" + currentScriptName + "]: " + text + " " + JSON.stringify(object));
    logger(object)
  }
}

function log(currentScriptName, text, object = undefined) {
  _log(console.log, currentScriptName, text, object)
}

function debug(currentScriptName, text, object = undefined) {
  _log(console.debug, currentScriptName, text, object)
}

function info(currentScriptName, text, object = undefined) {
  _log(console.info, currentScriptName, text, object)
}

function warn(currentScriptName, text, object = undefined) {
  _log(console.warn, currentScriptName, text, object)
}

function error(currentScriptName, text, object = undefined) {
  _log(console.error, currentScriptName, text, object)
}

export {log, debug, info, warn, error}
