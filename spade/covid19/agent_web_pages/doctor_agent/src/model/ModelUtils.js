// const currentScriptName = "ModelUtils.js";

const OBJECT_REFERENCE_ID_FIELD_NAME = '$oid'

const HOUR_ARTIFICIAL_FIELD_NAME = 'hour'
const WEEKDAY_ARTIFICIAL_FIELD_NAME = 'weekday'
const MONTH_ARTIFICIAL_FIELD_NAME = 'month'
const YEAR_ARTIFICIAL_FIELD_NAME = 'year'

/** An internal function to get correct description from mapping objects, or undefined if description obj undefined */
export function selectDescription(descriptionObj, short = true) {
  if (descriptionObj !== undefined)
    return short ? descriptionObj.shortDescription : descriptionObj.longDescription
  else return undefined
}

export {
  OBJECT_REFERENCE_ID_FIELD_NAME,
  YEAR_ARTIFICIAL_FIELD_NAME,
  MONTH_ARTIFICIAL_FIELD_NAME,
  WEEKDAY_ARTIFICIAL_FIELD_NAME,
  HOUR_ARTIFICIAL_FIELD_NAME,
};
