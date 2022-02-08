import React from "react";
import {
  AGE_FIELD_TO_PRETTY_DESCRIPTION,
  DIFFICULTY_FIELD_TO_PRETTY_DESCRIPTION,
  FUN_FIELD_TO_PRETTY_DESCRIPTION,
  LANGUAGE_FIELD_TO_PRETTY_DESCRIPTION,
  SEX_FIELD_TO_PRETTY_DESCRIPTION
} from "./FieldValuesDictionaryToDescription";
import {checkDatetimeValue, extractDateObject} from "./DatetimeExtractor";
import {dateToPrettyString} from "../utils/DateUtils";
import {OBJECT_REFERENCE_ID_FIELD_NAME, selectDescription} from "./ModelUtils";

// const currentScriptName = "ProfileFieldNamesDictionaryToHandlers.js";

const USER_ID_FIELD_NAME = '_id'
const USER_FIRST_NAME_FIELD_NAME = 'first_name'
const USER_LAST_NAME_FIELD_NAME = 'last_name'
const USER_LANGUAGE_FIELD_NAME = 'language'
const USER_AGE_FIELD_NAME = 'age'
const USER_SEX_FIELD_NAME = 'sex'
const USER_LAST_INTERACTION_FIELD_NAME = 'last_interaction'
const USER_FAVOURITE_SPORT_DAYS_FIELD_NAME = 'favourite_sport_days'
const USER_GOAL_IDS_FIELD_NAME = 'goals'
const USER_REGISTRATION_COMPLETED_FIELD_NAME = 'registration_completed'
const USER_TELEGRAM_ID_FIELD_NAME = 'telegram_id'
const USER_CURRENT_QUESTION_ID_FIELD_NAME = 'current_question'
const USER_CURRENT_QUESTION_ANSWER_FIELD_NAME = 'current_question_answer'
const USER_SPORT_SESSIONS_ARRAY_FIELD_NAME = 'sport_sessions'

const SPORT_SESSION_EXERCISE_SET_ID_FIELD_NAME = 'exercise_set'
const SPORT_SESSION_STARTED_AT_FIELD_NAME = 'started_at'
const SPORT_SESSION_ENDED_AT_FIELD_NAME = 'ended_at'
const SPORT_SESSION_ABORTED_FIELD_NAME = 'aborted'
const SPORT_SESSION_FUN_RATING_FIELD_NAME = 'fun_rating'
const SPORT_SESSION_DONE_EXERCISES_ARRAY_FIELD_NAME = 'done_exercises_ordered'

const DONE_EXERCISE_EXERCISE_ID_FIELD_NAME = 'exercise'
const DONE_EXERCISE_ENDED_AT_FIELD_NAME = 'ended_at'
const DONE_EXERCISE_DIFFICULTY_RATING_FIELD_NAME = 'difficulty_rating'

const PROFILE_AVAILABLE_AGGREGATION_FIELDS = [
  USER_LANGUAGE_FIELD_NAME, USER_AGE_FIELD_NAME, USER_SEX_FIELD_NAME, USER_CURRENT_QUESTION_ID_FIELD_NAME,
  USER_CURRENT_QUESTION_ANSWER_FIELD_NAME
];

/** Dictionary of data field names to their data handlers */
const PROFILE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION = {
  [USER_ID_FIELD_NAME]: {
    keyPrettyNameShort: "ID",
    keyPrettyNameLong: "User ID",
    valuePrettifier: (value, _shortDescription = false) => {
      value = _parseOrSame(value)
      return value[OBJECT_REFERENCE_ID_FIELD_NAME]
    },
  },
  [USER_FIRST_NAME_FIELD_NAME]: {
    keyPrettyNameShort: "Name",
    keyPrettyNameLong: "First Name",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
  [USER_LAST_NAME_FIELD_NAME]: {
    keyPrettyNameShort: "Surname",
    keyPrettyNameLong: "Last Name",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
  [USER_LANGUAGE_FIELD_NAME]: {
    keyPrettyNameShort: "Language",
    keyPrettyNameLong: "Language",
    valuePrettifier: (value, shortDescription = false, iconify = true) => {
      if (value === undefined) return undefined;
      else if (iconify) return LANGUAGE_FIELD_TO_PRETTY_DESCRIPTION[value].icon;
      else return selectDescription(LANGUAGE_FIELD_TO_PRETTY_DESCRIPTION[value], shortDescription)
    },
  },
  [USER_AGE_FIELD_NAME]: {
    keyPrettyNameShort: "Age",
    keyPrettyNameLong: "Age",
    rawValuesToDescriptionMap: AGE_FIELD_TO_PRETTY_DESCRIPTION,
    valuePrettifier: (value, shortDescription = false) =>
      selectDescription(AGE_FIELD_TO_PRETTY_DESCRIPTION[value], shortDescription),
  },
  [USER_SEX_FIELD_NAME]: {
    keyPrettyNameShort: "Sex",
    keyPrettyNameLong: "Sex",
    rawValuesToDescriptionMap: SEX_FIELD_TO_PRETTY_DESCRIPTION,
    valuePrettifier: (value, shortDescription = false, iconify = true) => {
      if (value === undefined) return undefined;
      else if (iconify) return <i className={`fa fa-${value === 'SEX_M' ? 'mars' : 'venus'}`}/>;
      else return selectDescription(SEX_FIELD_TO_PRETTY_DESCRIPTION[value], shortDescription)
    },
  },
  [USER_LAST_INTERACTION_FIELD_NAME]: {
    keyPrettyNameShort: "Last interaction",
    keyPrettyNameLong: "Last user interaction",
    valuePrettifier: (value, _shortDescription = false) => _prettifyDateOrReturnValue(value),
  },
  [USER_FAVOURITE_SPORT_DAYS_FIELD_NAME]: {
    keyPrettyNameShort: "Sport Days",
    keyPrettyNameLong: "Favourite Sport Days",
    valuePrettifier: (value, _shortDescription = false) => {
      const sportDaysArray = _parseOrSame(value)
      return sportDaysArray === undefined || sportDaysArray.length === 0 || !Array.isArray(sportDaysArray)
        ? "No days"
        : sportDaysArray.join(', ')
    }
  },
  [USER_GOAL_IDS_FIELD_NAME]: {
    keyPrettyNameShort: "Goals",
    keyPrettyNameLong: "Goals",
    valuePrettifier: (value, _shortDescription = false) => {
      const goalIDsArray = _parseOrSame(value)
      return goalIDsArray === undefined || !Array.isArray(goalIDsArray)
        ? "No goals"
        : `${goalIDsArray.length} goals`
    }

  },
  [USER_REGISTRATION_COMPLETED_FIELD_NAME]: {
    keyPrettyNameShort: "Registration completed",
    keyPrettyNameLong: "Registration completed",
    valuePrettifier: (value, _shortDescription = false) => value !== undefined ? value : false,
  },
  [USER_TELEGRAM_ID_FIELD_NAME]: {
    keyPrettyNameShort: "Telegram ID",
    keyPrettyNameLong: "Telegram ID",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
  [USER_CURRENT_QUESTION_ID_FIELD_NAME]: {
    keyPrettyNameShort: "Question",
    keyPrettyNameLong: "Current Question",
    valuePrettifier: (value, _shortDescription = false) => {
      value = _parseOrSame(value)
      return value[OBJECT_REFERENCE_ID_FIELD_NAME]
    },
  },
  [USER_CURRENT_QUESTION_ANSWER_FIELD_NAME]: {
    keyPrettyNameShort: "Answer",
    keyPrettyNameLong: "Current Question Answer",
    rawValuesToDescriptionMap: DIFFICULTY_FIELD_TO_PRETTY_DESCRIPTION,
    valuePrettifier: (value, shortDescription = false) =>
      selectDescription(DIFFICULTY_FIELD_TO_PRETTY_DESCRIPTION[value], shortDescription),
  },
  [USER_SPORT_SESSIONS_ARRAY_FIELD_NAME]: {
    keyPrettyNameShort: "Sessions",
    keyPrettyNameLong: "Sport Sessions",
    valuePrettifier: (value, shortDescription = false) => {
      value = _parseOrSame(value)
      return value === undefined || !Array.isArray(value)
        ? shortDescription
          ? "No sessions"
          : "No sport sessions"
        : shortDescription
          ? `${value.length} sessions`
          : `${value.length} sport sessions`
    }
  }
};

/** Dictionary of data field names to their data handlers */
const SPORT_SESSION_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION = {
  [SPORT_SESSION_EXERCISE_SET_ID_FIELD_NAME]: {
    keyPrettyNameShort: "Set",
    keyPrettyNameLong: "Exercise Set",
    valuePrettifier: (value, _shortDescription = false) => {
      value = _parseOrSame(value)
      return value[OBJECT_REFERENCE_ID_FIELD_NAME]
    },
  },
  [SPORT_SESSION_STARTED_AT_FIELD_NAME]: {
    keyPrettyNameShort: "Started",
    keyPrettyNameLong: "Started At",
    valuePrettifier: (value, _shortDescription = false) => _prettifyDateOrReturnValue(value),
  },
  [SPORT_SESSION_ENDED_AT_FIELD_NAME]: {
    keyPrettyNameShort: "Ended",
    keyPrettyNameLong: "Ended At",
    valuePrettifier: (value, _shortDescription = false) => _prettifyDateOrReturnValue(value),
  },
  [SPORT_SESSION_ABORTED_FIELD_NAME]: {
    keyPrettyNameShort: "Aborted",
    keyPrettyNameLong: "Session was aborted",
    valuePrettifier: (value, _shortDescription = false) => value,
  },
  [SPORT_SESSION_FUN_RATING_FIELD_NAME]: {
    keyPrettyNameShort: "Fun",
    keyPrettyNameLong: "Fun Rating",
    rawValuesToDescriptionMap: FUN_FIELD_TO_PRETTY_DESCRIPTION,
    valuePrettifier: (value, shortDescription = false) =>
      selectDescription(FUN_FIELD_TO_PRETTY_DESCRIPTION[value], shortDescription),
  },
  [SPORT_SESSION_DONE_EXERCISES_ARRAY_FIELD_NAME]: {
    keyPrettyNameShort: "Exercises",
    keyPrettyNameLong: "Done exercises",
    valuePrettifier: (value, shortDescription = false) => {
      value = _parseOrSame(value)
      return value === undefined
        ? shortDescription
          ? "No exercises"
          : "No exercises done"
        : shortDescription
          ? `${value.length} done`
          : `${value.length} exercises done`
    }
  }
}

/** Dictionary of data field names to their data handlers */
const DONE_EXERCISE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION = {
  [DONE_EXERCISE_EXERCISE_ID_FIELD_NAME]: {
    keyPrettyNameShort: "Exercise",
    keyPrettyNameLong: "Exercise",
    valuePrettifier: (value, _shortDescription = false) => {
      value = _parseOrSame(value)
      return value[OBJECT_REFERENCE_ID_FIELD_NAME]
    },
  },
  [DONE_EXERCISE_ENDED_AT_FIELD_NAME]: {
    keyPrettyNameShort: "Ended",
    keyPrettyNameLong: "Ended At",
    valuePrettifier: (value, _shortDescription = false) => _prettifyDateOrReturnValue(value),
  },
  [DONE_EXERCISE_DIFFICULTY_RATING_FIELD_NAME]: {
    keyPrettyNameShort: "Difficulty",
    keyPrettyNameLong: "Difficulty Rating",
    rawValuesToDescriptionMap: DIFFICULTY_FIELD_TO_PRETTY_DESCRIPTION,
    valuePrettifier: (value, shortDescription = false) =>
      selectDescription(DIFFICULTY_FIELD_TO_PRETTY_DESCRIPTION[value], shortDescription),
  },
}

/** An internal function to prettify the datetime field, or return the given value if not a date field */
function _prettifyDateOrReturnValue(value) {
  if (checkDatetimeValue(value))
    return dateToPrettyString(extractDateObject(value));
  else
    return value
}

/** An internal function to transform a string to an object */
function _parseOrSame(value) {
  if (typeof value === "string") {
    try {
      return JSON.parse(value.replaceAll('\'', '"'))
    } catch (e) {
    }
  }
  return value
}

export {
  PROFILE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  PROFILE_AVAILABLE_AGGREGATION_FIELDS,
  USER_ID_FIELD_NAME,
  USER_FIRST_NAME_FIELD_NAME,
  USER_LAST_NAME_FIELD_NAME,
  USER_LANGUAGE_FIELD_NAME,
  USER_AGE_FIELD_NAME,
  USER_SEX_FIELD_NAME,
  USER_LAST_INTERACTION_FIELD_NAME,
  USER_FAVOURITE_SPORT_DAYS_FIELD_NAME,
  USER_GOAL_IDS_FIELD_NAME,
  USER_REGISTRATION_COMPLETED_FIELD_NAME,
  USER_TELEGRAM_ID_FIELD_NAME,
  USER_CURRENT_QUESTION_ID_FIELD_NAME,
  USER_CURRENT_QUESTION_ANSWER_FIELD_NAME,
  USER_SPORT_SESSIONS_ARRAY_FIELD_NAME,
  SPORT_SESSION_EXERCISE_SET_ID_FIELD_NAME,
  SPORT_SESSION_STARTED_AT_FIELD_NAME,
  SPORT_SESSION_ENDED_AT_FIELD_NAME,
  SPORT_SESSION_ABORTED_FIELD_NAME,
  SPORT_SESSION_FUN_RATING_FIELD_NAME,
  SPORT_SESSION_DONE_EXERCISES_ARRAY_FIELD_NAME,
  DONE_EXERCISE_EXERCISE_ID_FIELD_NAME,
  DONE_EXERCISE_ENDED_AT_FIELD_NAME,
  DONE_EXERCISE_DIFFICULTY_RATING_FIELD_NAME,
  SPORT_SESSION_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  DONE_EXERCISE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
}
