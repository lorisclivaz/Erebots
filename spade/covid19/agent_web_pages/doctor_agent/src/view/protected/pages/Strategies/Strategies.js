import React, {Component} from 'react';
import {Card, CardBody, CardHeader, Col, Row} from 'reactstrap';
import {getAll, SERVER_STRATEGY_ENDPOINT} from "../../../../controller/ServerApi";
import {
  createLoading,
  createPartialInitialStateFromFields,
  load,
  noDataAvailableComponent,
  showLoadingOrRender
} from "../../../../utils/DataLoadingUtils";
import DataTable from "react-data-table-component";
import './Strategies.css'
import {OBJECT_REFERENCE_ID_FIELD_NAME} from "../../../../model/ModelUtils";
import {getKeyHandlerFor, prettifyFieldName} from "../../../../model/FieldPrettifyHandler";
import {
  STRATEGY_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  STRATEGY_ID_FIELD_NAME,
  STRATEGY_NAME_FIELD_NAME,
  STRATEGY_DESCRIPTION_FIELD_NAME
} from "../../../../model/StrategyFieldNamesDictionaryToDescription";
import Button from "reactstrap/lib/Button";
import {Link} from "react-router-dom";

const currentScriptName = "Strategies.js";

const getStrategyLink = strategyID => `/home/modify/strategies/${strategyID}`;

class Strategies extends Component {

  allStrategiesField = "allStrategies";
  fieldNames = [this.allStrategiesField];

  constructor(props) {
    super(props);
    this.state = {
      ...(createPartialInitialStateFromFields(this.fieldNames)),

    }
  }

  componentDidMount() {
    load(this, this.allStrategiesField, getAll, {serverEndPoint: SERVER_STRATEGY_ENDPOINT});
  }


  render() {
    return (
      <div className="animated fadeIn">
        <Row>
          <Col xl={12}>
            <Card>
              <CardHeader>
                <i className="fa fa-align-justify"/> Strategies
                <div className="card-header-actions">
                  <Link to={getStrategyLink('new')}>
                    <Button size={'sm'} color={'success'}><i className={"fa fa-plus"}/> New</Button>
                  </Link>
                </div>
              </CardHeader>
              <CardBody>
                {
                  showLoadingOrRender(this, this.allStrategiesField,
                    allStrategies => {

                      const actionsFieldName = 'Actions'
                      const descriptionFieldName = 'Description'
                      const nameFieldName = 'Name'

                      const shownFields = [
                        nameFieldName,
                        descriptionFieldName,
                        actionsFieldName
                      ];

                      const getColumnWidthProportion = columnName => {
                        if ([descriptionFieldName].includes(columnName))
                          return "8"; // largest
                        else if ([].includes(columnName))
                          return "6"; // medium
                        else if ([actionsFieldName].includes(columnName))
                          return "1" // smallest
                        else return "2" // normal
                      }

                      const getHideColumnOnScreenSize = field => {
                        if ([].includes(field))
                          return "lg" // first hidden
                        else if ([descriptionFieldName].includes(field))
                          return "md" // second hidden
                        else if ([].includes(field))
                          return "sm" // third hidden
                        else return null // to not hide
                      }

                      const dataColumns = shownFields.map(field => {
                        const columnObj = {
                          name: prettifyFieldName(field, false, STRATEGY_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION),
                          sortable: true,
                          grow: getColumnWidthProportion(field),
                          center: [actionsFieldName].includes(field),
                          wrap: [nameFieldName, descriptionFieldName].includes(field),

                          // callback to produce data to be sorted
                          selector: data => {
                            if ([actionsFieldName].includes(field))
                              return ''
                            else if (field === nameFieldName)
                              return data[STRATEGY_NAME_FIELD_NAME]
                            else
                              return getKeyHandlerFor(
                                field, STRATEGY_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION
                              ).valuePrettifier(data[field], true, false);
                          },

                          // callback to produce views to be shown
                          format: data => {
                            if (field === actionsFieldName) {
                              return (
                                <Link to={
                                  getStrategyLink(data[STRATEGY_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME])
                                }>
                                  <Button color={'primary'} size={'sm'} outline>
                                    <i className="cui-pencil icons font-1xl d-block"/>
                                  </Button>
                                </Link>
                              )
                            } else if (field === nameFieldName)
                              return data[STRATEGY_NAME_FIELD_NAME]
                            else if (field === descriptionFieldName) {
                              return data[STRATEGY_DESCRIPTION_FIELD_NAME]
                            } else
                              return getKeyHandlerFor(
                                field, STRATEGY_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION
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
                                        data={allStrategies}
                                        keyField={`${STRATEGY_ID_FIELD_NAME}.${OBJECT_REFERENCE_ID_FIELD_NAME}`}
                                        striped={true}
                                        highlightOnHover={true}
                                        noDataComponent={noDataAvailableComponent()}
                                        dense={true} // enable if wanted more compact rows
                                        pagination={true}
                                        paginationPerPage={50}
                                        paginationRowsPerPageOptions={[5, 10, 20, 50, 100, 200, 500]}
                                        className={"strategies-table"}
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

export default Strategies;
