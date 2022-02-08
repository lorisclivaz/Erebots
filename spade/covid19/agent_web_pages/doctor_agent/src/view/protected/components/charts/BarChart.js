import React, {Component} from 'react';
import * as d3 from "d3";

class BarChart extends Component {
  componentDidMount() {
    this.drawChart();
  }

  drawChart() {
    const data = this.props.data;

    const svg = d3.select("#" + this.props.id).append("svg")
      .attr("width", 700)
      .attr("height", 500);

    svg.selectAll("rect")
      .data(data)
      .enter()
      .append("rect")
      .attr("x", (d, i) => i * 70)
      .attr("y", (d, i) => 500 - 10 * d)
      .attr("width", 65)
      .attr("height", (d, i) => d * 10)
      .attr("fill", "green")

    svg.selectAll("text")
      .data(data)
      .enter()
      .append("text")
      .text((d) => d)
      .attr("x", (d, i) => i * 70)
      .attr("y", (d, i) => 500 - (10 * d) - 3)

//selection.attr(“property”, (d, i) => {})
  }

  render(){
    return  <div id={"#" + this.props.id}/>
  }

}

export default BarChart;
