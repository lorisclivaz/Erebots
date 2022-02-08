import React, {Component} from 'react';
import {
  Button,
  Card,
  CardBody,
  CardHeader,
  Col,
  Form,
  FormGroup,
  Input,
  Label,
  Modal,
  ModalBody,
  ModalFooter,
  ModalHeader,
  Row
} from 'reactstrap';
import {
  ACTION_CREATE,
  ACTION_DELETE,
  ACTION_MODIFY,
  getSingle,
  postObject,
  SERVER_USER_GOAL_ENDPOINT,
} from "../../../../controller/ServerApi";
import {
  createLoading,
  createPartialInitialStateFromFields,
  errorComponent,
  load,
  showLoadingOrRender
} from "../../../../utils/DataLoadingUtils";
import {OBJECT_REFERENCE_ID_FIELD_NAME} from "../../../../model/ModelUtils";
import {
  USER_GOAL_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  USER_GOAL_ID_FIELD_NAME,
  USER_GOAL_TEXT_DE_FIELD_NAME,
  USER_GOAL_TEXT_EN_FIELD_NAME,
  USER_GOAL_TEXT_FR_FIELD_NAME,
  USER_GOAL_TEXT_IT_FIELD_NAME
} from "../../../../model/UserGoalFieldNamesDictionaryToDescription";
import {debug, log, warn} from "../../../../utils/Logging";
import {getKeyHandlerFor} from "../../../../model/FieldPrettifyHandler";
import {Link} from "react-router-dom";
import './UserGoal.css'

const currentScriptName = "UserGoal.js";

class UserGoal extends Component {

  userGoalData = "userGoalData";

  fieldNames = [
    this.userGoalData,
  ];

  formID = "user-goal-form"

  constructor(props) {
    super(props);
    this.state = {
      ...(createPartialInitialStateFromFields(this.fieldNames)),
      objID: '',
      [USER_GOAL_TEXT_EN_FIELD_NAME]: '',
      [USER_GOAL_TEXT_IT_FIELD_NAME]: '',
      [USER_GOAL_TEXT_FR_FIELD_NAME]: '',
      [USER_GOAL_TEXT_DE_FIELD_NAME]: '',
      uploadingChanges: false,
      errorMessage: '',
      deletionModalOpen: false,
    };

    this.setCurrentStateFromData.bind(this);
    this.getCurrentID.bind(this);
    this.handleTextChange.bind(this);
    this.sendChangesToServer.bind(this);
    this.setErrorMessage.bind(this);
    this.toggleDeletionModal.bind(this);
    this.deleteCurrentFromServer.bind(this);

    if (!this.isHandlingNewObject()) {
      load(this, this.userGoalData, getSingle,
        {serverEndPoint: SERVER_USER_GOAL_ENDPOINT, id: this.getCurrentID()},
        (data) => this.setCurrentStateFromData(data)
      );
    }
  }

  setCurrentStateFromData(data) {
    this.setState({
      objID: data[USER_GOAL_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME],
      [USER_GOAL_TEXT_EN_FIELD_NAME]: data[USER_GOAL_TEXT_EN_FIELD_NAME],
      [USER_GOAL_TEXT_IT_FIELD_NAME]: data[USER_GOAL_TEXT_IT_FIELD_NAME] || '',
      [USER_GOAL_TEXT_FR_FIELD_NAME]: data[USER_GOAL_TEXT_FR_FIELD_NAME] || '',
      [USER_GOAL_TEXT_DE_FIELD_NAME]: data[USER_GOAL_TEXT_DE_FIELD_NAME] || '',
    })
  }

  getCurrentID() {
    return this.props.match.params.id
  }

  isHandlingNewObject() {
    return this.getCurrentID() === "new"
  }

  handleTextChange(field, changedText) {
    const changedState = {}
    changedState[field] = changedText
    this.setState(changedState)
  }

  setErrorMessage(errorMessage) {
    this.setState({
      uploadingChanges: false,
      errorMessage: errorMessage
    })
    window.scrollTo(0, 0)
  }

  sendChangesToServer(insertNew = false) {
    log(currentScriptName, `Called sendChangesToServer with insertNew=${insertNew}`);
    this.setState({
      uploadingChanges: true,
      errorMessage: ''
    })

    const formData = new FormData(document.getElementById(this.formID))
    if (!formData.get(USER_GOAL_TEXT_EN_FIELD_NAME)) {
      this.setErrorMessage('English description is mandatory!')
    } else {
      let serverPromise
      if (insertNew) {
        serverPromise = postObject(ACTION_CREATE, SERVER_USER_GOAL_ENDPOINT, {formDataObject: formData})
      } else {
        const toUpdateID = this.getCurrentID()
        serverPromise = postObject(ACTION_MODIFY, SERVER_USER_GOAL_ENDPOINT, {id: toUpdateID, formDataObject: formData})
      }

      serverPromise.then(
        (result) => {
          debug(currentScriptName, `Saved changes to server:`, result);
          this.setCurrentStateFromData(result)
          this.setState({uploadingChanges: false})

          // Go to list of objects, when done
          window.history.back()
        },
        (error) => {
          warn(currentScriptName, `Error from server saving changes:`, error.message);
          this.setErrorMessage(error.message)
        }
      )
    }
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
          <Col lg={12}>
            {this.state.errorMessage === '' ? null : errorComponent(this.state.errorMessage)}
            <Card>
              <CardHeader>
                <strong>
                  <i className="icon-info pr-1"/>
                  {
                    this.isHandlingNewObject() ? 'New User Goal' : `User Goal ID: ${this.state.objID}`
                  }
                </strong>
                {
                  this.isHandlingNewObject()
                    ? null
                    : <Button color="danger"
                              onClick={this.toggleDeletionModal.bind(this)}
                              className="mr-1 float-right">
                      <i className={"fa fa-trash"}/> Delete
                    </Button>
                }
                <Modal isOpen={this.state.deletionModalOpen} toggle={this.toggleDeletionModal.bind(this)}
                       className={'modal-danger'}>
                  <ModalHeader toggle={this.toggleDeletionModal.bind(this)}>Delete User Goal</ModalHeader>
                  <ModalBody>
                    This will permanently delete the current User Goal from database.
                    <br/>
                    <br/>
                    References to this User Goal will be removed from every data structure in which it is.
                    This possibly includes Exercise Sets and user profiles.
                  </ModalBody>
                  <ModalFooter>
                    <Button color="danger" onClick={this.deleteCurrentFromServer.bind(this)}>Delete</Button>{' '}
                    <Button color="secondary" onClick={this.toggleDeletionModal.bind(this)}>Cancel</Button>
                  </ModalFooter>
                </Modal>
              </CardHeader>
              <CardBody>
                {(() => {
                  const formComponent = (
                    <div>
                      <Form id={this.formID} action="" method="post" encType="multipart/form-data"
                            className="form-horizontal">
                        {
                          [
                            USER_GOAL_TEXT_EN_FIELD_NAME,
                            USER_GOAL_TEXT_IT_FIELD_NAME,
                            USER_GOAL_TEXT_FR_FIELD_NAME,
                            USER_GOAL_TEXT_DE_FIELD_NAME,
                          ].map(field => {
                            const keyHandler = getKeyHandlerFor(field, USER_GOAL_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION)
                            return (
                              <FormGroup row key={field}>
                                <Col md="2">
                                  <Label htmlFor={`textarea-input-${field}`}>{keyHandler.keyPrettyNameLong}</Label>
                                </Col>
                                <Col xs="12" md="10">
                                  <Input type="textarea" rows="2"
                                         name={field}
                                         id={`textarea-input-${field}`}
                                         placeholder={`${keyHandler.keyPrettyNameLong} ...`}
                                         value={this.state[field]}
                                         onChange={e => this.handleTextChange(field, e.target.value)}
                                  />
                                </Col>
                              </FormGroup>
                            )
                          })
                        }
                      </Form>
                      <div className="form-actions float-right">
                        <Button type="submit" color="primary" className={"mr-2"}
                                onClick={() => this.sendChangesToServer(this.isHandlingNewObject())}
                                disabled={this.state.uploadingChanges}
                        >
                          {this.state.uploadingChanges
                            ? <img className='spinner' alt="spinner"
                                   src={require('../../../../assets/img/spinner.gif')}/>
                            : null}
                          {this.isHandlingNewObject() ? 'Insert' : 'Save changes'}
                        </Button>
                        <Link to={"/home/modify/user_goals"}>
                          <Button color="secondary" disabled={this.state.uploadingChanges}>Cancel</Button>
                        </Link>
                      </div>
                    </div>
                  )

                  // To show a loading if fields are not ready to be filled with server data
                  return this.isHandlingNewObject() ? formComponent : showLoadingOrRender(
                    this, this.userGoalData, _ => formComponent, createLoading({})
                  )
                })()}
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    )
  }
}

export default UserGoal;
