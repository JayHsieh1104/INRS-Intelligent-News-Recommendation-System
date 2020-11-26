import React from 'react';
import NewsCard from './NewsCard.js';
import './SportsNewsBlock.css';
const config = require("../../config.json");

class SportsNewsBlock extends React.Component {
    constructor(props) {
        super();
        this.state = {
          _error: null,
          _isLoaded: false,
          _articles: null,
        };
      }
    
      fetchNewsData() {
        fetch(config.backend_url_base + "/news/category/sports")
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
        this.fetchNewsData();
      }
    
      render() {
        const { _error, _isLoaded, _articles } = this.state;
        if (_error) {
          return (
            <div className="BlockTitle">
              <p>Sports News</p>
              <div>Error: {_error.message}</div>
            </div>
          );
        } else if (!_isLoaded) {
          return (
            <div className="BlockTitle">
              <p>Sports News</p>
              <div>Loading...</div>
            </div>
          )
        } else {
          return (
            <div>
              <div className="BlockTitle">Sports News</div>
              {_articles.map((_article) => (
                <NewsCard article={_article} />
              ))}
            </div>
          );
        }
      }
    }

export default SportsNewsBlock;