import {
  DONE_EXERCISE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  PROFILE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  SPORT_SESSION_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION
} from "./ProfileFieldNamesDictionaryToHandlers";
import {upperFirstChar} from "../utils/StringUtils";
import {EXERCISE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION} from "./ExerciseFieldNamesDictionaryToDescription";
import {EXERCISE_SET_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION} from "./ExerciseSetFieldNamesDictionaryToDescription";
import {USER_GOAL_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION} from "./UserGoalFieldNamesDictionaryToDescription";
import {EXERCISE_SET_MAPPING_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION} from "./ExerciseSetMappingFieldNamesDictionaryToDescription";
import {QUESTION_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION} from "./QuestionFieldNamesDictionaryToDescription";

/**
 * Returns the correct data handler, given its key
 *
 * If provided, the second parameter will preempt the default order of handler selection
 * (in case of duplicate keys in different data structures)
 *
 * The handler is an object:
 * ```javascript
 * {
 *   keyPrettyNameShort: "...",
 *   keyPrettyNameLong: "...",
 *   rawValuesToDescriptionMap: {...} | undefined,
 *   valuePrettifier: (value) => ...
 * }
 * ```
 *
 * It contains the logic o prettify both the key and the value through the prettifying function
 */
function getKeyHandlerFor(key, specificMapping = null) {
  if (specificMapping && specificMapping[key] !== undefined) {
    return specificMapping[key];
  } else if (PROFILE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION[key] !== undefined) {
    return PROFILE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION[key];
  } else if (SPORT_SESSION_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION[key] !== undefined) {
    return SPORT_SESSION_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION[key];
  } else if (DONE_EXERCISE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION[key] !== undefined) {
    return DONE_EXERCISE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION[key];
  } else if (EXERCISE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION[key] !== undefined) {
    return EXERCISE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION[key];
  } else if (EXERCISE_SET_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION[key] !== undefined) {
    return EXERCISE_SET_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION[key];
  } else if (USER_GOAL_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION[key] !== undefined) {
    return USER_GOAL_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION[key];
  } else if (EXERCISE_SET_MAPPING_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION[key] !== undefined) {
    return EXERCISE_SET_MAPPING_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION[key];
  } else if (QUESTION_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION[key] !== undefined) {
    return QUESTION_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION[key];
  } else {
    // debug(currentScriptName, `'${key}' is not a valid field key. Defaulting to identity handler.`);
    return {keyPrettyNameShort: key, keyPrettyNameLong: key, valuePrettifier: (value) => value} // return the identity handler
  }
}

/** An helper function to prettify a field name, managing even those fields not present in database, making their first letter uppercase */
function prettifyFieldName(fieldName, short = false, specificMapping = null) {
  const keyHandler = getKeyHandlerFor(fieldName, specificMapping);

  let fieldNameString;
  if (short)
    fieldNameString = keyHandler.keyPrettyNameShort;
  else
    fieldNameString = keyHandler.keyPrettyNameLong;

  return upperFirstChar(fieldNameString);
}

export {
  getKeyHandlerFor,
  prettifyFieldName
};
