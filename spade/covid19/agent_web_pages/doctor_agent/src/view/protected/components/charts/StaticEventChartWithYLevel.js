import React, {Component} from "react";
import {FIELD_CHART_DATA, FIELD_CHART_OPTIONS, MyBaseStaticChart} from "./MyBaseStaticChart";
import {convertToLocalMillis} from "../../../../model/DatetimeExtractor";
import {commonChartOptions, commonSingleDimensionChartDataViewSettings} from "../../../../utils/ChartJsUtils";
import {dateToPrettyString} from "../../../../utils/DateUtils";

const TIMESTAMP_FIELD = 'timestamp';
const LEVEL_FIELD = 'level';

export default class StaticEventChartWithYLevel extends Component {
  render() {
    return <MyBaseStaticChart

      apiFunction={this.props.apiFunction}
      apiFunctionParams={this.props.apiFunctionParams}
      chartType={this.props.chartType}
      loading={this.props.loading}

      dataManipulationLogic={(data) => {
        let xyData = data.map(timestamp_level_pair => {
          const dateObj = new Date(timestamp_level_pair[TIMESTAMP_FIELD] * 1000);
          return {x: convertToLocalMillis(dateObj), y: timestamp_level_pair[LEVEL_FIELD]}
        });

        xyData = xyData.sort((xy1, xy2) => xy1.x - xy2.x);

        const dataLegend = this.props.dataLegend;
        const chartData = {
          labels: xyData.map(xy => xy.x),
          datasets: [{
            ...commonSingleDimensionChartDataViewSettings,
            label: dataLegend,
            data: xyData
          }]
        };
        const chartOptions = {
          ...commonChartOptions,
          tooltips: {
            enabled: true,
            callbacks: {
              title: function (tooltipItem, _data) {
                // console.log(tooltipItem)
                return dateToPrettyString(tooltipItem[0].xLabel);
              },
              label: function (tooltipItem, _data) {
                // console.log(tooltipItem)
                return `Level ${tooltipItem.yLabel.toFixed(1)}`
              }
            }
          },
          scales: {
            yAxes: [{
              scaleLabel: {
                display: true,
                labelString: this.props.yLabelString,
              },
              ticks: {
                stepSize: 0.1
              }
            }],
            xAxes: [{
              ticks: {
                autoSkip: false,
                callback: function (value, _index, _values) {
                  return dateToPrettyString(value, false);
                }
              }
            }]
          }
        };

        let toReturn = {};
        toReturn[FIELD_CHART_DATA] = chartData;
        toReturn[FIELD_CHART_OPTIONS] = chartOptions;
        return toReturn;
      }}
    />
  }
}
