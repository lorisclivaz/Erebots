import React, {Component} from 'react';
import {Card, CardBody, CardHeader, Col, Row} from 'reactstrap';
import {getAll, SERVER_API_ADDRESS, SERVER_EXERCISE_ENDPOINT} from "../../../../controller/ServerApi";
import {
  createLoading,
  createPartialInitialStateFromFields,
  load,
  noDataAvailableComponent,
  showLoadingOrRender
} from "../../../../utils/DataLoadingUtils";
import DataTable from "react-data-table-component";
import './Exercises.css'
import {OBJECT_REFERENCE_ID_FIELD_NAME} from "../../../../model/ModelUtils";
import {getKeyHandlerFor, prettifyFieldName} from "../../../../model/FieldPrettifyHandler";
import {
  EXERCISE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  EXERCISE_ID_FIELD_NAME,
  EXERCISE_LABEL_FIELD_NAME,
  EXERCISE_TEXT_EN_FIELD_NAME
} from "../../../../model/ExerciseFieldNamesDictionaryToDescription";
import Button from "reactstrap/lib/Button";
import {Link} from "react-router-dom";
import CardImg from "reactstrap/lib/CardImg";

// const currentScriptName = "Exercises.js";

const getExerciseLink = exerciseID => `/home/modify/exercises/${exerciseID}`;

class Exercises extends Component {

  allExercisesField = "allExercises";
  fieldNames = [this.allExercisesField];

  constructor(props) {
    super(props);
    this.state = {
      ...(createPartialInitialStateFromFields(this.fieldNames)),

    }
  }

  componentDidMount() {
    load(this, this.allExercisesField, getAll, {serverEndPoint: SERVER_EXERCISE_ENDPOINT});
  }


  render() {
    return (
      <div className="animated fadeIn">
        <Row>
          <Col xl={12}>
            <Card>
              <CardHeader>
                <i className="fa fa-align-justify"/> Exercises
                <div className="card-header-actions">
                  <Link to={getExerciseLink('new')}>
                    <Button size={'sm'} color={'success'}><i className={"fa fa-plus"}/> New</Button>
                  </Link>
                </div>
              </CardHeader>
              <CardBody>
                {
                  showLoadingOrRender(this, this.allExercisesField,
                    allExercises => {

                      const actionsFieldName = 'Actions'
                      const gifFieldName = 'GIF Image'
                      const nameFieldName = 'User Shown Description'

                      const shownFields = [
                        EXERCISE_LABEL_FIELD_NAME,
                        nameFieldName,
                        gifFieldName,
                        actionsFieldName
                      ];

                      const getColumnWidthProportion = columnName => {
                        if ([nameFieldName].includes(columnName))
                          return "8"; // largest
                        else if ([].includes(columnName))
                          return "6"; // medium
                        else if ([actionsFieldName, gifFieldName].includes(columnName))
                          return "1" // smallest
                        else return "4" // normal
                      }

                      const getHideColumnOnScreenSize = field => {
                        if ([].includes(field))
                          return "lg" // first hidden
                        else if ([gifFieldName, EXERCISE_LABEL_FIELD_NAME].includes(field))
                          return "md" // second hidden
                        else if ([].includes(field))
                          return "sm" // third hidden
                        else return null // to not hide
                      }

                      const dataColumns = shownFields.map(field => {
                        const columnObj = {
                          name: prettifyFieldName(field, false, EXERCISE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION),
                          sortable: true,
                          grow: getColumnWidthProportion(field),
                          center: [gifFieldName, actionsFieldName].includes(field),
                          wrap: [nameFieldName, EXERCISE_LABEL_FIELD_NAME].includes(field),

                          // callback to produce data to be sorted
                          selector: data => {
                            if ([gifFieldName, actionsFieldName].includes(field))
                              return ''
                            else if (field === nameFieldName)
                              return data[EXERCISE_TEXT_EN_FIELD_NAME]
                            else
                              return getKeyHandlerFor(
                                field, EXERCISE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION
                              ).valuePrettifier(data[field], true, false);
                          },

                          // callback to produce views to be shown
                          format: data => {
                            if (field === actionsFieldName) {
                              return (
                                <Link to={
                                  getExerciseLink(data[EXERCISE_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME])
                                }>
                                  <Button color={'primary'} size={'sm'} outline>
                                    <i className="cui-pencil icons font-1xl d-block"/>
                                  </Button>
                                </Link>
                              )
                            } else if (field === nameFieldName)
                              return data[EXERCISE_TEXT_EN_FIELD_NAME]
                            else if (field === gifFieldName) {
                              const exerciseID = data[EXERCISE_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]
                              return (
                                <CardImg id={exerciseID} alt={"Exercise Image preview"}
                                         key={exerciseID}
                                         src={`${SERVER_API_ADDRESS}${SERVER_EXERCISE_ENDPOINT}/${exerciseID}/gif?random=${performance.now()}`}
                                />
                              )
                            } else
                              return getKeyHandlerFor(
                                field, EXERCISE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION
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
                                        data={allExercises}
                                        keyField={`${EXERCISE_ID_FIELD_NAME}.${OBJECT_REFERENCE_ID_FIELD_NAME}`}
                                        striped={true}
                                        highlightOnHover={true}
                                        noDataComponent={noDataAvailableComponent()}
                                        dense={true} // enable if wanted more compact rows
                                        pagination={true}
                                        paginationPerPage={50}
                                        paginationRowsPerPageOptions={[5, 10, 20, 50, 100, 200, 500]}
                                        className={"exercises-table"}
                      />
                    },
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

export default Exercises;
