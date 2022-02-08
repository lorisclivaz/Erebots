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
  getAll,
  getSingle,
  postObject,
  SERVER_EXERCISE_ENDPOINT,
  SERVER_EXERCISE_MAPPING_ENDPOINT,
  SERVER_EXERCISE_SET_ENDPOINT,
  SERVER_QUESTION_ENDPOINT
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
import {debug, warn} from "../../../../utils/Logging";
import './ExerciseSetMapping.css'
import {
  EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME,
  EXERCISE_SET_MAPPING_ID_FIELD_NAME,
  EXERCISE_SET_MAPPING_QUESTION_ANSWER_FIELD_NAME,
  EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME,
  EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME
} from "../../../../model/ExerciseSetMappingFieldNamesDictionaryToDescription";
import {
  allQuestionsIDsToDescription,
  QUESTION_ID_FIELD_NAME,
  QUESTION_NEXT_FIELD_NAME,
  QUESTION_PREVIOUS_FIELD_NAME,
  QUESTION_TEXT_EN_FIELD_NAME
} from "../../../../model/QuestionFieldNamesDictionaryToDescription";
import {allExercisesIDsToDescription} from "../../../../model/ExerciseFieldNamesDictionaryToDescription";
import {
  allExerciseSetsIDsToDescription,
  EXERCISE_SET_ID_FIELD_NAME
} from "../../../../model/ExerciseSetFieldNamesDictionaryToDescription";
import MultiSelect from "react-multi-select-component";
import {computeQuestionLevel, sortQuestionObjects} from "../../../../model/QuestionsUtils";
import {
  DIFFICULTY_FIELD_TO_PRETTY_DESCRIPTION,
  SHIFT_FIELD_TO_PRETTY_DESCRIPTION
} from "../../../../model/FieldValuesDictionaryToDescription";
import UncontrolledTooltip from "reactstrap/lib/UncontrolledTooltip";

const currentScriptName = "ExerciseSetMapping.js";

class ExerciseSetMapping extends Component {

  allExercises = "allExercises"
  allQuestions = "allQuestions"
  allExerciseSets = "allExerciseSets"
  exerciseSetMappingField = "exerciseSetMapping";

  fieldNames = [
    this.exerciseSetMappingField,
    this.allExercises,
    this.allQuestions,
    this.allExerciseSets,
  ];

  formID = "exercise-set-mapping-form"

  defaultExerciseSetListValue = []
  defaultQuestionIdValue = ''
  defaultQuestionAnswerValue = ''
  defaultQuestionShiftValue = '-- None --'

  constructor(props) {
    super(props);
    this.state = {
      ...(createPartialInitialStateFromFields(this.fieldNames)),
      objID: '',
      [EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME]: this.defaultExerciseSetListValue,
      [EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME]: this.defaultQuestionIdValue,
      [EXERCISE_SET_MAPPING_QUESTION_ANSWER_FIELD_NAME]: this.defaultQuestionAnswerValue,
      [EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME]: this.defaultQuestionShiftValue,
      uploadingChanges: false,
      errorMessage: '',
      deletionModalOpen: false,
      hasExercisesSelected: undefined
    };

    this.setCurrentStateFromData.bind(this);
    this.getCurrentID.bind(this);
    this.handleSelectedEvent.bind(this);
    this.setHasExercisesSelected.bind(this);
    this.sendChangesToServer.bind(this);
    this.setErrorMessage.bind(this);
    this.toggleDeletionModal.bind(this);
    this.deleteCurrentFromServer.bind(this);

    load(this, this.allExercises, getAll, {serverEndPoint: SERVER_EXERCISE_ENDPOINT})
    load(this, this.allExerciseSets, getAll, {serverEndPoint: SERVER_EXERCISE_SET_ENDPOINT})
    load(this, this.allQuestions, getAll, {serverEndPoint: SERVER_QUESTION_ENDPOINT})
    if (!this.isHandlingNewObject()) {
      load(this, this.exerciseSetMappingField, getSingle,
        {serverEndPoint: SERVER_EXERCISE_MAPPING_ENDPOINT, id: this.getCurrentID()},
        (data) => this.setCurrentStateFromData(data)
      );
    }
  }

  setCurrentStateFromData(data) {
    this.setState({
      objID: data[EXERCISE_SET_MAPPING_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME],

      [EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME]:
      data[EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME].map(oid => oid[OBJECT_REFERENCE_ID_FIELD_NAME])
      || this.defaultExerciseSetListValue,

      [EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME]:
      data[EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME] || this.defaultQuestionIdValue,

      [EXERCISE_SET_MAPPING_QUESTION_ANSWER_FIELD_NAME]:
        data[EXERCISE_SET_MAPPING_QUESTION_ANSWER_FIELD_NAME] === undefined
          ? this.defaultQuestionAnswerValue
          : data[EXERCISE_SET_MAPPING_QUESTION_ANSWER_FIELD_NAME],

      [EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME]:
      data[EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME] || this.defaultQuestionShiftValue,

      hasExercisesSelected: data[EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME] === undefined
    })
  }

  getCurrentID() {
    return this.props.match.params.id
  }

  isHandlingNewObject() {
    return this.getCurrentID() === "new"
  }

  handleSelectedEvent(field, selected) {
    debug(currentScriptName, `Changed selection for field ${field}: `, selected)

    let newField
    if (field === EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME) {
      newField = selected.map(option => option.value)
    } else {
      newField = selected
    }

    const changedState = {}
    changedState[field] = newField
    this.setState(changedState)
  }

  setErrorMessage(errorMessage) {
    this.setState({
      uploadingChanges: false,
      errorMessage: errorMessage
    })
    window.scrollTo(0, 0)
  }

  setHasExercisesSelected(hasExercisesSelected) {
    this.setState({hasExercisesSelected: hasExercisesSelected})
  }

  sendChangesToServer(insertNew = false) {
    debug(currentScriptName, `Called sendChangesToServer with insertNew=${insertNew}`);
    this.setState({
      uploadingChanges: true,
      errorMessage: ''
    })

    const formData = new FormData(document.getElementById(this.formID))
    formData.append(
      EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME,
      JSON.stringify(this.state[EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME])
    )
    if (formData.get(EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME) === this.defaultQuestionIdValue) {
      this.setErrorMessage('Select the question!')
    } else if (formData.get(EXERCISE_SET_MAPPING_QUESTION_ANSWER_FIELD_NAME) === this.defaultQuestionAnswerValue) {
      this.setErrorMessage('Select the question answer!')
    } else if (
      formData.get(EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME) === JSON.stringify(this.defaultExerciseSetListValue)
      && formData.get(EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME) === this.defaultQuestionShiftValue
    ) {
      this.setErrorMessage('Select some exercise sets or the proper question shift!')
    } else {
      let serverPromise
      if (insertNew) {
        serverPromise = postObject(ACTION_CREATE, SERVER_EXERCISE_MAPPING_ENDPOINT, {formDataObject: formData})
      } else {
        const toUpdateID = this.getCurrentID()
        serverPromise = postObject(ACTION_MODIFY, SERVER_EXERCISE_MAPPING_ENDPOINT, {
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
          this.setErrorMessage(error.message + ' -- Be sure to not have duplicated question and answer')
        }
      )
    }
  }

  toggleDeletionModal() {
    this.setState({deletionModalOpen: !this.state.deletionModalOpen})
  }

  deleteCurrentFromServer() {
    postObject(ACTION_DELETE, SERVER_EXERCISE_MAPPING_ENDPOINT, {id: this.getCurrentID()}).then(
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
                    this.isHandlingNewObject() ? 'New Exercise Set Mapping' : `Exercise Set Mapping ID: ${this.state.objID}`
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
                  <ModalHeader toggle={this.toggleDeletionModal.bind(this)}>Delete Exercise Set Mapping</ModalHeader>
                  <ModalBody>
                    This will permanently delete the current Exercise Set Mapping from database.
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
                    allExercises => showLoadingOrRender(this, this.allExerciseSets,
                      allExerciseSets => showLoadingOrRender(this, this.allQuestions,
                        allQuestions => {

                          const questionsPrettyMapping = allQuestionsIDsToDescription(allQuestions)
                          const exercisesPrettyMapping = allExercisesIDsToDescription(allExercises)
                          const exerciseSetsPrettyMapping = allExerciseSetsIDsToDescription(
                            allExerciseSets,
                            exercisesPrettyMapping,
                            ' ► '
                          )

                          return (
                            <div>
                              <Form id={this.formID} action="" method="post" encType="multipart/form-data"
                                    className="form-horizontal">
                                <FormGroup row>
                                  <Col md="2">
                                    <Label htmlFor="select-question">Question</Label>
                                  </Col>
                                  <Col xs="12" md="10">
                                    <Input type="select" name={EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME}
                                           id="select-question"
                                           value={this.state[EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME]}
                                           onChange={e =>
                                             this.handleSelectedEvent(EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME, e.target.value)
                                           }>
                                      <option value={this.defaultQuestionIdValue}>{this.defaultQuestionIdValue}</option>
                                      {
                                        sortQuestionObjects(allQuestions).map((question, index) => {
                                          return (
                                            <option
                                              key={question[QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]}
                                              value={question[QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]}>
                                              Level {index + 1} → {question[QUESTION_TEXT_EN_FIELD_NAME]}
                                            </option>
                                          )
                                        })
                                      }
                                    </Input>
                                  </Col>
                                </FormGroup>
                                <FormGroup row>
                                  <Col md="2">
                                    <Label htmlFor="select-answer">Question Answer</Label>
                                  </Col>
                                  <Col xs="12" md="10">
                                    <Input type="select" name={EXERCISE_SET_MAPPING_QUESTION_ANSWER_FIELD_NAME}
                                           id="select-answer"
                                           value={this.state[EXERCISE_SET_MAPPING_QUESTION_ANSWER_FIELD_NAME]}
                                           onChange={e =>
                                             this.handleSelectedEvent(EXERCISE_SET_MAPPING_QUESTION_ANSWER_FIELD_NAME, e.target.value)
                                           }>
                                      <option value={this.defaultQuestionAnswerValue}>
                                        {this.defaultQuestionAnswerValue}
                                      </option>
                                      {
                                        Object.keys(DIFFICULTY_FIELD_TO_PRETTY_DESCRIPTION).map(difficulty => {
                                          return (
                                            <option key={difficulty} value={difficulty}>
                                              {DIFFICULTY_FIELD_TO_PRETTY_DESCRIPTION[difficulty].longDescription}
                                            </option>
                                          )
                                        })
                                      }
                                    </Input>
                                  </Col>
                                </FormGroup>
                                <FormGroup row>
                                  <Col md="2">
                                    <Label htmlFor={`multi-select-exercise-set`}>
                                      To suggest Exercise Sets
                                    </Label>
                                  </Col>
                                  <Col md="10">
                                    <div id={"multi-select-exercise-set"}>
                                      <MultiSelect
                                        disabled={this.state.hasExercisesSelected === false}
                                        options={allExerciseSets.map(exerciseSet => {
                                          const exerciseSetID = exerciseSet[EXERCISE_SET_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]
                                          return {
                                            label: exerciseSetsPrettyMapping[exerciseSetID],
                                            value: exerciseSetID
                                          }
                                        })}
                                        hasSelectAll={false}
                                        value={
                                          this.state[EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME]
                                            .map(exerciseSetID => {
                                              return {
                                                label: exerciseSetsPrettyMapping[exerciseSetID],
                                                value: exerciseSetID
                                              }
                                            })
                                        }
                                        onChange={currentSelection => {
                                          if (JSON.stringify(currentSelection) === JSON.stringify(this.defaultExerciseSetListValue))
                                            this.setHasExercisesSelected(undefined)
                                          else
                                            this.setHasExercisesSelected(true)

                                          this.handleSelectedEvent(EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME, currentSelection)
                                        }}
                                        labelledBy={"Select"}/>
                                    </div>
                                    {
                                      this.state[EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME] !== this.defaultQuestionShiftValue
                                        ? <UncontrolledTooltip placement="bottom" target="multi-select-exercise-set">
                                          To suggest exercise sets, deselect the question shift
                                        </UncontrolledTooltip>
                                        : null
                                    }
                                  </Col>
                                </FormGroup>
                                <FormGroup row>
                                  <Col md="2">
                                    <Label htmlFor="select-question-shift">Question Shift</Label>
                                  </Col>
                                  <Col xs="12" md="10">
                                    <Input
                                      disabled={this.state.hasExercisesSelected === true}
                                      type="select" name={EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME}
                                      id="select-question-shift"
                                      value={this.state[EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME]}
                                      onChange={e => {
                                        const selectedValue = e.target.value
                                        if (selectedValue === this.defaultQuestionShiftValue)
                                          this.setHasExercisesSelected(undefined)
                                        else
                                          this.setHasExercisesSelected(false)

                                        this.handleSelectedEvent(EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME, selectedValue)
                                      }}>
                                      <option value={this.defaultQuestionShiftValue}>
                                        {this.defaultQuestionShiftValue}
                                      </option>
                                      {
                                        Object.keys(SHIFT_FIELD_TO_PRETTY_DESCRIPTION).map(shift => {
                                          return (
                                            <option key={shift} value={shift}>
                                              {SHIFT_FIELD_TO_PRETTY_DESCRIPTION[shift].longDescription}
                                            </option>
                                          )
                                        })
                                      }
                                    </Input>
                                    {
                                      JSON.stringify(this.state[EXERCISE_SET_MAPPING_EXERCISE_SET_ID_LIST_FIELD_NAME])
                                      !== JSON.stringify(this.defaultExerciseSetListValue)
                                        ? <UncontrolledTooltip placement="bottom" target="select-question-shift">
                                          To make a question shift, deselect suggested exercise sets.
                                        </UncontrolledTooltip>
                                        : null
                                    }
                                  </Col>
                                </FormGroup>
                                {
                                  (
                                    this.state.hasExercisesSelected !== true &&
                                    this.state[EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME] !== this.defaultQuestionShiftValue
                                  ) ? <FormGroup row>
                                      <Col md="2">
                                        <Label>Will shift to</Label>
                                      </Col>
                                      <Col xs="12" md="10">
                                        <p className="form-control-static">
                                          {(() => {
                                            if (this.state[EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME]) {
                                              const questionShift = this.state[EXERCISE_SET_MAPPING_QUESTION_SHIFT_FIELD_NAME]
                                              const currentQuestion = allQuestions.find(question =>
                                                question[QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME] ===
                                                this.state[EXERCISE_SET_MAPPING_QUESTION_ID_FIELD_NAME]
                                              )
                                              if (questionShift.toLowerCase() === QUESTION_NEXT_FIELD_NAME) {
                                                if (currentQuestion[QUESTION_NEXT_FIELD_NAME])
                                                  return `
                                                  Level
                                                  ${computeQuestionLevel(allQuestions, currentQuestion[QUESTION_NEXT_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME])}
                                                  →
                                                  ${
                                                    questionsPrettyMapping[
                                                      currentQuestion[QUESTION_NEXT_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]
                                                      ]
                                                  }`
                                                else
                                                  return "Current main question has no next question, will not shift"
                                              } else {
                                                if (currentQuestion[QUESTION_PREVIOUS_FIELD_NAME])
                                                  return `
                                                  Level
                                                  ${computeQuestionLevel(allQuestions, currentQuestion[QUESTION_PREVIOUS_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME])}
                                                  →
                                                  ${
                                                    questionsPrettyMapping[
                                                      currentQuestion[QUESTION_PREVIOUS_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]
                                                      ]
                                                  }`
                                                else
                                                  return "Current main question has no previous question, will not shift"
                                              }
                                            } else {
                                              return "Select a main question"
                                            }
                                          })()}
                                        </p>
                                      </Col>
                                    </FormGroup>
                                    : null
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
                                <Link to={"/home/modify/exercise_set_mappings"}>
                                  <Button color="secondary" disabled={this.state.uploadingChanges}>Cancel</Button>
                                </Link>
                              </div>
                            </div>
                          )
                        },
                        createLoading({})
                      ),
                      createLoading({})
                    ),
                    createLoading({})
                  )

                  // To show a loading if fields are not ready to be filled with server data
                  return this.isHandlingNewObject() ? formComponent : showLoadingOrRender(
                    this, this.exerciseSetMappingField, _ => formComponent, createLoading({})
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

export default ExerciseSetMapping;
