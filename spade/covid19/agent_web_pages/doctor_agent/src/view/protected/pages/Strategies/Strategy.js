import React, {useState, Component} from 'react';
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
  SERVER_STRATEGY_ENDPOINT
} from "../../../../controller/ServerApi";
import {
  createLoading,
  createPartialInitialStateFromFields,
  errorComponent,
  load,
  showLoadingOrRender
} from "../../../../utils/DataLoadingUtils";
import {OBJECT_REFERENCE_ID_FIELD_NAME} from "../../../../model/ModelUtils";
import {getKeyHandlerFor} from "../../../../model/FieldPrettifyHandler";
import {Link} from "react-router-dom";
import {debug, log, warn} from "../../../../utils/Logging";
import './Strategy.css'
import {
  STRATEGY_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  STRATEGY_ID_FIELD_NAME,
  STRATEGY_NAME_FIELD_NAME,
  STRATEGY_DESCRIPTION_FIELD_NAME
} from "../../../../model/StrategyFieldNamesDictionaryToDescription";
import {USER_GOAL_ID_FIELD_NAME} from "../../../../model/UserGoalFieldNamesDictionaryToDescription";

const currentScriptName = "Strategy.js";

class Strategy extends Component {

  strategyDataField = "strategyData";

  fieldNames = [
    this.strategyDataField,
  ];

  formID = "strategy-form"

  constructor(props) {
    super(props);
    this.state = {
      ...(createPartialInitialStateFromFields(this.fieldNames)),
      objID: '',
      [STRATEGY_NAME_FIELD_NAME]: '',
      [STRATEGY_DESCRIPTION_FIELD_NAME]: '',
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
      load(this, this.strategyDataField, getSingle,
        {serverEndPoint: SERVER_STRATEGY_ENDPOINT, id: this.getCurrentID()},
        (data) => this.setCurrentStateFromData(data)
      );
    }

    this.data2 = [12, 5, 6, 6, 9, 10]
  }

  setCurrentStateFromData(data) {
    this.setState({
      objID: data[STRATEGY_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME],
      [STRATEGY_NAME_FIELD_NAME]: data[STRATEGY_NAME_FIELD_NAME],
      [STRATEGY_DESCRIPTION_FIELD_NAME]: data[STRATEGY_DESCRIPTION_FIELD_NAME] || ''
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
    if (!formData.get(STRATEGY_NAME_FIELD_NAME)) {
      this.setErrorMessage('A name for the strategy is mandatory!')
    } else {
      let serverPromise
      if (insertNew) {
        serverPromise = postObject(ACTION_CREATE, SERVER_STRATEGY_ENDPOINT, {formDataObject: formData})
      } else {
        const toUpdateID = this.getCurrentID()
        serverPromise = postObject(ACTION_MODIFY, SERVER_STRATEGY_ENDPOINT, {id: toUpdateID, formDataObject: formData})
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
    postObject(ACTION_DELETE, SERVER_STRATEGY_ENDPOINT, {id: this.getCurrentID()}).then(
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
                    this.isHandlingNewObject() ? 'New Strategy' : `Strategy ID: ${this.state.objID}`
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
                  <ModalHeader toggle={this.toggleDeletionModal.bind(this)}>Delete Strategy</ModalHeader>
                  <ModalBody>
                    This will permanently delete the current Strategy from database.
                    <br/>
                    <br/>
                    References to this Strategy will be removed from every data structure in which it is.
                    This means that every Exercise Set Mapping of this question will be also deleted and
                    all users at this question level will not have a level anymore. Consider modifying questions
                    instead of deleting and inserting them again.
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
                            STRATEGY_NAME_FIELD_NAME,
                            STRATEGY_DESCRIPTION_FIELD_NAME,
                          ].map(field => {
                            const keyHandler = getKeyHandlerFor(field, STRATEGY_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION)
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
                        <hr/>
                        <div className="container-fluid">
                          <div className="row">
                            <div className="col-8 border-right">
                              Graph...
                            </div>
                            <div className="col-4 border">
                              <div className="row m-2 mr-0">
                                <div className="col-md-10">
                                  <h2>Start</h2>
                                </div>
                                <div className="col-2 p-0">
                                  <div className="float-right">
                                    <Button color={'primary'} className="btn btn-default btn-circle btn-xl mr-1">
                                      <i className={"fa fa-save icons font-1xl d-block"}/>
                                    </Button>
                                    <Button color={'success'} className="btn btn-default btn-circle btn-xl mr-1">
                                      <i className="fa fa-plus icons font-1xl d-block"/>
                                    </Button>
                                    <Button color="danger" className="btn btn-default btn-circle btn-xl">
                                      <i className={"fa fa-trash icons font-1xl d-block"}/>
                                    </Button>
                                  </div>
                                </div>
                              </div>
                              <hr/>
                              <div className="row m-2 mt-3">
                                <div className="col-12">
                                  <div className="form-group row">
                                    <h4 className="col-3">Action</h4>
                                    <select className="col-9" aria-label="Action selection" defaultValue="0">
                                      <option value="0">Select Action Type</option>
                                      <option value="1">1</option>
                                      <option value="2">2</option>
                                      <option value="3">3</option>
                                    </select>
                                  </div>
                                </div>
                              </div>
                              <hr/>
                              <div className="row m-2 mt-3">
                                <div className="col-12">
                                  <div className="form-group row">
                                    <h4 className="col-3">Transition</h4>
                                    <select className="col-9" aria-label="Action selection" defaultValue="0">
                                      <option value="0">Select Transition Type</option>
                                      <option value="1">1</option>
                                      <option value="2">2</option>
                                      <option value="3">3</option>
                                    </select>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </Form>
                      <hr/>
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
                        <Link to={"/home/modify/strategies"}>
                          <Button color="secondary" disabled={this.state.uploadingChanges}>Cancel</Button>
                        </Link>
                      </div>
                    </div>
                  )

                  // To show a loading if fields are not ready to be filled with server data
                  return this.isHandlingNewObject() ? formComponent : showLoadingOrRender(
                    this, this.strategyDataField, _ => formComponent, createLoading({})
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

export default Strategy;
