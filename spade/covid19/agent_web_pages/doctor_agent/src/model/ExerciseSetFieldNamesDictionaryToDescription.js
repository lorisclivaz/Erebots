import {OBJECT_REFERENCE_ID_FIELD_NAME} from "./ModelUtils";

// const currentScriptName = "ExerciseSetFieldNamesDictionaryToDescription.js";

const EXERCISE_SET_ID_FIELD_NAME = '_id'
const EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME = 'exercise_list'
const EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME = 'suitable_for_goals'

/** Dictionary of data field names to their data handlers */
const EXERCISE_SET_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION = {
  [EXERCISE_SET_ID_FIELD_NAME]: {
    keyPrettyNameShort: "ID",
    keyPrettyNameLong: "Exercise Set ID",
    valuePrettifier: (value, _shortDescription = false) => value[OBJECT_REFERENCE_ID_FIELD_NAME],
  },
  [EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME]: {
    keyPrettyNameShort: "Exercise List",
    keyPrettyNameLong: "Exercise List",
    valuePrettifier: (value, _shortDescription = false) => JSON.stringify(value),
  },
  [EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME]: {
    keyPrettyNameShort: "For Goals",
    keyPrettyNameLong: "Suitable For Goals",
    valuePrettifier: (value, _shortDescription = false) => JSON.stringify(value),
  },
};

/** Utility function to get a mapping from ID to the pretty version of the object */
function allExerciseSetsIDsToDescription(allExerciseSets, exerciseIDsToDescription, joiningString = ', ') {
  const tempMapping = {}
  allExerciseSets.forEach(exerciseSet => {
    tempMapping[exerciseSet[EXERCISE_SET_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]] = (
      exerciseSet[EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME].map(oid =>
        exerciseIDsToDescription[oid[OBJECT_REFERENCE_ID_FIELD_NAME]]
      ).join(joiningString)
    )
  })
  return tempMapping
}

export {
  EXERCISE_SET_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  EXERCISE_SET_ID_FIELD_NAME,
  EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME,
  EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME,
  allExerciseSetsIDsToDescription
}
