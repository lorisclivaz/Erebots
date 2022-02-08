import {log} from "../utils/Logging";
import {AppState} from "../model/AppState";

const STATE_NAME_COOKIE = 'local_state';
const currentScriptName = "CookiesController.js";

class CookiesController {

  constructor(cookies, loggingEnabled = true) {
    this.cookies = cookies;
    this.loggingEnabled = loggingEnabled;
  }

  saveStateToCookies(toSaveState) {
    if (this.loggingEnabled)
      log(currentScriptName, "Will save state to cookies:", toSaveState);

    // makes the cookie accessible to all pages, within 12h, after which it expires
    this.cookies.set(STATE_NAME_COOKIE, toSaveState, {path: '/', maxAge: 43200});

    if (this.loggingEnabled)
      log(currentScriptName, "Saved state to cookies.");
  }

  loadStateOrDefault(component, defaultStateValue = new AppState({})) {
    const cookies_local_state = this.cookies.get(STATE_NAME_COOKIE);

    if (this.loggingEnabled)
      log(currentScriptName, "Cookies local state:", cookies_local_state);

    if (cookies_local_state === undefined)
      this.saveStateToCookies(defaultStateValue);

    const newState = cookies_local_state || defaultStateValue;

    if (component.state === undefined)
      component.state = newState;
    else
      component.setState(newState);

    if (this.loggingEnabled)
      log(currentScriptName, "Loaded state from cookies:", newState);

    return component.state;
  }

  eraseCookies() {
    this.cookies.remove(STATE_NAME_COOKIE);
    if (this.loggingEnabled)
      log(currentScriptName, "Erased cookies");
  }

}

export {CookiesController}
