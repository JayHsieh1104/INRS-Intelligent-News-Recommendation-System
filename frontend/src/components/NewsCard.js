import React from "react";
import RelatedNewsCard from "./RelatedNewsCard.js";
import "./NewsCard.css";

class NewsCard extends React.Component {
  constructor(props) {
    super();
    this.state = {};
  }

  render() {
    const related_articles = JSON.parse(this.props.article.related_articles);
    let article_author = this.props.article.author;
    if (article_author !== null && article_author !== "") {
      article_author = this.props.article.author + " - ";
    }
    return (
      <div className="NewsCard">
        <div className="MainNews">
          <div className="MainNewsContent">
            <a href={this.props.article.url} className="MainNewsTitle">
              {this.props.article.title}
            </a>
            <div className="MainNewsSourceAuthorDate">
              Posted by {article_author} {this.props.article.source}
            </div>
            <div className="MainNewsSourceAuthorDate">
              Updated {this.props.article.published_date.substring(11, 16)}, {this.props.article.published_date.substring(0, 10)}
            </div>
            <img
              className="MainNewsImg"
              src={this.props.article.url_image}
              alt="News pic"
            ></img>
            <div className="MainNewsText">
              {this.props.article.content} <a href={this.props.article.url}>Read More</a>
            </div>
          </div>
        </div>
        <div className="RelatedNews">
          <p className="recommendedNewsTitle">
            You may be also interested in...
          </p>
          {related_articles.map((_article) => (
            <RelatedNewsCard article={_article} />
          ))}
        </div>
      </div>
    );
  }
}

export default NewsCard;
