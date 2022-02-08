import {CustomTooltips} from "@coreui/coreui-plugin-chartjs-custom-tooltips";
import {defaults} from "react-chartjs-2";

/**
 * A function to write something over points in charts of Chart.js (namely on Line and Bar charts was tested)
 *
 * It should be called inside the bar chart options object like this way:
 *
 * ```javascript
 * {
 *  ...otherBarChartOptions,
 *  animation: {
 *    duration: 1,
 *    onComplete: function () {
 *      writePercentageOverBarsInChart(this, total)
 *    }
 *  }
 * }
 * ```
 */
function writeInChart(self, total, getStringToWrite) {
  const chartInstance = self.chart, ctx = chartInstance.ctx;
  ctx.font = `${defaults.global.defaultFontSize}, ${defaults.global.defaultFontStyle}, ${defaults.global.defaultFontFamily}`;
  ctx.fillStyle = self.chart.config.options.defaultFontColor;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'bottom';

  self.data.datasets.forEach(function (dataset, i) {
    const meta = chartInstance.controller.getDatasetMeta(i);
    meta.data.forEach(function (bar, index) {
      const label = getStringToWrite(dataset.data[index], total);
      ctx.fillText(label, bar._model.x, bar._model.y - 5);
    });
  });
}

/**
 * A function to write percentages in charts of Chart.js
 *
 * It should be called inside the bar chart options object like this way:
 *
 * ```javascript
 * {
 *  ...otherBarChartOptions,
 *  animation: {
 *    duration: 1,
 *    onComplete: function () {
 *      writePercentagesInChart(this, total)
 *    }
 *  }
 * }
 * ```
 *
 * @param self the chart instance
 * @param total the total value on which the graph is working on (needed to compute partial percentages
 */
function writePercentagesInChart(self, total) {
  writeInChart(self, total, (partial, total) => {
    const percentage = (partial / total) * 100;
    return `${Math.round(percentage * 10) / 10} %`;
  });
}

/**
 * A function to write absolute values in charts of Chart.js
 *
 * It should be called inside the bar chart options object like this way:
 *
 * ```javascript
 * {
 *  ...otherBarChartOptions,
 *  animation: {
 *    duration: 1,
 *    onComplete: function () {
 *      writePercentagesInChart(this, total)
 *    }
 *  }
 * }
 * ```
 *
 * @param self the chart instance
 * @param total the total value on which the graph is working on (needed to compute partial percentages
 */
function writeValuesInChart(self, total) {
  writeInChart(self, total, (partial, _) => `${partial}`);
}

const datasetsBorderColors = [
  'rgba(50, 50, 50, 1)',
  'rgba(0, 128, 255, 1)',
  'rgba(255, 0, 127, 1)',
  'rgba(0, 255, 255, 1)',
  'rgba(0, 255, 128, 1)',
  'rgba(0, 255, 0, 1)',
  'rgba(128, 255, 0, 1)',
  'rgba(255, 255, 0, 1)',
  'rgba(255, 128, 0, 1)',
  'rgba(255, 0, 0, 1)',
  'rgba(255, 0, 255, 1)',
  'rgba(127, 0, 255, 1)',
  'rgba(0, 0, 255, 1)',
]

const datasetsBackgroundColors = [
  'rgba(155, 155, 155, 0.2)',
  'rgba(0, 128, 255, 0.2)',
  'rgba(255, 0, 127, 0.2)',
  'rgba(0, 255, 255, 0.2)',
  'rgba(0, 255, 128, 0.2)',
  'rgba(0, 255, 0, 0.2)',
  'rgba(128, 255, 0, 0.2)',
  'rgba(255, 255, 0, 0.2)',
  'rgba(255, 128, 0, 0.2)',
  'rgba(255, 0, 0, 0.2)',
  'rgba(255, 0, 255, 0.2)',
  'rgba(127, 0, 255, 0.2)',
  'rgba(0, 0, 255, 0.2)',
]

const commonMultipleDimensionChartDataViewSettings = {
  borderWidth: 1,
  // hoverBackgroundColor: datasetsBackgroundColors[0],
  // hoverBorderColor: datasetsBorderColors[0],
}

const commonSingleDimensionChartDataViewSettings = {
  backgroundColor: datasetsBackgroundColors[0],
  borderColor: datasetsBorderColors[0],
  borderWidth: 1,
  hoverBackgroundColor: 'rgba(255, 99, 132, 0.4)',
  hoverBorderColor: 'rgba(255, 99, 132, 1)',
};

const commonChartOptions = {
  tooltips: {
    enabled: false,
    custom: CustomTooltips
  },
  maintainAspectRatio: true,
  legend: {
    position: 'bottom'
  },
  hover: {
    animationDuration: 0
  }
};

export {
  writePercentagesInChart,
  writeValuesInChart,
  datasetsBorderColors,
  datasetsBackgroundColors,
  commonSingleDimensionChartDataViewSettings,
  commonMultipleDimensionChartDataViewSettings,
  commonChartOptions
}
