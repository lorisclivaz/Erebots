import {debug, warn} from "./Logging";
import {Alert} from "reactstrap";
import React from "react";

const currentScriptName = "DataLoadingUtils.js";

/** Utility function to create a partial initial state in component constructor */
function createInitialStateFieldsFor(dataFieldName) {
  let obj = {};
  obj[`${dataFieldName}FetchError`] = null;
  obj[`${dataFieldName}Loaded`] = false;
  obj[`${dataFieldName}Data`] = [];
  return obj;
}

/** Utility function to create a whole partial initial state fro loading data, starting from field names */
function createPartialInitialStateFromFields(fieldNameList) {
  let partialInitialState = {};
  fieldNameList.forEach(name => {
    const newFields = createInitialStateFieldsFor(name);
    partialInitialState = {...partialInitialState, ...newFields}
  });
  return partialInitialState;
}

/** Generic function to load data from server and modify accordingly the component state */
function load(
  component,
  dataFieldName,
  loadFunction, loadFunctionParams = {},
  onSuccessCallback = (data) => data
) {
  if (component.state[`${dataFieldName}Loaded`] === false) {
    loadFunction(loadFunctionParams).then(
      (result) => {
        debug(currentScriptName, `loaded '${dataFieldName}' from server:`, result);
        let modifiedState = {};
        modifiedState[`${dataFieldName}Loaded`] = true;
        modifiedState[`${dataFieldName}Data`] = result;
        component.setState(modifiedState);
        onSuccessCallback(result);
      },
      (error) => {
        warn(currentScriptName, `Error from server loading '${dataFieldName}':`, error);
        let modifiedState = {};
        modifiedState[`${dataFieldName}Loaded`] = true;
        modifiedState[`${dataFieldName}FetchError`] = error;
        component.setState(modifiedState);
      }
    )
  }
}

/** A function creating a generic loading component */
function createLoading({pt = 1, position = "center", otherClasses = ""}) {
  return (
    <div className={`animated fadeIn pt-${pt} text-${position} ${otherClasses}`}>
      <img className='spinner' alt="spinner"
           src={require('../assets/img/spinner.gif')}
           style={{height: '25px', paddingBottom: '2px'}}/>
      <span> Loading...</span>
    </div>
  );
}

/** A function creating a component showing an error message */
function errorComponent(errorMessage) {
  return <Alert color="danger">Error: {errorMessage}</Alert>;
}

/** A function to return a component when no data is available to be shown */
function noDataAvailableComponent(customMessage = null) {
  let message;
  if (customMessage) message = customMessage;
  else message = "No data available"
  return (
    <Alert color="secondary" className="text-center">
      <i className="text-center text-muted icon-ban"/> {message}
    </Alert>
  );
}

/** Generic function to show a loading message, if data not already loaded or the component (or an error component)
 * if data has been loaded */
function showLoadingOrRender(
  component,
  waitForDataField,
  renderWithData,
  loadingComponent = createLoading({}),
  errorComponentFunction = (errorMessage) => errorComponent(errorMessage)
) {
  const fetchError = component.state[`${waitForDataField}FetchError`];
  const loaded = component.state[`${waitForDataField}Loaded`];
  const data = component.state[`${waitForDataField}Data`];

  if (fetchError) {
    return errorComponentFunction(fetchError.message)
  } else if (!loaded) {
    return loadingComponent;
  } else {
    return renderWithData(data)
  }
}

export {
  createInitialStateFieldsFor,
  createPartialInitialStateFromFields,
  load,
  createLoading,
  errorComponent,
  noDataAvailableComponent,
  showLoadingOrRender
}
