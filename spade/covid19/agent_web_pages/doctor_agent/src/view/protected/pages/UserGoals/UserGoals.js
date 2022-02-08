import React, {Component} from 'react';
import {Button, Card, CardBody, CardHeader, Col, Modal, ModalBody, ModalFooter, ModalHeader, Row} from 'reactstrap';
import {ACTION_DELETE, getAll, postObject, SERVER_USER_GOAL_ENDPOINT} from "../../../../controller/ServerApi";
import {
  createLoading,
  createPartialInitialStateFromFields,
  load,
  noDataAvailableComponent,
  showLoadingOrRender
} from "../../../../utils/DataLoadingUtils";
import DataTable from "react-data-table-component";
import './UserGoals.css'
import {OBJECT_REFERENCE_ID_FIELD_NAME} from "../../../../model/ModelUtils";
import {Link} from "react-router-dom";
import {
  USER_GOAL_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  USER_GOAL_ID_FIELD_NAME,
  USER_GOAL_TEXT_EN_FIELD_NAME
} from "../../../../model/UserGoalFieldNamesDictionaryToDescription";
import {getKeyHandlerFor, prettifyFieldName} from "../../../../model/FieldPrettifyHandler";
import {debug, warn} from "../../../../utils/Logging";

const currentScriptName = "UserGoals.js";

const getUserGoalLink = userGoalID => `/home/modify/user_goals/${userGoalID}`;

class UserGoals extends Component {

  allUserGoalsField = "allUserGoals";
  fieldNames = [this.allUserGoalsField];

  constructor(props) {
    super(props);
    this.state = {
      ...(createPartialInitialStateFromFields(this.fieldNames)),

    }
  }

  componentDidMount() {
    load(this, this.allUserGoalsField, getAll, {serverEndPoint: SERVER_USER_GOAL_ENDPOINT});
  }

  toggleDeletionModal() {
    this.setState({deletionModalOpen: !this.state.deletionModalOpen})
  }

  deleteCurrentFromServer() {
    postObject(ACTION_DELETE, SERVER_USER_GOAL_ENDPOINT, {id: this.getCurrentID()}).then(
      result => {
        debug(currentScriptName, `Deleted from server:`, result);
        this.setState({uploadingChanges: false})

        // Go to list of objects, when done
        window.history.back()
      },
      error => {
        warn(currentScriptName, `Error from server during deletion:`, error.message);
        this.setErrorMessage(error.message)
      }
    )

    this.toggleDeletionModal()
  }

  render() {
    return (
      <div className="animated fadeIn">
        <Row>
          <Col xl={12}>
            <Card>
              <CardHeader>
                <i className="fa fa-align-justify"/> User Goals
                <div className="card-header-actions">
                  <Link to={getUserGoalLink('new')}>
                    <Button size={'sm'} color={'success'}><i className={"fa fa-plus"}/> New</Button>
                  </Link>
                </div>
                <Modal isOpen={this.state.deletionModalOpen} toggle={this.toggleDeletionModal.bind(this)}
                       className={'modal-danger'}>
                  <ModalHeader toggle={this.toggleDeletionModal.bind(this)}>Delete User Goal</ModalHeader>
                  <ModalBody>
                    This will permanently delete the selected User Goal from database.
                    <br/>
                    <br/>
                    References to this User Goal will be removed from every data structure in which it is.
                    This possibly includes Exercise Sets and User Profiles.
                  </ModalBody>
                  <ModalFooter>
                    <Button color="danger" onClick={this.deleteCurrentFromServer.bind(this)}>Delete</Button>{' '}
                    <Button color="secondary" onClick={this.toggleDeletionModal.bind(this)}>Cancel</Button>
                  </ModalFooter>
                </Modal>
              </CardHeader>
              <CardBody>
                {
                  showLoadingOrRender(this, this.allUserGoalsField,
                    allUserGoals => {

                      const actionsFieldName = 'Actions'

                      const shownFields = [
                        USER_GOAL_TEXT_EN_FIELD_NAME,
                        actionsFieldName
                      ];

                      const getColumnWidthProportion = columnName => {
                        if ([USER_GOAL_TEXT_EN_FIELD_NAME].includes(columnName))
                          return "8"; // largest
                        else if ([].includes(columnName))
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
                          name: prettifyFieldName(field, false, USER_GOAL_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION),
                          sortable: true,
                          grow: getColumnWidthProportion(field),
                          center: [actionsFieldName].includes(field),
                          wrap: [USER_GOAL_TEXT_EN_FIELD_NAME].includes(field),

                          // callback to produce data to be sorted
                          selector: data => {
                            if ([actionsFieldName].includes(field))
                              return ''
                            else
                              return getKeyHandlerFor(
                                field, USER_GOAL_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION
                              ).valuePrettifier(data[field], true, false);
                          },

                          // callback to produce views to be shown
                          format: data => {
                            if (field === actionsFieldName) {
                              return (
                                <div className="form-actions float-right">
                                  <Link to={
                                    getUserGoalLink(data[USER_GOAL_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME])
                                  }>
                                    <Button color={'primary'} size={'sm'} outline>
                                      <i className="cui-pencil icons font-1xl d-block"/>
                                    </Button>
                                  </Link>
                                  <Button color="danger"
                                          size={'sm'} outline
                                          onClick={this.toggleDeletionModal.bind(this)}>
                                    <i className={"cui-trash icons font-1xl d-block"}/>
                                  </Button>
                                </div>
                              )
                            } else
                              return getKeyHandlerFor(
                                field, USER_GOAL_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION
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
                                        data={allUserGoals}
                                        keyField={`${USER_GOAL_ID_FIELD_NAME}.${OBJECT_REFERENCE_ID_FIELD_NAME}`}
                                        striped={true}
                                        highlightOnHover={true}
                                        noDataComponent={noDataAvailableComponent()}
                                        dense={true} // enable if wanted more compact rows
                                        pagination={true}
                                        paginationPerPage={50}
                                        paginationRowsPerPageOptions={[5, 10, 20, 50, 100, 200, 500]}
                                        className={"user-goals-table"}
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

export default UserGoals;
