import React from "react";

const AGE_FIELD_TO_PRETTY_DESCRIPTION = {
  'AGE_18_24': {
    longDescription: "Age between 18 and 24 years",
    shortDescription: "Between 18 and 24",
  },
  'AGE_25_34': {
    longDescription: "Age between 25 and 34 years",
    shortDescription: "Between 25 and 34",
  },
  'AGE_35_44': {
    longDescription: "Age between 35 and 44 years",
    shortDescription: "Between 35 and 44",
  },
  'AGE_45_54': {
    longDescription: "Age between 45 and 54 years",
    shortDescription: "Between 45 and 54",
  },
  'AGE_55_64': {
    longDescription: "Age between 55 and 64 years",
    shortDescription: "Between 55 and 64",
  },
  'AGE_65_+': {
    longDescription: "Age above 65 years",
    shortDescription: "Above 65 years",
  },
};

const SEX_FIELD_TO_PRETTY_DESCRIPTION = {
  'SEX_M': {
    longDescription: "Male",
    shortDescription: "Male",
  },
  'SEX_W': {
    longDescription: "Female",
    shortDescription: "Female",
  },
};

const LANGUAGE_FIELD_TO_PRETTY_DESCRIPTION = {
  'LANGUAGE_ENGLISH': {
    longDescription: "English",
    shortDescription: "English",
    icon: <i className={`flag-icon flag-icon-us`}/>
  },
  'LANGUAGE_ITALIAN': {
    longDescription: "Italian",
    shortDescription: "Italian",
    icon: <i className={`flag-icon flag-icon-it`}/>
  },
  'LANGUAGE_FRENCH': {
    longDescription: "French",
    shortDescription: "French",
    icon: <i className={`flag-icon flag-icon-fr`}/>
  },
  'LANGUAGE_GERMAN': {
    longDescription: "German",
    shortDescription: "German",
    icon: <i className={`flag-icon flag-icon-de`}/>
  },
}

const DIFFICULTY_FIELD_TO_PRETTY_DESCRIPTION = {
  0: {
    longDescription: "Impossible",
    shortDescription: "Impossible",
  },
  1: {
    longDescription: "Very difficult",
    shortDescription: "Very difficult",
  },
  2: {
    longDescription: "Difficult",
    shortDescription: "Difficult",
  },
  3: {
    longDescription: "Slightly difficult",
    shortDescription: "Slightly difficult",
  },
  4: {
    longDescription: "Easy",
    shortDescription: "Easy",
  },
};

const SHIFT_FIELD_TO_PRETTY_DESCRIPTION = {
  'PREVIOUS': {
    longDescription: "Previous",
    shortDescription: "Previous",
  },
  'NEXT': {
    longDescription: "Next",
    shortDescription: "Next",
  },
};

const FUN_FIELD_TO_PRETTY_DESCRIPTION = {
  'FUNNY': {
    longDescription: "Was funny",
    shortDescription: "Funny",
  },
  'INDIFFERENT': {
    longDescription: "Was indifferent",
    shortDescription: "Indifferent",
  },
  'NOT_FUNNY': {
    longDescription: "Was not funny",
    shortDescription: "Not funny",
  },
}

export {
  AGE_FIELD_TO_PRETTY_DESCRIPTION,
  SEX_FIELD_TO_PRETTY_DESCRIPTION,
  LANGUAGE_FIELD_TO_PRETTY_DESCRIPTION,
  SHIFT_FIELD_TO_PRETTY_DESCRIPTION,
  DIFFICULTY_FIELD_TO_PRETTY_DESCRIPTION,
  FUN_FIELD_TO_PRETTY_DESCRIPTION,
};
