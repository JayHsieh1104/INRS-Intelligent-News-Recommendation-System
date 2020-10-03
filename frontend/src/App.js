import React from "react";
import LeftNav from "./components/LeftNav";
import RightNav from "./components/RightNav";
import TopHeadlinesBlock from "./components/TopHeadlinesBlock";
import BusinessNewsBlock from "./components/BusinessNewsBlock";
import SportsNewsBlock from "./components/SportsNewsBlock";
import EntertainmentNewsBlock from "./components/EntertainmentNewsBlock";
import HealthNewsBlock from "./components/HealthNewsBlock";
import ScienceNewsBlock from "./components/ScienceNewsBlock";
import TechnologyNewsBlock from "./components/TechnologyNewsBlock";
import { BrowserRouter as Router, Route } from "react-router-dom";

import "./App.css";

class App extends React.Component {
  render() {
    return (
      <div className="App">
        <Router>
          <div className="LeftNav">
            <LeftNav />
          </div>

          <div className="CentralBlock">
            <Route exact path="/" component={TopHeadlinesBlock} />
            <Route path="/BusinessNews" component={BusinessNewsBlock} />
            <Route path="/SportsNews" component={SportsNewsBlock} />
            <Route
              path="/EntertainmentNews"
              component={EntertainmentNewsBlock}
            />
            <Route path="/HealthNews" component={HealthNewsBlock} />
            <Route path="/ScienceNews" component={ScienceNewsBlock} />
            <Route
              path="/TechnologyNews"
              component={TechnologyNewsBlock}
            />
          </div>
        </Router>

        <div className="RightNav">
        <RightNav />
        </div>
      </div>
    );
  }
}

export default App;
