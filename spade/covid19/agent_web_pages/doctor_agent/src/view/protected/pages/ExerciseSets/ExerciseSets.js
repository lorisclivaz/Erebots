import React, {Component} from 'react';
import {Card, CardBody, CardHeader, Col, Row} from 'reactstrap';
import {
  getAll,
  SERVER_EXERCISE_ENDPOINT,
  SERVER_EXERCISE_SET_ENDPOINT,
  SERVER_USER_GOAL_ENDPOINT
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
import './ExerciseSets.css'
import {
  EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME,
  EXERCISE_SET_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  EXERCISE_SET_ID_FIELD_NAME,
  EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME
} from "../../../../model/ExerciseSetFieldNamesDictionaryToDescription";
import {allExercisesIDsToDescription} from "../../../../model/ExerciseFieldNamesDictionaryToDescription";
import {allGoalsIDsToDescription} from "../../../../model/UserGoalFieldNamesDictionaryToDescription";

// const currentScriptName = "ExerciseSets.js";

const getExerciseSetLink = exerciseSetID => `/home/modify/exercise_sets/${exerciseSetID}`;

class ExerciseSets extends Component {

  allExerciseSetsField = "allExerciseSets";
  allExercises = "allExercises"
  allUserGoals = "allUserGoals"

  fieldNames = [
    this.allExerciseSetsField,
    this.allExercises,
    this.allUserGoals,
  ];

  constructor(props) {
    super(props);
    this.state = {
      ...(createPartialInitialStateFromFields(this.fieldNames)),

    }
  }

  componentDidMount() {
    load(this, this.allUserGoals, getAll, {serverEndPoint: SERVER_USER_GOAL_ENDPOINT});
    load(this, this.allExercises, getAll, {serverEndPoint: SERVER_EXERCISE_ENDPOINT});
    load(this, this.allExerciseSetsField, getAll, {serverEndPoint: SERVER_EXERCISE_SET_ENDPOINT});
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
                <i className="fa fa-align-justify"/> Exercise Sets
                <div className="card-header-actions">
                  <Link to={getExerciseSetLink('new')}>
                    <Button size={'sm'} color={'success'}><i className={"fa fa-plus"}/> New</Button>
                  </Link>
                </div>
              </CardHeader>
              <CardBody>
                {
                  showLoadingOrRender(this, this.allUserGoals,
                    allUserGoals => showLoadingOrRender(this, this.allExercises,
                      allExercises => showLoadingOrRender(this, this.allExerciseSetsField,
                        allExerciseSets => {

                          const goalsPrettyMapping = allGoalsIDsToDescription(allUserGoals)
                          const exercisesPrettyMapping = allExercisesIDsToDescription(allExercises)

                          const actionsFieldName = 'Actions'

                          const shownFields = [
                            EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME,
                            EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME,
                            actionsFieldName
                          ];

                          const getColumnWidthProportion = columnName => {
                            if ([EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME].includes(columnName))
                              return "8"; // largest
                            else if ([EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME].includes(columnName))
                              return "6"; // medium
                            else if ([actionsFieldName].includes(columnName))
                              return "1" // smallest
                            else return "4" // normal
                          }

                          const getHideColumnOnScreenSize = field => {
                            if ([].includes(field))
                              return "lg" // first hidden
                            else if ([].includes(field))
                              return "md" // second hidden
                            else if ([].includes(field))
                              return "sm" // third hidden
                            else return null // to not hide
                          }

                          const dataColumns = shownFields.map(field => {
                            const columnObj = {
                              name: prettifyFieldName(field, false, EXERCISE_SET_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION),
                              sortable: true,
                              grow: getColumnWidthProportion(field),
                              center: [actionsFieldName].includes(field),
                              wrap: [
                                EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME,
                                EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME
                              ].includes(field),

                              // callback to produce data to be sorted
                              selector: data => {
                                if (field === actionsFieldName)
                                  return ''
                                else if (field === EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME)
                                  return this.idsListToDescriptionHandler(data[field], exercisesPrettyMapping)
                                else if (field === EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME)
                                  return this.idsListToDescriptionHandler(data[field], goalsPrettyMapping)
                                else
                                  return getKeyHandlerFor(
                                    field, EXERCISE_SET_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION
                                  ).valuePrettifier(data[field], true, false);
                              },

                              // callback to produce views to be shown
                              format: data => {
                                if (field === actionsFieldName) {
                                  return (
                                    <Link to={
                                      getExerciseSetLink(data[EXERCISE_SET_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME])
                                    }>
                                      <Button color={'primary'} size={'sm'} outline>
                                        <i className="cui-pencil icons font-1xl d-block"/>
                                      </Button>
                                    </Link>
                                  )
                                } else if (field === EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME) {
                                  return (
                                    this.idsListToDescriptionHandler(data[field], exercisesPrettyMapping)
                                      .join(', ')
                                  )
                                } else if (field === EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME) {
                                  return (
                                    this.idsListToDescriptionHandler(data[field], goalsPrettyMapping)
                                      .join(', ')
                                  )
                                } else
                                  return getKeyHandlerFor(
                                    field, EXERCISE_SET_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION
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
                                            data={allExerciseSets}
                                            keyField={`${EXERCISE_SET_ID_FIELD_NAME}.${OBJECT_REFERENCE_ID_FIELD_NAME}`}
                                            striped={true}
                                            highlightOnHover={true}
                                            noDataComponent={noDataAvailableComponent()}
                                            dense={true} // enable if wanted more compact rows
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

export default ExerciseSets;
