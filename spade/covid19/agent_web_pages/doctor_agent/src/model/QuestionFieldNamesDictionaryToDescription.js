import {OBJECT_REFERENCE_ID_FIELD_NAME} from "./ModelUtils";

// const currentScriptName = "QuestionFieldNamesDictionaryToDescription.js";

const QUESTION_ID_FIELD_NAME = '_id'
const QUESTION_TEXT_EN_FIELD_NAME = 'text_en'
const QUESTION_TEXT_IT_FIELD_NAME = 'text_it'
const QUESTION_TEXT_FR_FIELD_NAME = 'text_fr'
const QUESTION_TEXT_DE_FIELD_NAME = 'text_de'
const QUESTION_NEXT_FIELD_NAME = 'next'
const QUESTION_PREVIOUS_FIELD_NAME = 'previous'

/** Dictionary of data field names to their data handlers */
const QUESTION_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION = {
  [QUESTION_ID_FIELD_NAME]: {
    keyPrettyNameShort: "ID",
    keyPrettyNameLong: "Question ID",
    valuePrettifier: (value, _shortDescription = false) => value[OBJECT_REFERENCE_ID_FIELD_NAME],
  },
  [QUESTION_TEXT_EN_FIELD_NAME]: {
    keyPrettyNameShort: "English",
    keyPrettyNameLong: "English Text",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
  [QUESTION_TEXT_IT_FIELD_NAME]: {
    keyPrettyNameShort: "Italian",
    keyPrettyNameLong: "Italian Text",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
  [QUESTION_TEXT_FR_FIELD_NAME]: {
    keyPrettyNameShort: "French",
    keyPrettyNameLong: "French Text",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
  [QUESTION_TEXT_DE_FIELD_NAME]: {
    keyPrettyNameShort: "German",
    keyPrettyNameLong: "German Text",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
  [QUESTION_NEXT_FIELD_NAME]: {
    keyPrettyNameShort: "Next",
    keyPrettyNameLong: "Next Question",
    valuePrettifier: (value, _shortDescription = false) => JSON.stringify(value),
  },
  [QUESTION_PREVIOUS_FIELD_NAME]: {
    keyPrettyNameShort: "Previous",
    keyPrettyNameLong: "Previous Question",
    valuePrettifier: (value, _shortDescription = false) => JSON.stringify(value),
  },
};


/** Utility function to get a mapping from ID to the pretty version of the object */
function allQuestionsIDsToDescription(allQuestions) {
  const tempMapping = {}
  allQuestions.forEach(question => {
    tempMapping[question[QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]] = question[QUESTION_TEXT_EN_FIELD_NAME]
  })
  return tempMapping
}

export {
  QUESTION_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  QUESTION_ID_FIELD_NAME,
  QUESTION_TEXT_EN_FIELD_NAME,
  QUESTION_TEXT_IT_FIELD_NAME,
  QUESTION_TEXT_FR_FIELD_NAME,
  QUESTION_TEXT_DE_FIELD_NAME,
  QUESTION_NEXT_FIELD_NAME,
  QUESTION_PREVIOUS_FIELD_NAME,
  allQuestionsIDsToDescription
}
