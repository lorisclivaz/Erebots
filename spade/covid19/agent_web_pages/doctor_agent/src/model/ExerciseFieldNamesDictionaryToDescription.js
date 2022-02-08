import {OBJECT_REFERENCE_ID_FIELD_NAME} from "./ModelUtils";

// const currentScriptName = "ExerciseFieldNamesDictionaryToDescription.js";

const EXERCISE_ID_FIELD_NAME = '_id'
const EXERCISE_TEXT_EN_FIELD_NAME = 'text_en'
const EXERCISE_TEXT_IT_FIELD_NAME = 'text_it'
const EXERCISE_TEXT_FR_FIELD_NAME = 'text_fr'
const EXERCISE_TEXT_DE_FIELD_NAME = 'text_de'
const EXERCISE_LABEL_FIELD_NAME = 'label'
const EXERCISE_GIF_PATH_FIELD_NAME = 'gif_path'

/** Dictionary of data field names to their data handlers */
const EXERCISE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION = {
  [EXERCISE_ID_FIELD_NAME]: {
    keyPrettyNameShort: "ID",
    keyPrettyNameLong: "Exercise ID",
    valuePrettifier: (value, _shortDescription = false) => value[OBJECT_REFERENCE_ID_FIELD_NAME],
  },
  [EXERCISE_TEXT_EN_FIELD_NAME]: {
    keyPrettyNameShort: "English",
    keyPrettyNameLong: "English Description",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
  [EXERCISE_TEXT_IT_FIELD_NAME]: {
    keyPrettyNameShort: "Italian",
    keyPrettyNameLong: "Italian Description",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
  [EXERCISE_TEXT_FR_FIELD_NAME]: {
    keyPrettyNameShort: "French",
    keyPrettyNameLong: "French Description",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
  [EXERCISE_TEXT_DE_FIELD_NAME]: {
    keyPrettyNameShort: "German",
    keyPrettyNameLong: "German Description",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
  [EXERCISE_LABEL_FIELD_NAME]: {
    keyPrettyNameShort: "Label",
    keyPrettyNameLong: "Mnemonic Label",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
  [EXERCISE_GIF_PATH_FIELD_NAME]: {
    keyPrettyNameShort: "GIF",
    keyPrettyNameLong: "GIF Image",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
};

/** Utility function to get a mapping from ID to the pretty version of the object */
function allExercisesIDsToDescription(allExercises) {
  const tempMapping = {}
  allExercises.forEach(exercise => {
    tempMapping[exercise[EXERCISE_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]] =
      exercise[EXERCISE_LABEL_FIELD_NAME] || exercise[EXERCISE_TEXT_EN_FIELD_NAME]
  })
  return tempMapping
}


export {
  EXERCISE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  EXERCISE_ID_FIELD_NAME,
  EXERCISE_TEXT_EN_FIELD_NAME,
  EXERCISE_TEXT_IT_FIELD_NAME,
  EXERCISE_TEXT_FR_FIELD_NAME,
  EXERCISE_TEXT_DE_FIELD_NAME,
  EXERCISE_LABEL_FIELD_NAME,
  EXERCISE_GIF_PATH_FIELD_NAME,
  allExercisesIDsToDescription
}
