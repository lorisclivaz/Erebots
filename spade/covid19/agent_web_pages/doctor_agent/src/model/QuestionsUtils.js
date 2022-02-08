import {
  QUESTION_ID_FIELD_NAME,
  QUESTION_NEXT_FIELD_NAME,
  QUESTION_PREVIOUS_FIELD_NAME
} from "./QuestionFieldNamesDictionaryToDescription";
import {OBJECT_REFERENCE_ID_FIELD_NAME} from "./ModelUtils";

/**
 * Utility function to retrieve a question object among all by ID
 * @param allQuestions
 * @param questionID
 * @return {*}
 */
function getQuestionByID(allQuestions, questionID) {
  return allQuestions.find(question => {
    return question[QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME] === questionID
  })
}

/**
 * Utility function to follow the startQuestion next pointer and do some action on each next question
 * @param allQuestions
 * @param startQuestion
 * @param fun
 */
function followNextPointerAndDo(allQuestions, startQuestion, fun) {
  let currentQuestion = startQuestion
  while (currentQuestion[QUESTION_NEXT_FIELD_NAME] !== undefined) {
    const nextQuestionID = currentQuestion[QUESTION_NEXT_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]
    currentQuestion = getQuestionByID(allQuestions, nextQuestionID)
    fun(currentQuestion)
  }
}

/**
 * Returns allQuestions sorted using their next/previous fields
 * @param allQuestions
 * @return {[]}
 */
function sortQuestionObjects(allQuestions) {
  const firstQuestion = allQuestions.find(question => {
    return question[QUESTION_PREVIOUS_FIELD_NAME] === undefined
  })

  const resultQuestions = []
  resultQuestions.push(firstQuestion)

  followNextPointerAndDo(allQuestions, firstQuestion, question => resultQuestions.push(question))

  return resultQuestions
}

/**
 * Utility function to compute the level number of a question.
 * @param allQuestions
 * @param currentQuestionID
 * @return {number} The currentQuestionID level
 */
function computeQuestionLevel(allQuestions, currentQuestionID) {
  let nextCount = 0

  followNextPointerAndDo(allQuestions, getQuestionByID(allQuestions, currentQuestionID), _ => nextCount++)

  return allQuestions.length - nextCount
}

export {sortQuestionObjects, computeQuestionLevel}
