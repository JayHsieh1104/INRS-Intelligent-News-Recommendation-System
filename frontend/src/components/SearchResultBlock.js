import React from "react";
import NewsCard from "./NewsCard.js";

import "./SearchResultBlock.css";
const config = require("../../config.json");

class SearchResultBlock extends React.Component {
  constructor(props) {
    super();
    this.state = {
      _error: null,
      _isLoaded: false,
      _articles: null
    };
  }

  fetchNewsData(_searching_keyword) {
    fetch(config.backend_url_base + "/news/keyword/" + _searching_keyword)
      .then((res) => res.json())
      .then(
        (jsonObj) => {
          this.setState({
            _isLoaded: true,
            _articles: jsonObj,
          });
        },
        (error) => {
          this.setState({
            _isLoaded: true,
            _error: error,
          });
        }
      );
  }

  componentDidMount() {
    this.fetchNewsData(this.props._searching_keyword);
  }

  componentDidUpdate(prevProps) {
    if (this.props._searching_keyword !== prevProps._searching_keyword) {
      this.fetchNewsData(this.props._searching_keyword);
    }
  }

  render() {
    const { _error, _isLoaded, _articles } = this.state;
    if (_error) {
      return (
        <div className="BlockTitle">
          <p>Search for news related to "{this.props._searching_keyword}"</p>
          <div>Error: {_error.message}</div>
        </div>
      );
    } else if (!_isLoaded) {
      return (
        <div className="BlockTitle">
          <p>Search for news related to "{this.props._searching_keyword}"</p>
          <div>Loading...</div>
        </div>
      );
    } else {
      return (
        <div>
          <div className="BlockTitle">
            Search for news related to "{this.props._searching_keyword}"
          </div>
          {_articles.map((_article) => (
            <NewsCard article={_article} />
          ))}
        </div>
      );
    }
  }
}

export default SearchResultBlock;
