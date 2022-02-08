import {OBJECT_REFERENCE_ID_FIELD_NAME} from "./ModelUtils";

// const currentScriptName = "ExerciseFieldNamesDictionaryToDescription.js";

const STRATEGY_ID_FIELD_NAME = '_id'
const STRATEGY_NAME_FIELD_NAME = 'name'
const STRATEGY_DESCRIPTION_FIELD_NAME = 'description'

/** Dictionary of data field names to their data handlers */
const STRATEGY_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION = {
  [STRATEGY_ID_FIELD_NAME]: {
    keyPrettyNameShort: "ID",
    keyPrettyNameLong: "Strategy ID",
    valuePrettifier: (value, _shortDescription = false) => value[OBJECT_REFERENCE_ID_FIELD_NAME],
  },
  [STRATEGY_NAME_FIELD_NAME]: {
    keyPrettyNameShort: "Name",
    keyPrettyNameLong: "Name",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
  [STRATEGY_DESCRIPTION_FIELD_NAME]: {
    keyPrettyNameShort: "Desc.",
    keyPrettyNameLong: "Description",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
};

/** Utility function to get a mapping from ID to the pretty version of the object */
function allStrategiesIDsToDescription(allStrategies) {
  const tempMapping = {}
  allStrategies.forEach(strategy => {
    tempMapping[strategy[STRATEGY_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]] =
      strategy[STRATEGY_NAME_FIELD_NAME] || strategy[STRATEGY_DESCRIPTION_FIELD_NAME]
  })
  return tempMapping
}


export {
  STRATEGY_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  STRATEGY_ID_FIELD_NAME,
  STRATEGY_NAME_FIELD_NAME,
  STRATEGY_DESCRIPTION_FIELD_NAME,
  allStrategiesIDsToDescription
}
