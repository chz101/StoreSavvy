import logo from './logo.svg';
import './App.css';
import React, {Component} from 'react';
import {
  Button
} from 'react-native'
import Notifications from 'react-native-notifications'
    
export default class App extends Component {
  state = {
    time: 0,
  };

  componentDidMount() {
    this.interval = setInterval(() => this.setState(prevState => { return {time: prevState.time + 1 } }), 1000);
    //this.interval = setInterval(() => this.setState(prevState => { time: date.getTime() }), 1000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  sendNotification(item, days) {
    Notifications.postLocalNotification({
      body: item + "is about to go bad in " + days + "days!",
      title: "StoreSavvy Alert",
      // sound: "chime.aiff",
      silent: false,
      // category: "SOME_CATEGORY",
      // userInfo: { },
      // fireDate: new Date(),
    });
  }

  render() {
    if (this.state.time > 1 && this.state.time % 10 === 0){
      alert("Apple is about to expire in 3 days!");
      //this.sendNotification("Apple", 3);
    }
    return (
      <div className="App">
        <Button
          title={this.state.time}
          color="#841584"
        />
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
      </div>
    );
  }
}
