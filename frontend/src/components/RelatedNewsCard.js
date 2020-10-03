import React from "react";
import "./RelatedNewsCard.css";

class RelatedNewsCard extends React.Component {
  constructor(props) {
    super();
    this.state = {
    };
  }

  render() {
    return (
      <div className="RelatedNewsCard">
        <div className="RelatedNewsContent">
          <a href={this.props.article.url} className="RelatedNewsTitle">
          • {this.props.article.title}
          </a>
          <div className="RelatedNewsSourceDate">
            {this.props.article.source} - {this.props.article.publishedAt.substring(0, 10)}
          </div>
        </div>
      </div>
    );
  }
}

export default RelatedNewsCard;
