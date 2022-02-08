import React, {Component} from 'react';
import {
  Button,
  Card,
  CardBody,
  CardHeader,
  Col,
  Form,
  FormGroup,
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
  getAll,
  getSingle,
  postObject,
  SERVER_API_ADDRESS,
  SERVER_EXERCISE_ENDPOINT,
  SERVER_EXERCISE_SET_ENDPOINT,
  SERVER_USER_GOAL_ENDPOINT
} from "../../../../controller/ServerApi";
import {
  createLoading,
  createPartialInitialStateFromFields,
  errorComponent,
  load,
  showLoadingOrRender
} from "../../../../utils/DataLoadingUtils";
import {OBJECT_REFERENCE_ID_FIELD_NAME} from "../../../../model/ModelUtils";
import {Link} from "react-router-dom";
import {debug, log, warn} from "../../../../utils/Logging";
import CardImg from "reactstrap/lib/CardImg";
import './ExerciseSet.css'
import {
  EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME,
  EXERCISE_SET_ID_FIELD_NAME,
  EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME
} from "../../../../model/ExerciseSetFieldNamesDictionaryToDescription";
import MultiSelect from "react-multi-select-component";
import {
  allExercisesIDsToDescription,
  EXERCISE_ID_FIELD_NAME,
  EXERCISE_LABEL_FIELD_NAME,
  EXERCISE_TEXT_EN_FIELD_NAME
} from "../../../../model/ExerciseFieldNamesDictionaryToDescription";
import {
  allGoalsIDsToDescription,
  USER_GOAL_ID_FIELD_NAME,
  USER_GOAL_TEXT_EN_FIELD_NAME
} from "../../../../model/UserGoalFieldNamesDictionaryToDescription";

const currentScriptName = "ExerciseSet.js";

class ExerciseSet extends Component {

  allExercises = "allExercises"
  allUserGoals = "allUserGoals"
  exerciseSetField = "exerciseSet";

  fieldNames = [
    this.exerciseSetField,
    this.allExercises,
    this.allUserGoals,
  ];

  formID = "exercise-set-form"

  constructor(props) {
    super(props);
    this.state = {
      ...(createPartialInitialStateFromFields(this.fieldNames)),
      objID: '',
      [EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME]: [],
      [EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME]: [],
      uploadingChanges: false,
      errorMessage: '',
      deletionModalOpen: false,
    };

    this.setCurrentStateFromData.bind(this);
    this.getCurrentID.bind(this);
    this.handleSelectedEvent.bind(this);
    this.sendChangesToServer.bind(this);
    this.setErrorMessage.bind(this);
    this.toggleDeletionModal.bind(this);
    this.deleteCurrentFromServer.bind(this);

    load(this, this.allExercises, getAll, {serverEndPoint: SERVER_EXERCISE_ENDPOINT})
    load(this, this.allUserGoals, getAll, {serverEndPoint: SERVER_USER_GOAL_ENDPOINT})
    if (!this.isHandlingNewObject()) {
      load(this, this.exerciseSetField, getSingle,
        {serverEndPoint: SERVER_EXERCISE_SET_ENDPOINT, id: this.getCurrentID()},
        (data) => this.setCurrentStateFromData(data)
      );
    }
  }

  setCurrentStateFromData(data) {
    this.setState({
      objID: data[EXERCISE_SET_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME],

      [EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME]:
      data[EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME].map(oid => oid[OBJECT_REFERENCE_ID_FIELD_NAME]) || [],

      [EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME]:
      data[EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME].map(oid => oid[OBJECT_REFERENCE_ID_FIELD_NAME]) || [],
    })
  }

  getCurrentID() {
    return this.props.match.params.id
  }

  isHandlingNewObject() {
    return this.getCurrentID() === "new"
  }

  handleSelectedEvent(field, selectedArray) {
    debug(currentScriptName, `Changed selection for field ${field}: `, selectedArray)

    const selectedIDsArray = selectedArray.map(option => option.value)

    const changedState = {}
    changedState[field] = selectedIDsArray
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
    formData.append(
      EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME,
      JSON.stringify(this.state[EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME])
    )
    formData.append(
      EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME,
      JSON.stringify(this.state[EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME])
    )
    if (formData.get(EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME) === '[]') {
      this.setErrorMessage('Select at least one exercise!')
    } else if (formData.get(EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME) === '[]') {
      this.setErrorMessage('Select at least one goal!')
    } else {
      let serverPromise
      if (insertNew) {
        serverPromise = postObject(ACTION_CREATE, SERVER_EXERCISE_SET_ENDPOINT, {formDataObject: formData})
      } else {
        const toUpdateID = this.getCurrentID()
        serverPromise = postObject(ACTION_MODIFY, SERVER_EXERCISE_SET_ENDPOINT, {
          id: toUpdateID,
          formDataObject: formData
        })
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
    postObject(ACTION_DELETE, SERVER_EXERCISE_SET_ENDPOINT, {id: this.getCurrentID()}).then(
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
                    this.isHandlingNewObject() ? 'New Exercise Set' : `Exercise Set ID: ${this.state.objID}`
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
                  <ModalHeader toggle={this.toggleDeletionModal.bind(this)}>Delete Exercise Set</ModalHeader>
                  <ModalBody>
                    This will permanently delete the current Exercise Set from database.
                    <br/>
                    <br/>
                    References to this Exercise Set will be removed from all Exercise Set Mappings in which it is.
                    User Sport Sessions referencing this Exercise Set will be also removed.
                  </ModalBody>
                  <ModalFooter>
                    <Button color="danger" onClick={this.deleteCurrentFromServer.bind(this)}>Delete</Button>{' '}
                    <Button color="secondary" onClick={this.toggleDeletionModal.bind(this)}>Cancel</Button>
                  </ModalFooter>
                </Modal>
              </CardHeader>
              <CardBody>
                {(() => {
                  const formComponent = showLoadingOrRender(this, this.allExercises,
                    allExercises => showLoadingOrRender(this, this.allUserGoals,
                      allUserGoals => {

                        const goalsPrettyMapping = allGoalsIDsToDescription(allUserGoals)
                        const exercisesPrettyMapping = allExercisesIDsToDescription(allExercises)

                        return (
                          <div>
                            <Form id={this.formID} action="" method="post" encType="multipart/form-data"
                                  className="form-horizontal">
                              <FormGroup row>
                                <Col md="2">
                                  <Label htmlFor={`multiple-select${EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME}`}>
                                    Exercises
                                  </Label>
                                </Col>
                                <Col md="4">
                                  <MultiSelect
                                    options={allExercises.map(exercise => {
                                      return {
                                        label: (
                                          exercise[EXERCISE_LABEL_FIELD_NAME] !== undefined ?
                                            `${exercise[EXERCISE_LABEL_FIELD_NAME]}: ` : ''
                                        ) + exercise[EXERCISE_TEXT_EN_FIELD_NAME],
                                        value: exercise[EXERCISE_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]
                                      }
                                    })}
                                    hasSelectAll={false}
                                    value={
                                      this.state[EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME]
                                        .map(exerciseID => {
                                          return {
                                            label: exercisesPrettyMapping[exerciseID],
                                            value: exerciseID
                                          }
                                        })
                                    }
                                    onChange={currentSelection =>
                                      this.handleSelectedEvent(EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME, currentSelection)
                                    }
                                    labelledBy={"Select"}/>
                                </Col>
                                <Col md="2">
                                  <Label htmlFor={`multiple-select${EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME}`}>
                                    Goals
                                  </Label>
                                </Col>
                                <Col md="4">
                                  <MultiSelect
                                    options={allUserGoals.map(userGoal => {
                                      return {
                                        label: userGoal[USER_GOAL_TEXT_EN_FIELD_NAME],
                                        value: userGoal[USER_GOAL_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]
                                      }
                                    })}
                                    hasSelectAll={false}
                                    value={
                                      this.state[EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME]
                                        .map(userGoalID => {
                                          return {
                                            label: goalsPrettyMapping[userGoalID],
                                            value: userGoalID
                                          }
                                        })
                                    }
                                    onChange={currentSelection =>
                                      this.handleSelectedEvent(EXERCISE_SET_SUITABLE_FOR_GOAL_IDS_FIELD_NAME, currentSelection)
                                    }
                                    labelledBy={"Select"}/>
                                </Col>
                              </FormGroup>
                              <FormGroup row>
                                <Col md="2">
                                  <Label htmlFor="selected-images-preview">Selected Exercises Preview</Label>
                                </Col>
                                <Col xs="12" md="10" id="selected-images-preview">
                                  {
                                    this.state[EXERCISE_SET_EXERCISE_ID_LIST_FIELD_NAME].map(exerciseID => {
                                      return (
                                        <CardImg id={exerciseID} alt={"Exercise Image preview"}
                                                 key={exerciseID}
                                                 src={`${SERVER_API_ADDRESS}${SERVER_EXERCISE_ENDPOINT}/${exerciseID}/gif?random=${performance.now()}`}
                                                 style={{width: "15%"}} className={"mr-3"}
                                        />
                                      )
                                    })
                                  }
                                </Col>
                              </FormGroup>
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
                              <Link to={"/home/modify/exercise_sets"}>
                                <Button color="secondary" disabled={this.state.uploadingChanges}>Cancel</Button>
                              </Link>
                            </div>
                          </div>
                        )
                      },
                      createLoading({})
                    ),
                    createLoading({})
                  )

                  // To show a loading if fields are not ready to be filled with server data
                  return this.isHandlingNewObject() ? formComponent : showLoadingOrRender(
                    this, this.exerciseSetField, _ => formComponent, createLoading({})
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

export default ExerciseSet;
