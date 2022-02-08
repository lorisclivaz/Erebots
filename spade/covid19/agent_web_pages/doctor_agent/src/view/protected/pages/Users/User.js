import React, {Component} from 'react';
import {Card, CardBody, CardHeader, Col, Row, Table} from 'reactstrap';
import {
  getAll,
  getSingle,
  getUserLevelHistory,
  SERVER_EXERCISE_ENDPOINT,
  SERVER_QUESTION_ENDPOINT,
  SERVER_USER_ENDPOINT,
  SERVER_USER_GOAL_ENDPOINT
} from "../../../../controller/ServerApi";
import {
  createLoading,
  createPartialInitialStateFromFields,
  load,
  noDataAvailableComponent,
  showLoadingOrRender
} from "../../../../utils/DataLoadingUtils";
import {
  DONE_EXERCISE_EXERCISE_ID_FIELD_NAME,
  SPORT_SESSION_ABORTED_FIELD_NAME,
  SPORT_SESSION_DONE_EXERCISES_ARRAY_FIELD_NAME,
  SPORT_SESSION_ENDED_AT_FIELD_NAME,
  SPORT_SESSION_FUN_RATING_FIELD_NAME,
  SPORT_SESSION_STARTED_AT_FIELD_NAME,
  USER_AGE_FIELD_NAME,
  USER_CURRENT_QUESTION_ANSWER_FIELD_NAME,
  USER_CURRENT_QUESTION_ID_FIELD_NAME,
  USER_FAVOURITE_SPORT_DAYS_FIELD_NAME,
  USER_FIRST_NAME_FIELD_NAME,
  USER_GOAL_IDS_FIELD_NAME,
  USER_ID_FIELD_NAME,
  USER_LANGUAGE_FIELD_NAME,
  USER_LAST_INTERACTION_FIELD_NAME,
  USER_SEX_FIELD_NAME,
  USER_SPORT_SESSIONS_ARRAY_FIELD_NAME
} from "../../../../model/ProfileFieldNamesDictionaryToHandlers";
import {OBJECT_REFERENCE_ID_FIELD_NAME} from "../../../../model/ModelUtils";
import {getKeyHandlerFor, prettifyFieldName} from "../../../../model/FieldPrettifyHandler";
import {allGoalsIDsToDescription} from "../../../../model/UserGoalFieldNamesDictionaryToDescription";
import {allQuestionsIDsToDescription} from "../../../../model/QuestionFieldNamesDictionaryToDescription";
import {computeQuestionLevel} from "../../../../model/QuestionsUtils";
import DataTable from "react-data-table-component";
import {convertToUTCMillis, DATE_OBJECT_FIELD_NAME, extractDateObject} from "../../../../model/DatetimeExtractor";
import Badge from "reactstrap/es/Badge";
import {millisToDurationString} from "../../../../utils/TimeDurationUtils";
import {allExercisesIDsToDescription} from "../../../../model/ExerciseFieldNamesDictionaryToDescription";
import './User.css'
import {
  CardEventChartWithOptions,
  EVENT_CHART_TIME_WINDOW_LAST_WEEK,
  EVENT_CHART_TYPE_LINE
} from "../../components/charts/CardEventChartWithOptions";

// const currentScriptName = "User.js";

/** Function to compute sport session status */
const computeSportSessionStatus = sportSession =>
  sportSession[SPORT_SESSION_ABORTED_FIELD_NAME] === true
    ? 'Aborted'
    : sportSession[SPORT_SESSION_ENDED_AT_FIELD_NAME] !== undefined ? 'Completed' : 'Pending'

/** Function to get color badge from user sport session status */
const getBadgeColorFromStatus = status => {
  return status === 'Completed' ? 'success' :
    status === 'Pending' ? 'secondary' :
      status === 'Aborted' ? 'warning' :
        status === 'Inactive' ? 'danger' :
          'primary';
}

class User extends Component {

  userDataField = "userData";
  allUserGoals = "allUserGoals"
  allEvaluationQuestions = "allEvaluationQuestions"
  allExercises = "allExercises"

  fieldNames = [
    this.userDataField,
    this.allUserGoals,
    this.allEvaluationQuestions,
    this.allExercises,
  ];

  toBeShownValues = [
    USER_FIRST_NAME_FIELD_NAME,
    USER_LANGUAGE_FIELD_NAME,
    USER_AGE_FIELD_NAME,
    USER_SEX_FIELD_NAME,
    USER_FAVOURITE_SPORT_DAYS_FIELD_NAME,
    USER_GOAL_IDS_FIELD_NAME,
    USER_CURRENT_QUESTION_ID_FIELD_NAME,
    USER_CURRENT_QUESTION_ANSWER_FIELD_NAME,
    USER_LAST_INTERACTION_FIELD_NAME,
  ]

  constructor(props) {
    super(props);
    this.state = {
      ...(createPartialInitialStateFromFields(this.fieldNames)),
    };

    this.getCurrentID.bind(this);

    load(this, this.userDataField, getSingle, {serverEndPoint: SERVER_USER_ENDPOINT, id: this.getCurrentID()});
    load(this, this.allUserGoals, getAll, {serverEndPoint: SERVER_USER_GOAL_ENDPOINT});
    load(this, this.allEvaluationQuestions, getAll, {serverEndPoint: SERVER_QUESTION_ENDPOINT});
    load(this, this.allExercises, getAll, {serverEndPoint: SERVER_EXERCISE_ENDPOINT});
  }

  getCurrentID() {
    return this.props.match.params.id
  }

  unpackUserDetails(userDataObj) {
    return userDataObj
      ? Object.entries(userDataObj) :
      [[USER_FIRST_NAME_FIELD_NAME, (<span><i className="text-muted icon-ban"/> Not found</span>)]];
  }

  render() {
    return (
      <div className="animated fadeIn">
        <Row>
          <Col lg={6}>
            {
              showLoadingOrRender(this, this.userDataField,
                (data) => {
                  const userDetails = this.unpackUserDetails(data);
                  return (
                    <Card>
                      <CardHeader>
                        <strong>
                          <i className="icon-info pr-1"/>
                          User ID: {data[USER_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]}
                        </strong>
                      </CardHeader>
                      <CardBody>
                        <Table responsive striped hover>
                          <tbody>
                          {
                            userDetails.map(([key, value]) => {
                              if (this.toBeShownValues.includes(key)) {
                                const keyDataHandler = getKeyHandlerFor(key);
                                const defaultRow = (
                                  <tr key={key}>
                                    <td>{`${keyDataHandler.keyPrettyNameLong}:`}</td>
                                    <td><strong>{keyDataHandler.valuePrettifier(value, false, true)}</strong></td>
                                  </tr>
                                );
                                if (key === USER_GOAL_IDS_FIELD_NAME) {
                                  return showLoadingOrRender(this, this.allUserGoals,
                                    goals => {
                                      const goalsPrettyMapping = allGoalsIDsToDescription(goals)
                                      return (
                                        <tr key={key}>
                                          <td>{`${keyDataHandler.keyPrettyNameLong}:`}</td>
                                          <td><strong>
                                            {
                                              value.map(oid =>
                                                goalsPrettyMapping[oid[OBJECT_REFERENCE_ID_FIELD_NAME]]
                                              ).join(', ')
                                            }
                                          </strong></td>
                                        </tr>
                                      )
                                    },
                                    defaultRow
                                  )
                                } else if (key === USER_CURRENT_QUESTION_ID_FIELD_NAME) {
                                  return showLoadingOrRender(this, this.allEvaluationQuestions,
                                    questions => {
                                      const questionPrettyMapping = allQuestionsIDsToDescription(questions)
                                      return (
                                        <tr key={key}>
                                          <td>{`${keyDataHandler.keyPrettyNameLong}:`}</td>
                                          <td><strong>
                                            {
                                              `Level ${computeQuestionLevel(questions, value[OBJECT_REFERENCE_ID_FIELD_NAME])}
                                               → ${questionPrettyMapping[value[OBJECT_REFERENCE_ID_FIELD_NAME]]}`
                                            }
                                          </strong></td>
                                        </tr>
                                      )
                                    },
                                    defaultRow
                                  )
                                } else
                                  return defaultRow;
                              } else {
                                return null; // doesn't create an element
                              }
                            })
                          }
                          </tbody>
                        </Table>
                      </CardBody>
                    </Card>
                  )
                },
                createLoading({pt: 3, position: 'center'})
              )
            }
          </Col>

          <Col lg={6}>
            <Card>
              <CardHeader>
                <i className="fa fa-align-justify"/> Sport sessions
              </CardHeader>
              <CardBody>
                {
                  showLoadingOrRender(this, this.userDataField,
                    currentUser => {
                      const statusFieldName = 'Status'
                      const durationFieldName = 'Duration'

                      let exercisesPrettyMapping = undefined

                      const shownFields = [
                        SPORT_SESSION_STARTED_AT_FIELD_NAME,
                        statusFieldName,
                        durationFieldName,
                        SPORT_SESSION_DONE_EXERCISES_ARRAY_FIELD_NAME,
                        SPORT_SESSION_FUN_RATING_FIELD_NAME,
                      ];

                      const getColumnWidthProportion = columnName => {
                        if ([SPORT_SESSION_DONE_EXERCISES_ARRAY_FIELD_NAME].includes(columnName))
                          return "8"; // largest
                        else if ([SPORT_SESSION_STARTED_AT_FIELD_NAME].includes(columnName))
                          return "6"; // medium
                        else if ([durationFieldName, statusFieldName, SPORT_SESSION_FUN_RATING_FIELD_NAME].includes(columnName))
                          return "1" // smallest
                        else return "4" // normal
                      }

                      const computeSportSessionDuration = sportSession => {
                        if (sportSession[SPORT_SESSION_ENDED_AT_FIELD_NAME] === undefined)
                          return undefined
                        else
                          return (
                            convertToUTCMillis(extractDateObject(sportSession[SPORT_SESSION_ENDED_AT_FIELD_NAME]))
                            - convertToUTCMillis(extractDateObject(sportSession[SPORT_SESSION_STARTED_AT_FIELD_NAME]))
                          )
                      }

                      const dataColumns = shownFields.map(field => {
                        return {
                          name: prettifyFieldName(field, true),
                          sortable: true,
                          grow: getColumnWidthProportion(field),
                          wrap: [
                            SPORT_SESSION_STARTED_AT_FIELD_NAME,
                            SPORT_SESSION_DONE_EXERCISES_ARRAY_FIELD_NAME,
                            durationFieldName
                          ].includes(field),

                          // callback to produce data to be sorted
                          selector: sportSession => {
                            if (field === statusFieldName)
                              return computeSportSessionStatus(sportSession)
                            else if (field === durationFieldName) {
                              const sportSessionDuration = computeSportSessionDuration(sportSession)
                              return sportSessionDuration === undefined ? '' : millisToDurationString(sportSessionDuration)
                            } else if ([SPORT_SESSION_STARTED_AT_FIELD_NAME].includes(field))
                              return convertToUTCMillis(extractDateObject(sportSession[field]));
                            else if (field === SPORT_SESSION_DONE_EXERCISES_ARRAY_FIELD_NAME)
                              return showLoadingOrRender(this, this.allExercises,
                                exercises => {
                                  if (!exercisesPrettyMapping)
                                    exercisesPrettyMapping = allExercisesIDsToDescription(exercises)

                                  return sportSession[SPORT_SESSION_DONE_EXERCISES_ARRAY_FIELD_NAME]
                                    .map(doneExercise => doneExercise[DONE_EXERCISE_EXERCISE_ID_FIELD_NAME])
                                    .map(oid => oid[OBJECT_REFERENCE_ID_FIELD_NAME])
                                    .map(id => exercisesPrettyMapping[id])
                                    .join(", ")
                                },
                                getKeyHandlerFor(field).valuePrettifier(sportSession[field], true, false)
                              )
                            else
                              return getKeyHandlerFor(field).valuePrettifier(sportSession[field], true, false);
                          },

                          // callback to produce views to be shown
                          format: sportSession => {
                            if (field === statusFieldName) {
                              const sportSessionStatus = computeSportSessionStatus(sportSession)
                              return (
                                <Badge color={getBadgeColorFromStatus(sportSessionStatus)}>
                                  {sportSessionStatus}
                                </Badge>
                              )
                            } else if (field === durationFieldName) {
                              const sportSessionDuration = computeSportSessionDuration(sportSession)
                              return sportSessionDuration === undefined
                                ? <i className={"fa fa-ellipsis-h"}/>
                                : millisToDurationString(sportSessionDuration)
                            } else if (field === SPORT_SESSION_DONE_EXERCISES_ARRAY_FIELD_NAME)
                              return showLoadingOrRender(this, this.allExercises,
                                exercises => {
                                  if (!exercisesPrettyMapping)
                                    exercisesPrettyMapping = allExercisesIDsToDescription(exercises)

                                  const sportSessionArray = sportSession[SPORT_SESSION_DONE_EXERCISES_ARRAY_FIELD_NAME]
                                  return sportSessionArray.length > 0
                                    ? sportSessionArray
                                      .map(doneExercise => doneExercise[DONE_EXERCISE_EXERCISE_ID_FIELD_NAME])
                                      .map(oid => oid[OBJECT_REFERENCE_ID_FIELD_NAME])
                                      .map(id => exercisesPrettyMapping[id])
                                      .join(", ")
                                    : <i className={"icon-ban"}/>
                                },
                                getKeyHandlerFor(field).valuePrettifier(sportSession[field], true, true)
                              )
                            else if (field === SPORT_SESSION_FUN_RATING_FIELD_NAME)
                              return sportSession[field] === undefined
                                ? <i className={"icon-ban font-1xl"}/>
                                : getKeyHandlerFor(field).valuePrettifier(sportSession[field], true, true)
                            else
                              return getKeyHandlerFor(field).valuePrettifier(sportSession[field], true, true)
                          },
                        }
                      })

                      return <DataTable noHeader={true}
                                        columns={dataColumns}
                                        data={currentUser[USER_SPORT_SESSIONS_ARRAY_FIELD_NAME]}
                                        keyField={`${SPORT_SESSION_STARTED_AT_FIELD_NAME}.${DATE_OBJECT_FIELD_NAME}`}
                                        defaultSortField={SPORT_SESSION_STARTED_AT_FIELD_NAME}
                                        defaultSortAsc={false}
                                        striped={true}
                                        highlightOnHover={true}
                                        noDataComponent={noDataAvailableComponent()}
                        // dense={true} // enable if wanted more compact rows
                                        pagination={true}
                                        paginationPerPage={5}
                                        paginationRowsPerPageOptions={[5, 10, 20, 50, 100, 200, 500]}
                                        className={"user-table"}
                      />
                    },
                    createLoading({})
                  )
                }
              </CardBody>
            </Card>

            <CardEventChartWithOptions
              apiFunction={getUserLevelHistory}
              apiFunctionParams={{
                id: this.getCurrentID()
              }}
              defaultChartType={EVENT_CHART_TYPE_LINE}
              defaultTimeWindow={EVENT_CHART_TIME_WINDOW_LAST_WEEK}
              title={"User progress"}
              singleDimensionDataLegend={"User level"}
              loading={createLoading}
            />

          </Col>
        </Row>
      </div>
    )
  }
}

export default User;
