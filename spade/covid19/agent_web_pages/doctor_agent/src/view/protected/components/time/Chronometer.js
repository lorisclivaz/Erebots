import React, {Component} from "react";
import {millisToDurationString} from "../../../../utils/TimeDurationUtils";
import {convertToUTCMillis} from "../../../../model/DatetimeExtractor";

// const currentScriptName = "Chronometer.js"

export default class Chronometer extends Component {

  constructor(props) {
    super(props);

    this.state = {currentDate: new Date()}
  }

  componentDidMount() {
    this.timerID = setInterval(
      () => this.tick(),
      1000
    );
  }

  componentWillUnmount() {
    clearInterval(this.timerID);
  }

  tick() {
    this.setState({currentDate: new Date()});
  }

  render() {
    // console.log(lastSmokeEventDate)
    // console.log(lastSmokeEventDate.getTime())
    // console.log(lastSmokeEventDate.getTimezoneOffset())
    // console.log(lastSmokeEventDate.getTimezoneOffset()*60*1000)
    // console.log(lastSmokeEventDate.getTime() + lastSmokeEventDate.getTimezoneOffset()*60*1000)
    // console.log(new Date())
    // console.log(Date.now())
    const elapsedTimeTillNow = this.state.currentDate - convertToUTCMillis(this.props.fromDate);
    // debug(currentScriptName, `Elapsed time millis from fromDate: ${elapsedTimeTillNow}`);
    return <div className="text-value">{millisToDurationString(elapsedTimeTillNow)}</div>
  }

}
