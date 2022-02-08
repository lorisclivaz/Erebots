import React, {Component} from "react";
import {
  commonChartOptions,
  commonMultipleDimensionChartDataViewSettings,
  commonSingleDimensionChartDataViewSettings,
  datasetsBackgroundColors,
  datasetsBorderColors
} from "../../../../utils/ChartJsUtils";
import {FIELD_CHART_DATA, FIELD_CHART_OPTIONS, MyBaseStaticChart} from "./MyBaseStaticChart";
import {upperFirstChar} from "../../../../utils/StringUtils";
import {Radar} from "react-chartjs-2";
import {
  AGGREGATE_BY_PROFILE_DIM_1_FIELD_QUERY_PARAMETER,
  AGGREGATE_BY_PROFILE_DIM_2_FIELD_QUERY_PARAMETER
} from "../../../../controller/ServerApi";
import {debug} from "../../../../utils/Logging";
import {getKeyHandlerFor} from "../../../../model/FieldPrettifyHandler";

const currentScriptName = "StaticAggregationChartWithValues.js"

export default class StaticAggregationChartWithValues extends Component {

  render() {
    return <MyBaseStaticChart

      apiFunction={this.props.apiFunction}
      apiFunctionParams={this.props.apiFunctionParams}
      chartType={this.props.chartType}
      loading={this.props.loading}

      dataManipulationLogic={data => {
        debug(currentScriptName, `Entering data manipulation logic with:`, data)
        const firstDimension = this.props.apiFunctionParams[AGGREGATE_BY_PROFILE_DIM_1_FIELD_QUERY_PARAMETER];
        debug(currentScriptName, `first dimension is:`, firstDimension)
        const secondDimension = this.props.apiFunctionParams[AGGREGATE_BY_PROFILE_DIM_2_FIELD_QUERY_PARAMETER] || null;
        debug(currentScriptName, `second dimension is:`, secondDimension)

        const twoDimensionalGraph = secondDimension !== null
        debug(currentScriptName, `Its a two dimensional graph:`, twoDimensionalGraph)

        const firstDimensionHandler = getKeyHandlerFor(firstDimension, this.props.firstDimSpecificMapping)
        const secondDimensionHandler = getKeyHandlerFor(secondDimension, this.props.secondDimSpecificMapping)

        let firstDimDataLabels;
        if (firstDimensionHandler.rawValuesToDescriptionMap !== undefined) {
          // if present use the ordering given, by our data model
          firstDimDataLabels = Object.keys(firstDimensionHandler.rawValuesToDescriptionMap)
          debug(currentScriptName, `Our data model has a proper ordering for first dimension values: `, firstDimDataLabels)
          // adding non predefined present labels at the end
          const notPresentLabels = Object.keys(data).filter(key => !firstDimDataLabels.includes(key))
          debug(currentScriptName, `But there could be also non present labels to be added: `, notPresentLabels)
          firstDimDataLabels = firstDimDataLabels.concat(notPresentLabels)
          debug(currentScriptName, `Concatenation result is: `, firstDimDataLabels)
        } else {
          // if not present a predefined key ordering, take the labels from the server data
          firstDimDataLabels = Object.keys(data);
          debug(currentScriptName, `We don't have a predefined ordering according to our data model for first dimension values,
           these are labels taken from received server data:`, firstDimDataLabels)
          // sort alphabetically only if requested
          if (this.props.sortDataLabelsDim1 || this.props.sortDataLabelsDim1 === undefined)
            firstDimDataLabels = firstDimDataLabels.sort();
        }

        let secondDimDataLabels;
        if (twoDimensionalGraph && secondDimensionHandler.rawValuesToDescriptionMap !== undefined) {
          // if present use the ordering given, by our data model
          secondDimDataLabels = Object.keys(secondDimensionHandler.rawValuesToDescriptionMap)
          debug(currentScriptName, `Our data model has a proper ordering for second dimension values: `, secondDimDataLabels)
          // adding non predefined present labels at the end
          let notPresentLabels = new Set()
          Object.values(data).forEach(subAggregationObj => {
            if (!Array.isArray(subAggregationObj))
              Object.keys(subAggregationObj)
                .filter(secondDimKey => !secondDimDataLabels.includes(secondDimKey))
                .forEach(secondDimensionDataLabel => notPresentLabels.add(secondDimensionDataLabel))
          })
          debug(currentScriptName, `But there could be also non present labels to be added: `, notPresentLabels)
          secondDimDataLabels = secondDimDataLabels.concat([...notPresentLabels])
          debug(currentScriptName, `Concatenation result is: `, secondDimDataLabels)
        } else if (twoDimensionalGraph) {
          // if not present a predefined key ordering, take the labels from the server data
          secondDimDataLabels = new Set()
          Object.values(data).forEach(subAggregationObj => {
            if (!Array.isArray(subAggregationObj))
              Object.keys(subAggregationObj)
                .forEach(secondDimensionDataLabel => secondDimDataLabels.add(secondDimensionDataLabel))
          })
          secondDimDataLabels = [...secondDimDataLabels];
          debug(currentScriptName, `We don't have a predefined ordering according to our data model for second dimension values,
           these are labels taken from received server data:`, secondDimDataLabels)
          // sort alphabetically only if requested
          if (this.props.sortDataLabelsDim2 || this.props.sortDataLabelsDim2 === undefined)
            secondDimDataLabels = secondDimDataLabels.sort();
        }

        debug(currentScriptName, `Now lets count the total of data and the max value`)
        let totalGraphDataCount = 0;
        let maxCount = 0;
        firstDimDataLabels.forEach(firstDimKey => {
          if (data[firstDimKey] !== undefined) {
            if (twoDimensionalGraph) {
              secondDimDataLabels.forEach(secondDimKey => {
                if (data[firstDimKey][secondDimKey] !== undefined) {
                  totalGraphDataCount += data[firstDimKey][secondDimKey].length;
                  if (maxCount < data[firstDimKey][secondDimKey].length)
                    maxCount = data[firstDimKey][secondDimKey].length
                }
              })
            } else {
              totalGraphDataCount += data[firstDimKey].length;
              if (maxCount < data[firstDimKey].length)
                maxCount = data[firstDimKey].length
            }
          }
        });
        debug(currentScriptName, `Computed data total count is '${totalGraphDataCount}' and Max Value is '${maxCount}'`)

        const chartData = {
          labels: firstDimDataLabels.map(firstDimKey =>
            firstDimKey === 'uncatalogued'
              ? upperFirstChar(firstDimKey)
              : firstDimensionHandler.valuePrettifier(firstDimKey, true, false)
          ),
          datasets: twoDimensionalGraph
            ? secondDimDataLabels.map((secondDimKey, keyIndex) => {
              return {
                ...commonMultipleDimensionChartDataViewSettings,
                label: secondDimKey === 'uncatalogued'
                  ? upperFirstChar(secondDimKey)
                  : secondDimensionHandler.valuePrettifier(secondDimKey, true, false),
                data: firstDimDataLabels.map(firstDimKey => {
                  if (data[firstDimKey] !== undefined && data[firstDimKey][secondDimKey])
                    return data[firstDimKey][secondDimKey].length
                  else
                    return 0
                }),
                backgroundColor: datasetsBackgroundColors[keyIndex + 1],
                borderColor: datasetsBorderColors[keyIndex + 1],
              }
            })
            : [{
              ...commonSingleDimensionChartDataViewSettings,
              label: this.props.singleDimensionDataLegend,
              data: firstDimDataLabels.map(key => {
                if (data[key] !== undefined) return data[key].length
                else return 0
              }),
            }]
        };
        debug(currentScriptName, `Computed Chart Data`)

        const writeDataValuesInGraphFunction = this.props.writeDataValuesInGraph;
        const chartOptions = {
          ...commonChartOptions,
          animation: {
            duration: 1,
            onComplete: function () {
              writeDataValuesInGraphFunction(this, totalGraphDataCount);
            }
          },
          scales: {
            yAxes: [{
              display: this.props.chartType !== Radar,
              ticks: {
                beginAtZero: true,
                suggestedMax: maxCount + maxCount / 10
              }
            }]
          }
        };
        debug(currentScriptName, `Computed Chart Options`)

        let toReturn = {};
        toReturn[FIELD_CHART_DATA] = chartData;
        toReturn[FIELD_CHART_OPTIONS] = chartOptions;
        return toReturn;
      }}/>;
  }
}
