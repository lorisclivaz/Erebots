import React from "react";

import {OBJECT_REFERENCE_ID_FIELD_NAME, selectDescription} from "./ModelUtils";
import {
  DIFFICULTY_FIELD_TO_PRETTY_DESCRIPTION,
  SHIFT_FIELD_TO_PRETTY_DESCRIPTION
} from "./FieldValuesDictionaryToDescription";

// const currentScriptName = "ExerciseSetMappingFieldNamesDictionaryToDescription.js";

const EXERCISE_SET_MAPPING_ID_FIELD_NAME = '_id'
const EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME = 'suitable_exercise_sets'
const EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME = 'asked_question'
const EXERCISE_SET_MAPPING_QUESTION_ANSWER_FIELD_NAME = 'user_answer'
const EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME = 'question_shift'

/** Dictionary of data field names to their data handlers */
const EXERCISE_SET_MAPPING_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION = {
  [EXERCISE_SET_MAPPING_ID_FIELD_NAME]: {
    keyPrettyNameShort: "ID",
    keyPrettyNameLong: "Exercise Set Mapping ID",
    valuePrettifier: (value, _shortDescription = false) => value[OBJECT_REFERENCE_ID_FIELD_NAME],
  },
  [EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME]: {
    keyPrettyNameShort: "Question",
    keyPrettyNameLong: "Question",
    valuePrettifier: (value, _shortDescription = false) => JSON.stringify(value),
  },
  [EXERCISE_SET_MAPPING_QUESTION_ANSWER_FIELD_NAME]: {
    keyPrettyNameShort: "Answer",
    keyPrettyNameLong: "Question answer",
    rawValuesToDescriptionMap: DIFFICULTY_FIELD_TO_PRETTY_DESCRIPTION,
    valuePrettifier: (value, shortDescription = false) =>
      selectDescription(DIFFICULTY_FIELD_TO_PRETTY_DESCRIPTION[value], shortDescription),
  },
  [EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME]: {
    keyPrettyNameShort: "Exercise Sets",
    keyPrettyNameLong: "Suitable Exercise Sets",
    valuePrettifier: (value, _shortDescription = false) => JSON.stringify(value),
  },
  [EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME]: {
    keyPrettyNameShort: "Shift",
    keyPrettyNameLong: "Question shift",
    rawValuesToDescriptionMap: SHIFT_FIELD_TO_PRETTY_DESCRIPTION,
    valuePrettifier: (value, shortDescription = false) => {
      const description = selectDescription(SHIFT_FIELD_TO_PRETTY_DESCRIPTION[value], shortDescription)
      return description === undefined
        ? <span><i className="text-muted icon-ban"/></span>
        : description
    },
  },
};

export {
  EXERCISE_SET_MAPPING_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  EXERCISE_SET_MAPPING_ID_FIELD_NAME,
  EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME,
  EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME,
  EXERCISE_SET_MAPPING_QUESTION_ANSWER_FIELD_NAME,
  EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME,
}
