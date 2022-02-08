import React, {Component} from 'react';
import {Button, Card, CardBody, CardFooter, CardHeader, Col, Form, FormGroup, Label, Row} from 'reactstrap';
import {ACTION_MODIFY, getAll, postObject, SERVER_QUESTION_ENDPOINT} from "../../../../controller/ServerApi";
import {
  createLoading,
  createPartialInitialStateFromFields,
  load,
  showLoadingOrRender
} from "../../../../utils/DataLoadingUtils";
import {
  QUESTION_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION,
  QUESTION_ID_FIELD_NAME,
  QUESTION_NEXT_FIELD_NAME,
  QUESTION_PREVIOUS_FIELD_NAME,
  QUESTION_TEXT_DE_FIELD_NAME,
  QUESTION_TEXT_EN_FIELD_NAME,
  QUESTION_TEXT_FR_FIELD_NAME,
  QUESTION_TEXT_IT_FIELD_NAME
} from "../../../../model/QuestionFieldNamesDictionaryToDescription";
import {OBJECT_REFERENCE_ID_FIELD_NAME} from "../../../../model/ModelUtils";
import DraggableList from "react-draggable-list";
import {getKeyHandlerFor} from "../../../../model/FieldPrettifyHandler";
import {computeQuestionLevel, sortQuestionObjects} from "../../../../model/QuestionsUtils";
import {Link} from "react-router-dom";
import {debug, log, warn} from "../../../../utils/Logging";
import './QuestionsReorder.css'

const currentScriptName = "QuestionsReorder.js";

class QuestionItem extends Component {

  // This is used internally by the library DraggableList
  // noinspection JSUnusedGlobalSymbols
  getDragHeight() {
    return 32 // The height of other items during dragging
  }

  shouldComponentUpdate(nextProps, nextState, nextContext) {
    return this.props.commonProps.hiddenDetails !== nextProps.commonProps.hiddenDetails ||
      this.props.commonProps.originalQuestions.length !== nextProps.commonProps.originalQuestions.length ||
      this.props.item[QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME] !== nextProps.item[QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME] ||
      this.props.itemSelected !== nextProps.itemSelected
  }

  render() {
    const {item, itemSelected, dragHandleProps} = this.props;
    // const {value} = this.state;
    const scale = itemSelected * 0.05 + 1;
    const shadow = itemSelected * 15 + 1;
    const dragged = itemSelected !== 0;

    return (
      <div className={'item' + dragged ? ' dragged' : ''}
           style={{
             backgroundColor: 'white',
             transform: `scale(${scale})`,
             boxShadow: `rgba(0, 0, 0, 0.3) 0px ${shadow}px ${2 * shadow}px 0px`
           }}>
        <div className="dragHandle" {...dragHandleProps} >
          <Card>
            <CardHeader>
              <b>
                {'Level '}
                {computeQuestionLevel(this.props.commonProps.originalQuestions, item[QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME])}
                {' → '}
                {item[QUESTION_TEXT_EN_FIELD_NAME]}
              </b>
            </CardHeader>
            <CardBody hidden={itemSelected > 0.4 || this.props.commonProps.hiddenDetails}>
              <Form className="form-horizontal">
                {
                  [
                    QUESTION_TEXT_IT_FIELD_NAME,
                    QUESTION_TEXT_FR_FIELD_NAME,
                    QUESTION_TEXT_DE_FIELD_NAME,
                  ].map(field => {
                    const keyHandler = getKeyHandlerFor(field, QUESTION_FIELD_NAME_TO_PRETTY_DESCRIPTION_FUNCTION)
                    return (
                      <FormGroup row key={field}>
                        <Col md="2">
                          <Label><i>{keyHandler.keyPrettyNameLong}:</i></Label>
                        </Col>
                        <Col xs="12" md="10">
                          <p className="form-control-static">
                            {
                              item[field] || (
                                <span className={'text-muted'}>
                                  {`${keyHandler.keyPrettyNameLong} ...`}
                                </span>
                              )
                            }
                          </p>
                        </Col>
                      </FormGroup>
                    )
                  })
                }
              </Form>
            </CardBody>
          </Card>
        </div>
      </div>
    );
  }
}

class QuestionsReorder extends Component {

  allQuestions = "allQuestions";
  fieldNames = [this.allQuestions];

  constructor(props) {
    super(props);
    this.state = {
      ...(createPartialInitialStateFromFields(this.fieldNames)),
      draggableList: [],
      hiddenDetails: true,
      uploadingChanges: false,
      errorMessage: '',
    }

    this.onListChange.bind(this)
  }

  componentDidMount() {
    load(this, this.allQuestions, getAll,
      {serverEndPoint: SERVER_QUESTION_ENDPOINT},
      questions => this.onListChange(sortQuestionObjects(questions))
    );
  }

  onListChange(newList) {
    this.setState({draggableList: newList})
  }

  toggleHiddenDetails() {
    this.setState({hiddenDetails: !this.state.hiddenDetails})
  }

  setErrorMessage(errorMessage) {
    this.setState({
      uploadingChanges: false,
      errorMessage: errorMessage
    })
    window.scrollTo(0, 0)
  }

  sendChangesToServer() {
    log(currentScriptName, `Called sendChangesToServer`, this.state.draggableList);
    this.setState({
      uploadingChanges: true,
      errorMessage: ''
    })

    const originalQuestions = sortQuestionObjects(this.state[`${this.allQuestions}Data`])
    if (originalQuestions === undefined)
      warn(currentScriptName, "Hardcoded access to generic field is no more updated... change the line above")

    // Check for ordering changes
    const orderChanged = originalQuestions.some((question, index) => {
      return (
        question[QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]
        !== this.state.draggableList[index][QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]
      )
    })
    debug(currentScriptName, "Will actually send changes to server? ", orderChanged)

    if (orderChanged) {
      const serverPromises = this.state.draggableList.map((question, index, allReorderedQuestions) => {
        const formData = new FormData()
        formData.append(QUESTION_TEXT_EN_FIELD_NAME, question[QUESTION_TEXT_EN_FIELD_NAME])
        formData.append(QUESTION_TEXT_IT_FIELD_NAME, question[QUESTION_TEXT_IT_FIELD_NAME])
        formData.append(QUESTION_TEXT_FR_FIELD_NAME, question[QUESTION_TEXT_FR_FIELD_NAME])
        formData.append(QUESTION_TEXT_DE_FIELD_NAME, question[QUESTION_TEXT_DE_FIELD_NAME])

        formData.append(
          QUESTION_NEXT_FIELD_NAME,
          allReorderedQuestions[index + 1] === undefined
            ? ''
            : allReorderedQuestions[index + 1][QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]
        )
        formData.append(
          QUESTION_PREVIOUS_FIELD_NAME,
          allReorderedQuestions[index - 1] === undefined
            ? ''
            : allReorderedQuestions[index - 1][QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]
        )

        const toUpdateID = question[QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]
        return postObject(ACTION_MODIFY, SERVER_QUESTION_ENDPOINT, {
          id: toUpdateID,
          formDataObject: formData
        })
      })

      Promise.all(serverPromises).then(
        (result) => {
          debug(currentScriptName, `Saved changes to server:`, result);
          this.setState({uploadingChanges: false})

          // Go to list of objects, when done
          window.history.back()
        },
        (error) => {
          warn(currentScriptName, `Error from server saving changes:`, error.message);
          this.setErrorMessage(error.message)
        }
      )
    } else {
      this.setState({uploadingChanges: false})

      // Go to list of objects, when done
      window.history.back()
    }
  }

  render() {
    return (
      <div className="animated fadeIn">
        <Row>
          <Col xl={12}>
            <Card>
              <CardHeader>
                <i className="fa fa-align-justify"/> Questions <span className={"text-muted"}>(drag to reorder)</span>
                <div className="card-header-actions">
                  <Button size={'sm'} color={'secondary'} onClick={this.toggleHiddenDetails.bind(this)}>
                    <i className={"fa fa-list mr-2"}/>
                    {this.state.hiddenDetails ? "Show " : "Hide "}
                    Details
                  </Button>
                </div>
              </CardHeader>
              <CardBody>
                {
                  showLoadingOrRender(this, this.allQuestions,
                    allQuestions => {
                      return (
                        <DraggableList
                          list={this.state.draggableList}
                          itemKey={obj => obj[QUESTION_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME]}
                          template={QuestionItem}
                          onMoveEnd={newList => this.onListChange(newList)}
                          container={() => document.body}
                          commonProps={{
                            hiddenDetails: this.state.hiddenDetails,
                            originalQuestions: allQuestions
                          }}
                        />
                      )
                    },
                    createLoading({})
                  )
                }
              </CardBody>
              <CardFooter>
                <div className={'float-right'}>
                  <Button type="submit" color="primary" className={"mr-2"}
                          onClick={() => this.sendChangesToServer()}
                          disabled={this.state.uploadingChanges}
                  >
                    {this.state.uploadingChanges
                      ? <img className='spinner' alt="spinner"
                             src={require('../../../../assets/img/spinner.gif')}/>
                      : null}
                    Save changes
                  </Button>
                  <Link to={"/home/modify/questions"}>
                    <Button color="secondary" disabled={this.state.uploadingChanges}>Cancel</Button>
                  </Link>
                </div>
              </CardFooter>
            </Card>
          </Col>
        </Row>
      </div>
    )
  }
}

export default QuestionsReorder;
