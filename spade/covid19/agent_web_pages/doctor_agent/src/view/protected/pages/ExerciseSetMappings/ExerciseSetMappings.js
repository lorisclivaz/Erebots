import React, {Component} from 'react';
import {Card, CardBody, CardHeader, Col, Row} from 'reactstrap';
import {
  getAll,
  SERVER_EXERCISE_ENDPOINT,
  SERVER_EXERCISE_MAPPING_ENDPOINT,
  SERVER_EXERCISE_SET_ENDPOINT,
  SERVER_QUESTION_ENDPOINT
} from "../../../../controller/ServerApi";
import {
  createLoading,
  createPartialInitialStateFromFields,
  load,
  noDataAvailableComponent,
  showLoadingOrRender
} from "../../../../utils/DataLoadingUtils";
import DataTable from "react-data-table-component";
import {OBJECT_REFERENCE_ID_FIELD_NAME} from "../../../../model/ModelUtils";
import {getKeyHandlerFor, prettifyFieldName} from "../../../../model/FieldPrettifyHandler";
import Button from "reactstrap/lib/Button";
import {Link} from "react-router-dom";
import './ExerciseSetMappings.css'
import {allQuestionsIDsToDescription} from "../../../../model/QuestionFieldNamesDictionaryToDescription";
import {allExercisesIDsToDescription} from "../../../../model/ExerciseFieldNamesDictionaryToDescription";
import {
  EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME,
  EXERCISE_SET_MAPPING_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  EXERCISE_SET_MAPPING_ID_FIELD_NAME,
  EXERCISE_SET_MAPPING_QUESTION_ANSWER_FIELD_NAME,
  EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME,
  EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME
} from "../../../../model/ExerciseSetMappingFieldNamesDictionaryToDescription";
import {allExerciseSetsIDsToDescription} from "../../../../model/ExerciseSetFieldNamesDictionaryToDescription";
import {computeQuestionLevel} from "../../../../model/QuestionsUtils";

// const currentScriptName = "ExerciseSetMappings.js";

const getExerciseSetMappingLink = exerciseSetMappingID => `/home/modify/exercise_set_mappings/${exerciseSetMappingID}`;

class ExerciseSetMappings extends Component {

  allExerciseSetMappingsField = "allExerciseSetMappings";
  allExerciseSetsField = "allExerciseSets";
  allExercises = "allExercises"
  allEvaluationQuestions = "allEvaluationQuestions"

  fieldNames = [
    this.allExerciseSetMappingsField,
    this.allExerciseSetsField,
    this.allExercises,
    this.allEvaluationQuestions,
  ];

  constructor(props) {
    super(props);
    this.state = {
      ...(createPartialInitialStateFromFields(this.fieldNames)),

    }
  }

  componentDidMount() {
    load(this, this.allEvaluationQuestions, getAll, {serverEndPoint: SERVER_QUESTION_ENDPOINT});
    load(this, this.allExercises, getAll, {serverEndPoint: SERVER_EXERCISE_ENDPOINT});
    load(this, this.allExerciseSetsField, getAll, {serverEndPoint: SERVER_EXERCISE_SET_ENDPOINT});
    load(this, this.allExerciseSetMappingsField, getAll, {serverEndPoint: SERVER_EXERCISE_MAPPING_ENDPOINT});
  }

  idsListToDescriptionHandler = (idsList, idToDescriptionMapping) => {
    const IDs = idsList.map(oid => oid[OBJECT_REFERENCE_ID_FIELD_NAME])
    return IDs.map(id => idToDescriptionMapping[id])
  }

  render() {
    return (
      <div className="animated fadeIn">
        <Row>
          <Col xl={12}>
            <Card>
              <CardHeader>
                <i className="fa fa-align-justify"/> Exercise Set Mappings
                <div className="card-header-actions">
                  <Link to={getExerciseSetMappingLink('new')}>
                    <Button size={'sm'} color={'success'}><i className={"fa fa-plus"}/> New</Button>
                  </Link>
                </div>
              </CardHeader>
              <CardBody>
                {
                  showLoadingOrRender(this, this.allEvaluationQuestions,
                    allEvaluationQuestions => showLoadingOrRender(this, this.allExercises,
                      allExercises => showLoadingOrRender(this, this.allExerciseSetsField,
                        allExerciseSets => showLoadingOrRender(this, this.allExerciseSetMappingsField,
                          allExerciseSetMappings => {

                            const questionsPrettyMapping = allQuestionsIDsToDescription(allEvaluationQuestions)
                            const exercisesPrettyMapping = allExercisesIDsToDescription(allExercises)
                            const exerciseSetsPrettyMapping = allExerciseSetsIDsToDescription(
                              allExerciseSets,
                              exercisesPrettyMapping
                            )

                            const actionsFieldName = 'Actions'
                            const difficultyLevelFieldName = 'Difficulty Level'

                            const shownFields = [
                              EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME,
                              EXERCISE_SET_MAPPING_QUESTION_ANSWER_FIELD_NAME,
                              difficultyLevelFieldName,
                              EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME,
                              EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME,
                              actionsFieldName
                            ];

                            const getColumnWidthProportion = columnName => {
                              if ([
                                EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME,
                                EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME
                              ].includes(columnName))
                                return "8"; // largest
                              else if ([].includes(columnName))
                                return "6"; // medium
                              else if ([
                                EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME,
                                actionsFieldName,
                                difficultyLevelFieldName,
                              ].includes(columnName))
                                return "1" // smallest
                              else return "4" // normal
                            }

                            const getHideColumnOnScreenSize = field => {
                              if ([].includes(field))
                                return "lg" // first hidden
                              else if ([EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME,
                                EXERCISE_SET_MAPPING_QUESTION_ANSWER_FIELD_NAME].includes(field))
                                return "md" // second hidden
                              else if ([].includes(field))
                                return "sm" // third hidden
                              else return null // to not hide
                            }

                            const getQuestionLevel = data => {
                              return computeQuestionLevel(
                                allEvaluationQuestions,
                                data[EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]
                              ) + data[EXERCISE_SET_MAPPING_QUESTION_ANSWER_FIELD_NAME] * 0.1
                            }

                            const dataColumns = shownFields.map(field => {
                              const columnObj = {
                                name: prettifyFieldName(field, false, EXERCISE_SET_MAPPING_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION),
                                sortable: true,
                                grow: getColumnWidthProportion(field),
                                center: [actionsFieldName].includes(field),
                                wrap: [
                                  EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME,
                                  EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME
                                ].includes(field),

                                // callback to produce data to be sorted
                                selector: data => {
                                  if (field === actionsFieldName)
                                    return ''
                                  else if (field === difficultyLevelFieldName)
                                    return getQuestionLevel(data)
                                  else if (field === EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME)
                                    return this.idsListToDescriptionHandler(data[field], exerciseSetsPrettyMapping)
                                  else if (field === EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME)
                                    return questionsPrettyMapping[data[field][OBJECT_REFERENCE_ID_FIELD_NAME]]
                                  else
                                    return getKeyHandlerFor(
                                      field, EXERCISE_SET_MAPPING_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION
                                    ).valuePrettifier(data[field], true, false);
                                },

                                // callback to produce views to be shown
                                format: data => {
                                  if (field === actionsFieldName) {
                                    return (
                                      <Link to={
                                        getExerciseSetMappingLink(
                                          data[EXERCISE_SET_MAPPING_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]
                                        )
                                      }>
                                        <Button color={'primary'} size={'sm'} outline>
                                          <i className="cui-pencil icons font-1xl d-block"/>
                                        </Button>
                                      </Link>
                                    )
                                  } else if (field === difficultyLevelFieldName)
                                    return getQuestionLevel(data).toFixed(1)
                                  else if (field === EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME) {

                                    const exerciseSetList = this.idsListToDescriptionHandler(data[field], exerciseSetsPrettyMapping)
                                    return exerciseSetList.length === 0
                                      ? <span><i className="text-muted icon-ban"/></span>
                                      : exerciseSetList.join(' •• ')
                                  } else if (field === EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME) {
                                    return questionsPrettyMapping[data[field][OBJECT_REFERENCE_ID_FIELD_NAME]]
                                  } else
                                    return getKeyHandlerFor(
                                      field, EXERCISE_SET_MAPPING_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION
                                    ).valuePrettifier(data[field], true, true)
                                },
                              }

                              const hideProportion = getHideColumnOnScreenSize(field)
                              if (hideProportion != null)
                                columnObj['hide'] = hideProportion

                              return columnObj
                            })

                            return <DataTable noHeader={true}
                                              columns={dataColumns}
                                              data={allExerciseSetMappings}
                                              keyField={`${EXERCISE_SET_MAPPING_ID_FIELD_NAME}.${OBJECT_REFERENCE_ID_FIELD_NAME}`}
                                              striped={true}
                                              highlightOnHover={true}
                                              noDataComponent={noDataAvailableComponent()}
                              // dense={true} // enable if wanted more compact rows
                                              pagination={true}
                                              paginationPerPage={50}
                                              paginationRowsPerPageOptions={[5, 10, 20, 50, 100, 200, 500]}
                                              className={"exercise-sets-table"}
                            />
                          },
                          createLoading({})
                        ),
                        createLoading({})
                      ),
                      createLoading({})
                    ),
                    createLoading({})
                  )
                }
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    )
  }
}

export default ExerciseSetMappings;
