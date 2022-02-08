import React, {Component} from "react";
import {ButtonToolbar, Card, CardBody, CardHeader} from "reactstrap";
import StaticAggregationChartWithValues from "./StaticAggregationChartWithValues";
import {Bar, Line, Radar} from "react-chartjs-2";
import {writePercentagesInChart, writeValuesInChart} from "../../../../utils/ChartJsUtils";
import ButtonGroup from "reactstrap/es/ButtonGroup";
import createMultiSelectionButton from "../buttons/MultiSelectionButton";
import {PROFILE_AVAILABLE_AGGREGATION_FIELDS} from "../../../../model/ProfileFieldNamesDictionaryToHandlers";
import Button from "reactstrap/es/Button";
import {
  AGGREGATE_BY_PROFILE_DIM_1_FIELD_QUERY_PARAMETER,
  AGGREGATE_BY_PROFILE_DIM_2_FIELD_QUERY_PARAMETER
} from "../../../../controller/ServerApi";
import FullScreen from "react-full-screen";
import {MONTH_ARTIFICIAL_FIELD_NAME, WEEKDAY_ARTIFICIAL_FIELD_NAME} from "../../../../model/ModelUtils";
import {prettifyFieldName} from "../../../../model/FieldPrettifyHandler";

const NONE_DIMENSION_SELECTED_NAME = 'None'

const DEFAULT_NO_SORT_FIELDS = [
  WEEKDAY_ARTIFICIAL_FIELD_NAME,
  MONTH_ARTIFICIAL_FIELD_NAME,
];

const AGGREGATION_CHART_TYPE_BAR = "Bar"
const AGGREGATION_CHART_TYPE_LINE = "Line"
const AGGREGATION_CHART_TYPE_RADAR = "Radar"

const CHART_SHOW_VALUES_PERCENTAGE = "Percentage"
const CHART_SHOW_VALUES_ABSOLUTE = "Absolute"
const CHART_SHOW_VALUES_HIDE = "Hide values"

const DEFAULT_CHART_TYPE = AGGREGATION_CHART_TYPE_BAR;
const DEFAULT_SHOWN_VALUE = CHART_SHOW_VALUES_PERCENTAGE;

class CardAggregationChartWithOptions extends Component {

  /** Object holding mappings between the chart type name and its class */
  chartTypes = {}

  /** Object holding mappings between the chart show values name and its computation function */
  showValues = {};

  constructor(props) {
    super(props);

    this.chartTypes[AGGREGATION_CHART_TYPE_BAR] = Bar
    this.chartTypes[AGGREGATION_CHART_TYPE_LINE] = Line
    this.chartTypes[AGGREGATION_CHART_TYPE_RADAR] = Radar

    this.showValues[CHART_SHOW_VALUES_PERCENTAGE] = writePercentagesInChart
    this.showValues[CHART_SHOW_VALUES_ABSOLUTE] = writeValuesInChart
    this.showValues[CHART_SHOW_VALUES_HIDE] = (_1, _2) => ''

    this.state = {
      selectedAggregationField1: props.defaultAggregationField1 || props.firstDimensionAggregationFields[0],
      selectedAggregationField2: props.defaultAggregationField2 || NONE_DIMENSION_SELECTED_NAME,
      selectedChartType: props.defaultChartType || DEFAULT_CHART_TYPE,
      selectedShowValues: props.defaultShowValues || DEFAULT_SHOWN_VALUE,

      isFullScreen: false,
    }
  }

  toggleFullScreen = () => {
    this.setState({isFullScreen: !this.state.isFullScreen});
  }

  changeAggregationField1(newAggregationField) {
    this.setState({selectedAggregationField1: newAggregationField})
  }

  changeAggregationField2(newAggregationField) {
    this.setState({selectedAggregationField2: newAggregationField})
  }

  changeChartType(newChartType) {
    this.setState({selectedChartType: newChartType})
    if (newChartType === AGGREGATION_CHART_TYPE_BAR)
      this.changeShowValues(CHART_SHOW_VALUES_PERCENTAGE)
    else if (newChartType === AGGREGATION_CHART_TYPE_LINE)
      this.changeShowValues(CHART_SHOW_VALUES_ABSOLUTE)
    else if (newChartType === AGGREGATION_CHART_TYPE_RADAR)
      this.changeShowValues(CHART_SHOW_VALUES_HIDE)
  }

  changeShowValues(newShowValues) {
    this.setState({selectedShowValues: newShowValues})
  }

  render() {
    const {selectedAggregationField1, selectedAggregationField2, selectedChartType, selectedShowValues,} = this.state;
    return (
      <FullScreen enabled={this.state.isFullScreen}>
        <Card className="full-screenable-node">
          <CardHeader>
            <span className="h5"><strong>{this.props.title}</strong></span>

            <div className="card-header-actions">
              <ButtonToolbar className="float-right" aria-label="Toolbar with chart options button groups">
                <ButtonGroup vertical className="mr-2" aria-label="Aggregation selection group">
                  <Button disabled className="btn-light">1° Dimension</Button>
                  {
                    createMultiSelectionButton(this,
                      this.props.firstDimensionAggregationFields.filter(field => field !== selectedAggregationField2),
                      selectedAggregationField1,
                      this.changeAggregationField1.bind(this),
                      2,
                      text => prettifyFieldName(text, true),
                      "firstDimension"
                    )
                  }
                </ButtonGroup>
                <ButtonGroup vertical className="mr-3" aria-label="Aggregation selection group">
                  <Button disabled className="btn-light">2° Dimension</Button>
                  {
                    createMultiSelectionButton(this,
                      [NONE_DIMENSION_SELECTED_NAME, ...(this.props.secondDimensionAggregationFields.filter(field => field !== selectedAggregationField1))],
                      selectedAggregationField2,
                      this.changeAggregationField2.bind(this),
                      2,
                      text => prettifyFieldName(text, true),
                      "secondDimension"
                    )
                  }
                </ButtonGroup>
                <ButtonGroup vertical className="" aria-label="Chart group">
                  {
                    createMultiSelectionButton(this,
                      Object.keys(this.chartTypes),
                      selectedChartType,
                      this.changeChartType.bind(this),
                    )
                  }
                  {
                    createMultiSelectionButton(this,
                      Object.keys(this.showValues),
                      selectedShowValues,
                      this.changeShowValues.bind(this)
                    )
                  }
                </ButtonGroup>
                <i className={`${this.state.isFullScreen ? "fa fa-compress" : "fa fa-expand"} ml-3`}
                   onClick={this.toggleFullScreen}/>
              </ButtonToolbar>
            </div>
          </CardHeader>
          <CardBody>
            <StaticAggregationChartWithValues
              apiFunction={this.props.apiFunction}
              apiFunctionParams={(() => {
                let apiParams = this.props.apiFunctionParams ? {...this.props.apiFunctionParams} : {};
                if (PROFILE_AVAILABLE_AGGREGATION_FIELDS.includes(selectedAggregationField1))
                  apiParams[AGGREGATE_BY_PROFILE_DIM_1_FIELD_QUERY_PARAMETER] = selectedAggregationField1;

                if (PROFILE_AVAILABLE_AGGREGATION_FIELDS.includes(selectedAggregationField2))
                  apiParams[AGGREGATE_BY_PROFILE_DIM_2_FIELD_QUERY_PARAMETER] = selectedAggregationField2;

                return apiParams;
              })()}
              chartType={this.chartTypes[selectedChartType]}
              writeDataValuesInGraph={this.showValues[selectedShowValues]}
              sortDataLabelsDim1={!DEFAULT_NO_SORT_FIELDS.includes(selectedAggregationField1)}
              sortDataLabelsDim2={!DEFAULT_NO_SORT_FIELDS.includes(selectedAggregationField2)}
              singleDimensionDataLegend={this.props.singleDimensionDataLegend || this.props.title}
              loading={this.props.loading}
              firstDimSpecificMapping={this.props.specificMappingsForFields}
              secondDimSpecificMapping={this.props.specificMappingsForFields}
            />

          </CardBody>
        </Card>
      </FullScreen>
    );
  }

}

export {
  CardAggregationChartWithOptions,
  AGGREGATION_CHART_TYPE_BAR,
  AGGREGATION_CHART_TYPE_LINE,
  AGGREGATION_CHART_TYPE_RADAR,
  CHART_SHOW_VALUES_PERCENTAGE,
  CHART_SHOW_VALUES_ABSOLUTE,
  CHART_SHOW_VALUES_HIDE,
}
