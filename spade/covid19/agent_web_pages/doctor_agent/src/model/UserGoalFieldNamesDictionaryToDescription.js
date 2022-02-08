import {OBJECT_REFERENCE_ID_FIELD_NAME} from "./ModelUtils";

// const currentScriptName = "UserGoalFieldNamesDictionaryToDescription.js";

const USER_GOAL_ID_FIELD_NAME = '_id'
const USER_GOAL_TEXT_EN_FIELD_NAME = 'text_en'
const USER_GOAL_TEXT_IT_FIELD_NAME = 'text_it'
const USER_GOAL_TEXT_FR_FIELD_NAME = 'text_fr'
const USER_GOAL_TEXT_DE_FIELD_NAME = 'text_de'

/** Dictionary of data field names to their data handlers */
const USER_GOAL_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION = {
  [USER_GOAL_ID_FIELD_NAME]: {
    keyPrettyNameShort: "ID",
    keyPrettyNameLong: "User Goal ID",
    valuePrettifier: (value, _shortDescription = false) => value[OBJECT_REFERENCE_ID_FIELD_NAME],
  },
  [USER_GOAL_TEXT_EN_FIELD_NAME]: {
    keyPrettyNameShort: "English",
    keyPrettyNameLong: "English Description",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
  [USER_GOAL_TEXT_IT_FIELD_NAME]: {
    keyPrettyNameShort: "Italian",
    keyPrettyNameLong: "Italian Description",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
  [USER_GOAL_TEXT_FR_FIELD_NAME]: {
    keyPrettyNameShort: "French",
    keyPrettyNameLong: "French Description",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
  [USER_GOAL_TEXT_DE_FIELD_NAME]: {
    keyPrettyNameShort: "German",
    keyPrettyNameLong: "German Description",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
};

/** Utility function to get a mapping from ID to the pretty version of the object */
function allGoalsIDsToDescription(allGoals) {
  const tempMapping = {}
  allGoals.forEach(goal => {
    tempMapping[goal[USER_GOAL_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]] = goal[USER_GOAL_TEXT_EN_FIELD_NAME]
  })
  return tempMapping
}

export {
  USER_GOAL_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  USER_GOAL_ID_FIELD_NAME,
  USER_GOAL_TEXT_EN_FIELD_NAME,
  USER_GOAL_TEXT_IT_FIELD_NAME,
  USER_GOAL_TEXT_FR_FIELD_NAME,
  USER_GOAL_TEXT_DE_FIELD_NAME,
  allGoalsIDsToDescription
}
