import React, {Component} from 'react';
import {Card, CardBody, CardHeader, Col, Collapse, Progress, Row,} from 'reactstrap';
import {
  getAll,
  getObjectCount,
  SERVER_QUESTION_ENDPOINT,
  SERVER_USER_COUNT_ENDPOINT,
  SERVER_USER_ENDPOINT
} from "../../../../controller/ServerApi";
import {
  createLoading,
  createPartialInitialStateFromFields,
  load,
  showLoadingOrRender
} from "../../../../utils/DataLoadingUtils";
import {SEX_FIELD_TO_PRETTY_DESCRIPTION} from "../../../../model/FieldValuesDictionaryToDescription";
import {
  PROFILE_AVAILABLE_AGGREGATION_FIELDS,
  PROFILE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  USER_AGE_FIELD_NAME,
  USER_CURRENT_QUESTION_ID_FIELD_NAME,
  USER_SEX_FIELD_NAME
} from "../../../../model/ProfileFieldNamesDictionaryToHandlers";
import {
  AGGREGATION_CHART_TYPE_BAR,
  AGGREGATION_CHART_TYPE_RADAR,
  CardAggregationChartWithOptions,
  CHART_SHOW_VALUES_HIDE,
  CHART_SHOW_VALUES_PERCENTAGE
} from "../../components/charts/CardAggregationChartWithOptions";
import {getKeyHandlerFor} from "../../../../model/FieldPrettifyHandler";
import {OBJECT_REFERENCE_ID_FIELD_NAME} from "../../../../model/ModelUtils";
import {computeQuestionLevel} from "../../../../model/QuestionsUtils";

// const currentScriptName = "Dashboard.js";

const DATA_COUNT_FIELD_NAME = "count";
const SERVER_FIELD_MALE = Object.keys(SEX_FIELD_TO_PRETTY_DESCRIPTION)[0];
const SERVER_FIELD_FEMALE = Object.keys(SEX_FIELD_TO_PRETTY_DESCRIPTION)[1];

class Dashboard extends Component {

  userCountField = "patientCount";
  usersBySexField = "usersBySex";
  allUserProfilesField = "allUserProfiles";
  allUserEvaluationQuestions = "allQuestions"

  fieldNames = [
    this.userCountField,
    this.usersBySexField,
    this.allUserProfilesField,
    this.allUserEvaluationQuestions,
  ];

  constructor(props) {
    super(props);

    this.state = {
      ...(createPartialInitialStateFromFields(this.fieldNames)),

      collapsedPatientStatistics: false,
    };

    load(this, this.userCountField, getObjectCount, {serverEndPoint: SERVER_USER_COUNT_ENDPOINT});
    load(this, this.usersBySexField, getAll, {
      serverEndPoint: SERVER_USER_ENDPOINT, aggregateByDimension1: USER_SEX_FIELD_NAME
    });
    load(this, this.allUserProfilesField, getAll, {serverEndPoint: SERVER_USER_ENDPOINT})
    load(this, this.allUserEvaluationQuestions, getAll, {serverEndPoint: SERVER_QUESTION_ENDPOINT})

  }

  /** Creates a Male or Female Progress group */
  createMaleOrFemaleProgressGroup(
    sex,
    sexAggregatedField,
    barColor = 'success',
    showHeaderIcon = true
  ) {
    const sexHandler = getKeyHandlerFor(USER_SEX_FIELD_NAME);
    return showLoadingOrRender(this, sexAggregatedField,
      (data) => {
        let total = 0;
        Object.keys(data).forEach(k => total += data[k].length);
        const absoluteValue = (data[sex] || []).length;
        const percentage = Math.round((absoluteValue * 1000) / total) / 10;

        return (
          <div className="progress-group">
            <div className="progress-group-header">
              {
                showHeaderIcon
                  ? <i className={`progress-group-icon icon-user${sex === SERVER_FIELD_FEMALE ? '-female' : ''}`}/>
                  : null
              }
              <span className="title">{sexHandler.valuePrettifier(sex, false, false)}</span>
              <span className="ml-auto font-weight-bold">{absoluteValue} <span
                className="text-muted small">({percentage} %)</span></span>
            </div>
            <div className="progress-group-bars">
              <Progress className="progress-xs" color={barColor} value={percentage}/>
            </div>
          </div>
        )
      },
      <div className="progress-group">
        <div className="progress-group-header">
          <span className="title">{sexHandler.valuePrettifier(sex, false, false)}</span>
          {createLoading({position: 'right', otherClasses: 'ml-auto'})}
        </div>
        <div className="progress-group-bars">
          <Progress className="progress-xs" color={barColor} value="0"/>
        </div>
      </div>
    )
  }

  /** Creates a Male aor Female callout */
  createMaleOrFemaleCallout(
    sex,
    sexAggregatedField,
    calloutType = 'info',
    barColor = 'success',
    showIconAbove = true
  ) {
    return (
      <div className={`callout callout-${calloutType}`}>
        {showIconAbove ? <i className={`icon-user${sex === SERVER_FIELD_FEMALE ? '-female' : ''}`}/> : null}
        <br/>
        {this.createMaleOrFemaleProgressGroup(sex, sexAggregatedField, barColor, !showIconAbove)}
      </div>
    );
  }

  render() {
    return (
      <div className="animated fadeIn">

        <Row>
          <Col>
            <Card>
              <CardHeader>
                User statistics
                <div className="card-header-actions">
                  <div className="card-header-action btn btn-minimize" data-target="#patientStatisticsCard"
                       onClick={() => this.setState({collapsedPatientStatistics: !this.state.collapsedPatientStatistics})}>
                    <i className={`icon-arrow-${this.state.collapsedPatientStatistics ? "down" : "up"}`}/>
                  </div>
                </div>
              </CardHeader>
              <Collapse isOpen={!this.state.collapsedPatientStatistics} id="patientStatisticsCard">
                <CardBody>
                  <Row>
                    <Col xs="24" md="12" xl="12">
                      <Row>
                        <Col sm="2">
                          <div className="callout callout-info">
                            <small className="text-muted">Total Users</small>
                            <br/>
                            {
                              showLoadingOrRender(this, this.userCountField,
                                (data) => <strong className="h4">{data[DATA_COUNT_FIELD_NAME]}</strong>,
                                createLoading({position: "left"})
                              )
                            }
                          </div>
                        </Col>
                        <Col sm="5">
                          {this.createMaleOrFemaleCallout(SERVER_FIELD_MALE, this.usersBySexField, "success", "success")}
                        </Col>
                        <Col sm="5">
                          {this.createMaleOrFemaleCallout(SERVER_FIELD_FEMALE, this.usersBySexField, "success", "success")}
                        </Col>
                      </Row>

                      <hr className="mt-0"/>

                      {
                        showLoadingOrRender(this, this.allUserEvaluationQuestions,
                          allQuestions => {

                            const specificMapping = {
                              [USER_CURRENT_QUESTION_ID_FIELD_NAME]: {
                                ...PROFILE_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION[USER_CURRENT_QUESTION_ID_FIELD_NAME],
                                valuePrettifier: (value, shortDescription = false) => {
                                  let toAccessObj = value
                                  if (typeof value === "string") {
                                    try {
                                      toAccessObj = JSON.parse(value.replaceAll('\'', '"'))
                                    } catch (e) {
                                    }
                                  }
                                  if (typeof toAccessObj === "object") {
                                    const questionLevel = computeQuestionLevel(allQuestions, toAccessObj[OBJECT_REFERENCE_ID_FIELD_NAME])
                                    return shortDescription
                                      ? `Level ${questionLevel}`
                                      : `Question level ${questionLevel}`
                                  } else
                                    return value
                                },
                              }
                            }

                            return (
                              <Row>
                                <Col sm="6">
                                  <CardAggregationChartWithOptions
                                    apiFunction={getAll}
                                    apiFunctionParams={{serverEndPoint: SERVER_USER_ENDPOINT}}
                                    title={"Users"}
                                    firstDimensionAggregationFields={PROFILE_AVAILABLE_AGGREGATION_FIELDS}
                                    secondDimensionAggregationFields={PROFILE_AVAILABLE_AGGREGATION_FIELDS}
                                    defaultAggregationField1={USER_AGE_FIELD_NAME}
                                    defaultAggregationField2={null}
                                    defaultShowValues={CHART_SHOW_VALUES_PERCENTAGE}
                                    defaultChartType={AGGREGATION_CHART_TYPE_BAR}
                                    singleDimensionDataLegend={"Number of Users"}
                                    specificMappingsForFields={specificMapping}
                                    loading={createLoading}/>
                                </Col>
                                <Col sm="6">
                                  <CardAggregationChartWithOptions
                                    apiFunction={getAll}
                                    apiFunctionParams={{serverEndPoint: SERVER_USER_ENDPOINT}}
                                    title={"Users"}
                                    firstDimensionAggregationFields={PROFILE_AVAILABLE_AGGREGATION_FIELDS}
                                    secondDimensionAggregationFields={PROFILE_AVAILABLE_AGGREGATION_FIELDS}
                                    defaultAggregationField1={USER_AGE_FIELD_NAME}
                                    defaultAggregationField2={USER_SEX_FIELD_NAME}
                                    defaultShowValues={CHART_SHOW_VALUES_HIDE}
                                    defaultChartType={AGGREGATION_CHART_TYPE_RADAR}
                                    singleDimensionDataLegend={"Number of Users"}
                                    specificMappingsForFields={specificMapping}
                                    loading={createLoading}/>
                                </Col>
                              </Row>
                            )
                          },
                          createLoading({})
                        )
                      }
                    </Col>
                  </Row>
                </CardBody>
              </Collapse>
            </Card>
          </Col>
        </Row>

      </div>
    );
  }
}

export default Dashboard;
