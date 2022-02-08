import React, {Component} from "react";
import {Bubble, Line, Scatter} from "react-chartjs-2";
import {ButtonGroup, ButtonToolbar, Card, CardBody, CardHeader} from "reactstrap";
import StaticEventChartWithYLevel from "./StaticEventChartWithYLevel";
import {
  ONE_DAY_IN_MILLIS,
  ONE_MONTH_IN_MILLIS,
  ONE_WEEK_IN_MILLIS,
  ONE_YEAR_IN_MILLIS
} from "../../../../utils/DateUtils";
import createMultiSelectionButton from "../buttons/MultiSelectionButton";
import FullScreen from "react-full-screen";
import {TIME_WINDOW_START} from "../../../../controller/ServerApi";

const EVENT_CHART_TYPE_BUBBLE = "Bubble"
const EVENT_CHART_TYPE_SCATTER = "Scatter"
const EVENT_CHART_TYPE_LINE = "Line"

const EVENT_CHART_TIME_WINDOW_ALL = "All Time"
const EVENT_CHART_TIME_WINDOW_LAST_YEAR = "Last Year"
const EVENT_CHART_TIME_WINDOW_LAST_SIX_MONTHS = "Last 6 Months"
const EVENT_CHART_TIME_WINDOW_LAST_THREE_MONTHS = "Last 3 Months"
const EVENT_CHART_TIME_WINDOW_LAST_MONTH = "Last Month"
const EVENT_CHART_TIME_WINDOW_LAST_WEEK = "Last Week"
const EVENT_CHART_TIME_WINDOW_LAST_DAY = "Last Day"

const DEFAULT_CHART_TYPE = EVENT_CHART_TYPE_LINE;
const DEFAULT_TIME_WINDOW = EVENT_CHART_TIME_WINDOW_ALL;

class CardEventChartWithOptions extends Component {

  /** Object holding mappings between the chart type name and its class */
  chartTypes = {};

  /** Object holding mappings between the chart time window name and a function computing the start time */
  timeWindows = {};

  constructor(props) {
    super(props);

    this.chartTypes[EVENT_CHART_TYPE_BUBBLE] = Bubble
    this.chartTypes[EVENT_CHART_TYPE_SCATTER] = Scatter
    this.chartTypes[EVENT_CHART_TYPE_LINE] = Line

    this.timeWindows[EVENT_CHART_TIME_WINDOW_ALL] = {startTime: () => 0}
    this.timeWindows[EVENT_CHART_TIME_WINDOW_LAST_YEAR] = {startTime: () => Date.now() - ONE_YEAR_IN_MILLIS}
    this.timeWindows[EVENT_CHART_TIME_WINDOW_LAST_SIX_MONTHS] = {startTime: () => Date.now() - (ONE_MONTH_IN_MILLIS * 6)}
    this.timeWindows[EVENT_CHART_TIME_WINDOW_LAST_THREE_MONTHS] = {startTime: () => Date.now() - (ONE_MONTH_IN_MILLIS * 3)}
    this.timeWindows[EVENT_CHART_TIME_WINDOW_LAST_MONTH] = {startTime: () => Date.now() - ONE_MONTH_IN_MILLIS}
    this.timeWindows[EVENT_CHART_TIME_WINDOW_LAST_WEEK] = {startTime: () => Date.now() - ONE_WEEK_IN_MILLIS}
    this.timeWindows[EVENT_CHART_TIME_WINDOW_LAST_DAY] = {startTime: () => Date.now() - ONE_DAY_IN_MILLIS}

    this.state = {
      selectedTimeWindow: props.defaultTimeWindow || DEFAULT_TIME_WINDOW,
      selectedChartType: props.defaultChartType || DEFAULT_CHART_TYPE,

      isFullScreen: false,
    }
  }

  toggleFullScreen = () => {
    this.setState({isFullScreen: !this.state.isFullScreen});
  }

  changeLastTimeWindow(newTimeWindow) {
    this.setState({selectedTimeWindow: newTimeWindow})
  }

  changeChartType(newChartType) {
    this.setState({selectedChartType: newChartType})
  }

  render() {
    const {selectedTimeWindow, selectedChartType} = this.state;

    return (
      <FullScreen enabled={this.state.isFullScreen}>
        <Card className="full-screenable-node">
          <CardHeader>
            <span className="h5"><strong>{this.props.title}</strong> </span>
            <div className="card-header-actions">
              <ButtonToolbar className="float-right" aria-label="Toolbar with chart options button groups">
                <ButtonGroup className="mr-3" aria-label="Time group">
                  {
                    createMultiSelectionButton(this,
                      Object.keys(this.timeWindows),
                      selectedTimeWindow,
                      this.changeLastTimeWindow.bind(this)
                    )
                  }
                </ButtonGroup>
                <ButtonGroup className="mr-3" aria-label="Chart group">
                  {
                    createMultiSelectionButton(this,
                      Object.keys(this.chartTypes),
                      selectedChartType,
                      this.changeChartType.bind(this),
                      3
                    )
                  }
                </ButtonGroup>
                <i className={`${this.state.isFullScreen ? "fa fa-compress" : "fa fa-expand"} ml-3`}
                   onClick={this.toggleFullScreen}/>
              </ButtonToolbar>
            </div>
          </CardHeader>
          <CardBody>
            <StaticEventChartWithYLevel
              apiFunction={this.props.apiFunction}
              apiFunctionParams={(() => {
                let apiParams = this.props.apiFunctionParams ? {...this.props.apiFunctionParams} : {};
                apiParams[TIME_WINDOW_START] = this.timeWindows[selectedTimeWindow].startTime();
                return apiParams;
              })()}
              chartType={this.chartTypes[selectedChartType]}
              yLabelString={"User Level"}
              dataLegend={this.props.dataLegend || this.props.title}
              loading={this.props.loading}/>
          </CardBody>
        </Card>
      </FullScreen>
    );
  }

}

export {
  CardEventChartWithOptions,
  EVENT_CHART_TYPE_BUBBLE,
  EVENT_CHART_TYPE_SCATTER,
  EVENT_CHART_TYPE_LINE,
  EVENT_CHART_TIME_WINDOW_ALL,
  EVENT_CHART_TIME_WINDOW_LAST_YEAR,
  EVENT_CHART_TIME_WINDOW_LAST_SIX_MONTHS,
  EVENT_CHART_TIME_WINDOW_LAST_THREE_MONTHS,
  EVENT_CHART_TIME_WINDOW_LAST_MONTH,
  EVENT_CHART_TIME_WINDOW_LAST_WEEK,
  EVENT_CHART_TIME_WINDOW_LAST_DAY,
}
