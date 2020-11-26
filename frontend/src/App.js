import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import LeftNav from "./components/LeftNav";
import RightNav from "./components/RightNav";
import TopHeadlinesBlock from "./components/TopHeadlinesBlock";
import BusinessNewsBlock from "./components/BusinessNewsBlock";
import SportsNewsBlock from "./components/SportsNewsBlock";
import EntertainmentNewsBlock from "./components/EntertainmentNewsBlock";
import HealthNewsBlock from "./components/HealthNewsBlock";
import ScienceNewsBlock from "./components/ScienceNewsBlock";
import TechnologyNewsBlock from "./components/TechnologyNewsBlock";
import SearchResultBlock from "./components/SearchResultBlock";

import "./App.css";

class App extends React.Component {
  constructor(props) {
    super();
    this.state = {
      _searching_keyword: null,
    };
    this.parentFunction = this.parentFunction.bind(this);
  }

  parentFunction = (keyword_from_searchbar) => {
    this.setState({ _searching_keyword: keyword_from_searchbar});
  };

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
            <Route path="/TechnologyNews" component={TechnologyNewsBlock} />
            <Route
              path="/SearchResult"
              render={(props) => (
                <SearchResultBlock {...props} _searching_keyword={this.state._searching_keyword} />
              )}
            />
          </div>
          <div className="RightNav">
            <RightNav functionCallFromParent={this.parentFunction.bind(this)} />
          </div>
        </Router>
      </div>
    );
  }
}

export default App;
