import React, {Component} from 'react';
import {Card, CardBody, CardHeader, Col, Row} from 'reactstrap';
import {getAll, SERVER_QUESTION_ENDPOINT} from "../../../../controller/ServerApi";
import {
  createLoading,
  createPartialInitialStateFromFields,
  load,
  noDataAvailableComponent,
  showLoadingOrRender
} from "../../../../utils/DataLoadingUtils";
import DataTable from "react-data-table-component";
import {Link} from "react-router-dom";
import Button from "reactstrap/lib/Button";
import {
  allQuestionsIDsToDescription,
  QUESTION_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  QUESTION_ID_FIELD_NAME,
  QUESTION_NEXT_FIELD_NAME,
  QUESTION_PREVIOUS_FIELD_NAME,
  QUESTION_TEXT_EN_FIELD_NAME
} from "../../../../model/QuestionFieldNamesDictionaryToDescription";
import {getKeyHandlerFor, prettifyFieldName} from "../../../../model/FieldPrettifyHandler";
import {computeQuestionLevel, sortQuestionObjects} from "../../../../model/QuestionsUtils";
import {OBJECT_REFERENCE_ID_FIELD_NAME} from "../../../../model/ModelUtils";
import './Questions.css'

// const currentScriptName = "Questions.js";

const getQuestionLink = questionID => `/home/modify/questions/${questionID}`;

class Questions extends Component {

  allQuestions = "allQuestions";
  fieldNames = [this.allQuestions];

  constructor(props) {
    super(props);
    this.state = {
      ...(createPartialInitialStateFromFields(this.fieldNames)),

    }
  }

  componentDidMount() {
    load(this, this.allQuestions, getAll, {serverEndPoint: SERVER_QUESTION_ENDPOINT});
  }


  render() {
    return (
      <div className="animated fadeIn">
        <Row>
          <Col xl={12}>
            <Card>
              <CardHeader>
                <i className="fa fa-align-justify"/> Questions
                <div className="card-header-actions">
                  <Link to={"/home/modify/questions/order"}>
                    <Button size={'sm'} color={'primary'} className={'mr-2'}>
                      <i className={"fa fa-list"}/> Reorder
                    </Button>
                  </Link>
                  <Link to={getQuestionLink('new')}>
                    <Button size={'sm'} color={'success'}><i className={"fa fa-plus"}/> New</Button>
                  </Link>
                </div>
              </CardHeader>
              <CardBody>
                {
                  showLoadingOrRender(this, this.allQuestions,
                    allQuestions => {

                      const actionsFieldName = 'Actions'
                      const levelFieldName = 'Level'

                      const questionsPrettyMapping = allQuestionsIDsToDescription(allQuestions)

                      const shownFields = [
                        levelFieldName,
                        QUESTION_TEXT_EN_FIELD_NAME,
                        QUESTION_PREVIOUS_FIELD_NAME,
                        QUESTION_NEXT_FIELD_NAME,
                        actionsFieldName
                      ];

                      const getColumnWidthProportion = columnName => {
                        if ([QUESTION_TEXT_EN_FIELD_NAME].includes(columnName))
                          return "8"; // largest
                        else if ([].includes(columnName))
                          return "6"; // medium
                        else if ([QUESTION_ID_FIELD_NAME, levelFieldName, actionsFieldName].includes(columnName))
                          return "1" // smallest
                        else return "4" // normal
                      }

                      const getHideColumnOnScreenSize = field => {
                        if ([QUESTION_NEXT_FIELD_NAME, QUESTION_PREVIOUS_FIELD_NAME].includes(field))
                          return "lg" // first hidden
                        else if ([QUESTION_ID_FIELD_NAME].includes(field))
                          return "md" // second hidden
                        else if ([levelFieldName].includes(field))
                          return "sm" // third hidden
                        else return null // to not hide
                      }

                      const dataColumns = shownFields.map(field => {
                        const columnObj = {
                          name: prettifyFieldName(field, false, QUESTION_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION),
                          sortable: true,
                          grow: getColumnWidthProportion(field),
                          center: [actionsFieldName].includes(field),
                          wrap: [
                            QUESTION_TEXT_EN_FIELD_NAME,
                            QUESTION_NEXT_FIELD_NAME,
                            QUESTION_PREVIOUS_FIELD_NAME
                          ].includes(field),

                          // callback to produce data to be sorted
                          selector: data => {
                            if ([actionsFieldName].includes(field))
                              return ''
                            else if (field === levelFieldName)
                              return computeQuestionLevel(allQuestions, data[QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME])
                            else if ([QUESTION_NEXT_FIELD_NAME, QUESTION_PREVIOUS_FIELD_NAME].includes(field))
                              return data[field]
                                ? questionsPrettyMapping[data[field][OBJECT_REFERENCE_ID_FIELD_NAME]]
                                : ''
                            else
                              return getKeyHandlerFor(
                                field, QUESTION_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION
                              ).valuePrettifier(data[field], true, false);
                          },

                          // callback to produce views to be shown
                          format: data => {
                            if (field === actionsFieldName) {
                              return (
                                <Link to={
                                  getQuestionLink(data[QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME])
                                }>
                                  <Button color={'primary'} size={'sm'} outline>
                                    <i className="cui-pencil icons font-1xl d-block"/>
                                  </Button>
                                </Link>
                              )
                            } else if (field === levelFieldName)
                              return computeQuestionLevel(allQuestions, data[QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME])
                            else if ([QUESTION_NEXT_FIELD_NAME, QUESTION_PREVIOUS_FIELD_NAME].includes(field))
                              return data[field]
                                ? questionsPrettyMapping[data[field][OBJECT_REFERENCE_ID_FIELD_NAME]]
                                : <i className={'icon icon-ban'}/>
                            else
                              return getKeyHandlerFor(
                                field, QUESTION_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION
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
                                        data={sortQuestionObjects(allQuestions)}
                                        keyField={`${QUESTION_ID_FIELD_NAME}.${OBJECT_REFERENCE_ID_FIELD_NAME}`}
                                        striped={true}
                                        highlightOnHover={true}
                                        noDataComponent={noDataAvailableComponent()}
                                        dense={true} // enable if wanted more compact rows
                                        pagination={true}
                                        paginationPerPage={50}
                                        paginationRowsPerPageOptions={[5, 10, 20, 50, 100, 200, 500]}
                                        className={"questions-table"}
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

export default Questions;
