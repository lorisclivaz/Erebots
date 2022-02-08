import React, {Component} from "react";
import {
  createLoading,
  createPartialInitialStateFromFields,
  load,
  noDataAvailableComponent,
  showLoadingOrRender
} from "../../../../utils/DataLoadingUtils";
import {debug} from "../../../../utils/Logging";
import {Bar} from "react-chartjs-2";

const currentScriptName = "MyBaseStaticChart.js";

const FIELD_CHART_DATA = 'chartData';
const FIELD_CHART_OPTIONS = 'chartOptions';

class MyBaseStaticChart extends Component {

  chartDataField = "chartData";

  constructor(props) {
    super(props);

    this.loadData.bind(this);

    this.state = {
      ...(createPartialInitialStateFromFields([this.chartDataField])),
    };
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (JSON.stringify(prevProps.apiFunctionParams) !== JSON.stringify(this.props.apiFunctionParams)) {
      debug(currentScriptName, "Component should refresh the graph");
      debug(currentScriptName, "oldProps", prevProps);
      debug(currentScriptName, "newProps", this.props);

      this.setState({
        ...(createPartialInitialStateFromFields([this.chartDataField]))
      }, () => this.loadData());
    }
  }

  componentDidMount() {
    this.loadData()
  }

  loadData() {
    load(this, this.chartDataField, this.props.apiFunction, this.props.apiFunctionParams)
  }

  render() {
    return showLoadingOrRender(this, this.chartDataField,
      (data) => {
        if ((Array.isArray(data) && data.length) || Object.keys(data).length) {
          const chartDataAndOptionsObj = this.props.dataManipulationLogic(data);
          const chartData = chartDataAndOptionsObj[FIELD_CHART_DATA];
          const chartOptions = chartDataAndOptionsObj[FIELD_CHART_OPTIONS];
          const ChartType = this.props.chartType || Bar;
          return (
            <div className="chart-wrapper">
              <ChartType data={chartData} options={chartOptions}/>
            </div>
          );
        } else return noDataAvailableComponent()
      },
      this.props.loading ? this.props.loading({}) : createLoading({pt: 3, position: 'center'})
    )
  }
}

export {MyBaseStaticChart, FIELD_CHART_DATA, FIELD_CHART_OPTIONS}
