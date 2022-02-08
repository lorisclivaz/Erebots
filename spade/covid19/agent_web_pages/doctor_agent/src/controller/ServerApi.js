import {debug, log} from "../utils/Logging";
import {WebUserModel} from '../model/WebUserModel'

//const HOSTNAME = "vlhaislab-covidphysio.hevs.ch";
const HOSTNAME = "localhost";
const PORT = "10000";
const SERVER_API_VERSION = "v1";

const SERVER_API_ADDRESS = `http://${HOSTNAME}:${PORT}/api/${SERVER_API_VERSION}`;
// const SERVER_API_ADDRESS = `https://${HOSTNAME}/api/${SERVER_API_VERSION}`;


const SERVER_USER_ENDPOINT = "/user";
const SERVER_USER_COUNT_ENDPOINT = "/user/count";
const SERVER_USER_GOAL_ENDPOINT = "/user_goal";
const SERVER_USER_GOAL_COUNT_ENDPOINT = "/user_goal/count";
const SERVER_QUESTION_ENDPOINT = "/question";
const SERVER_QUESTION_COUNT_ENDPOINT = "/question/count";
const SERVER_EXERCISE_ENDPOINT = "/exercise";
const SERVER_EXERCISE_COUNT_ENDPOINT = "/exercise/count";
const SERVER_EXERCISE_SET_ENDPOINT = "/exercise_set";
const SERVER_EXERCISE_SET_COUNT_ENDPOINT = "/exercise_set/count";
const SERVER_EXERCISE_MAPPING_ENDPOINT = "/question_to_exercise_sets_mapping";
const SERVER_EXERCISE_MAPPING_COUNT_ENDPOINT = "/question_to_exercise_sets_mapping/count";

const SERVER_STRATEGY_ENDPOINT = "/strategy";
const SERVER_STRATEGY_COUNT_ENDPOINT = "/strategy/count";

const ACTION_CREATE = "CREATE"
const ACTION_MODIFY = "MODIFY"
const ACTION_DELETE = "DELETE"

const AGGREGATE_BY_PROFILE_DIM_1_FIELD_QUERY_PARAMETER = "aggregateByDimension1";
const AGGREGATE_BY_PROFILE_DIM_2_FIELD_QUERY_PARAMETER = "aggregateByDimension2";

const TIME_WINDOW_START = "from_date";
const TIME_WINDOW_END = "to_date";

const PAGINATION_PAGE_START = "start";
const PAGINATION_PAGE_END = "end";

const currentScriptName = "ServerApi.js";

/** Javascript implementation to make current computation wait some time */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/** Logs in the user with provided username and password, returning its user object */
async function logIn(username, password) {

  // TODO NOT NOW 30/03/2020: add code connecting to the server and know if the user is authenticated
  await sleep(1000);

  if (username === "imdavide" && password === "xNA#6V$Eh%gZv2Pw!p2k43Eeu$XQ8&$N") {
    log(currentScriptName, "User logged in");
    return new WebUserModel({name: "imdavide", surname: "", email: "name.surname@localhost.com", role: "Doctor"})
  } else if (password === "Cov19id!@PrjDoctorPsw") {
    log(currentScriptName, "Jolly User logged in");
    return new WebUserModel({name: username, surname: "", email: `${username}@localhost.com`, role: "Doctor"})
  } else {
    return undefined;
  }
}

async function logOut() {
  log(currentScriptName, "User logged out");
}

/** Fetches data from the server; it returns the promise of the data */
async function getAll({
                        serverEndPoint,
                        aggregateByDimension1 = null,
                        aggregateByDimension2 = null,
                        start = null,
                        end = null
                      }) {
  let toFetchEndpoint = `${SERVER_API_ADDRESS}${serverEndPoint}?`;
  toFetchEndpoint = attachProfileDimensionsParams(toFetchEndpoint, aggregateByDimension1, aggregateByDimension2)
  toFetchEndpoint = attachPaginationParams(toFetchEndpoint, start, end);
  debug(currentScriptName, `Fetching '${toFetchEndpoint}'`);
  return fetch(toFetchEndpoint).then(res => res.json())
}

/** Fetches data with provided ID; it returns the promise of the retrieved data */
async function getSingle({serverEndPoint, id}) {
  const toFetchEndpoint = `${SERVER_API_ADDRESS}${serverEndPoint}/${id}`;
  debug(currentScriptName, `Fetching '${toFetchEndpoint}'`);
  return fetch(toFetchEndpoint).then(res => res.json())
}

/** Fetches the number of objects from server */
async function getObjectCount({serverEndPoint}) {
  const toFetchEndpoint = `${SERVER_API_ADDRESS}${serverEndPoint}`;
  debug(currentScriptName, `Fetching '${toFetchEndpoint}'`);
  return fetch(toFetchEndpoint).then(res => res.json())
}

/** Method to create, modify or delete an object depending on the specified ACTION */
async function postObject(action, serverEndPoint, {id = null, formDataObject = null}) {
  let toFetchEndpoint = `${SERVER_API_ADDRESS}${serverEndPoint}`;
  let payload = {}
  if (action === ACTION_CREATE) {
    payload['method'] = 'POST'
    payload['body'] = formDataObject
  } else if (action === ACTION_MODIFY) {
    toFetchEndpoint = `${toFetchEndpoint}/${id}`
    payload['method'] = 'POST'
    payload['body'] = formDataObject
  } else if (action === ACTION_DELETE) {
    toFetchEndpoint = `${toFetchEndpoint}/${id}/delete`
    payload['method'] = 'POST'
  }
  debug(currentScriptName, `Action: ${action}, calling '${toFetchEndpoint}'`);
  return fetch(toFetchEndpoint, payload).then(res => res.json())
}

/** Fetches data with provided ID; it returns the promise of the retrieved data */
async function getUserLevelHistory({id, from_date = null, to_date = null}) {
  let toFetchEndpoint = `${SERVER_API_ADDRESS}${SERVER_USER_ENDPOINT}/${id}/level_history?`;
  toFetchEndpoint = attachTimeWindowParams(toFetchEndpoint, from_date, to_date)
  debug(currentScriptName, `Fetching '${toFetchEndpoint}'`);
  return fetch(toFetchEndpoint).then(res => res.json())
}

/** Internal utility function to attach to provided base url parameters for profile dimensions 1 and 2 */
function attachProfileDimensionsParams(baseUrl, aggregateByDimension1 = null, aggregateByDimension2 = null) {
  if (aggregateByDimension1 !== null) baseUrl = `${baseUrl}&${AGGREGATE_BY_PROFILE_DIM_1_FIELD_QUERY_PARAMETER}=${aggregateByDimension1}`;
  if (aggregateByDimension2 !== null) baseUrl = `${baseUrl}&${AGGREGATE_BY_PROFILE_DIM_2_FIELD_QUERY_PARAMETER}=${aggregateByDimension2}`;
  return baseUrl;
}

/** Internal utility function to attach to provided base url parameters for time window start and end */
function attachTimeWindowParams(baseUrl, timeWindowStart = null, timeWindowEnd = null) {
  if (timeWindowStart !== null) baseUrl = `${baseUrl}&${TIME_WINDOW_START}=${timeWindowStart}`;
  if (timeWindowEnd !== null) baseUrl = `${baseUrl}&${TIME_WINDOW_END}=${timeWindowEnd}`;
  return baseUrl;
}

/** Internal utility function to attach to provided base url parameters for pagination start and end */
function attachPaginationParams(baseUrl, paginationStart = null, paginationEnd = null) {
  if (paginationStart !== null) baseUrl = `${baseUrl}&${PAGINATION_PAGE_START}=${paginationStart}`;
  if (paginationEnd !== null) baseUrl = `${baseUrl}&${PAGINATION_PAGE_END}=${paginationEnd}`;
  return baseUrl;
}

export {
  SERVER_API_ADDRESS,
  SERVER_USER_ENDPOINT,
  SERVER_USER_COUNT_ENDPOINT,
  SERVER_USER_GOAL_ENDPOINT,
  SERVER_USER_GOAL_COUNT_ENDPOINT,
  SERVER_QUESTION_ENDPOINT,
  SERVER_QUESTION_COUNT_ENDPOINT,
  SERVER_EXERCISE_ENDPOINT,
  SERVER_EXERCISE_COUNT_ENDPOINT,
  SERVER_EXERCISE_SET_ENDPOINT,
  SERVER_EXERCISE_SET_COUNT_ENDPOINT,
  SERVER_EXERCISE_MAPPING_ENDPOINT,
  SERVER_EXERCISE_MAPPING_COUNT_ENDPOINT,
  SERVER_STRATEGY_ENDPOINT,
  SERVER_STRATEGY_COUNT_ENDPOINT,
  logIn,
  logOut,
  getAll,
  getSingle,
  getObjectCount,
  getUserLevelHistory,
  ACTION_CREATE,
  ACTION_MODIFY,
  ACTION_DELETE,
  postObject,
  AGGREGATE_BY_PROFILE_DIM_1_FIELD_QUERY_PARAMETER,
  AGGREGATE_BY_PROFILE_DIM_2_FIELD_QUERY_PARAMETER,
  TIME_WINDOW_START,
  TIME_WINDOW_END,
  PAGINATION_PAGE_START,
  PAGINATION_PAGE_END,
}
