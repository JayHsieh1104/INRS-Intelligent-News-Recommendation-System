import React from "react";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import FormControl from "react-bootstrap/FormControl";

class RightNav extends React.Component {
  constructor(props) {
    super();
    this.state = {
      _error: null,
      _isLoaded: false,
      _stockData: null,
    };
    this.fetchStockData = this.fetchStockData.bind(this);
  }

  fetchStockData() {
    fetch(
      "https://financialmodelingprep.com/api/v3/quote/%5EGSPC,%5EDJI,%5EIXIC?apikey=9dec6fb1a002e2de5ca62d2775bf26e9"
    )
      .then((res) => res.json())
      .then(
        (jsonObj) => {
          this.setState({
            _isLoaded: true,
            _stockData: jsonObj,
          });
        },
        (error) => {
          this.setState({
            _isLoaded: true,
            _stockData: error,
          });
        }
      );
  }

  componentDidMount() {
    this.fetchStockData();
  }

  render() {
    const { _error, _isLoaded, _stockData } = this.state;
    if (_error) {
      return (
        <div>
          <h3>Looking for certain news?</h3>
          <Form inline style={{ marginBottom: "10px" }}>
            <FormControl
              type="text"
              placeholder="Search for topics"
              className="mr-sm-2"
            />
            <Button variant="outline-primary">Search</Button>
          </Form>
          <Card>
            <Card.Header as="h5">Stock</Card.Header>
            <Card.Body>
              <Card.Text>Error: {_error.message}</Card.Text>
            </Card.Body>
          </Card>
        </div>
      );
    } else if (!_isLoaded) {
      return (
        <div>
          <h3>Looking for certain news?</h3>
          <Form inline style={{ marginBottom: "10px" }}>
            <FormControl
              type="text"
              placeholder="Search for topics"
              className="mr-sm-2"
            />
            <Button variant="outline-primary">Search</Button>
          </Form>
          <Card>
            <Card.Header as="h5">Stock</Card.Header>
            <Card.Body>
              <Card.Text>Loading...</Card.Text>
            </Card.Body>
          </Card>
        </div>
      );
    } else {
      let unix_timestamp = _stockData[0].timestamp;
      // Create a new JavaScript Date object based on the timestamp
      // multiplied by 1000 so that the argument is in milliseconds, not seconds.
      var date = new Date(unix_timestamp * 1000);
      // Hours part from the timestamp
      var hours = date.getHours();
      // Minutes part from the timestamp
      var minutes = "0" + date.getMinutes();
      // Seconds part from the timestamp
      var seconds = "0" + date.getSeconds();

      // Will display time in 10:30:23 format
      var formattedTime =
        hours + ":" + minutes.substr(-2) + ":" + seconds.substr(-2);
      return (
        <div>
          <h3>Looking for certain news?</h3>
          <Form inline style={{ marginBottom: "10px" }}>
            <FormControl
              type="text"
              placeholder="Search for topics"
              className="mr-sm-2"
            />
            <Button variant="outline-primary">Search</Button>
          </Form>
          <Card>
            <Card.Header as="h5">Market Indexes</Card.Header>
            <Card.Body>
              <Card.Text>Updated time: {formattedTime}</Card.Text>
              <Card.Title>Dow Jones</Card.Title>
              <Card.Text>
                • {_stockData[0].price} / {_stockData[0].change}{" "} / {_stockData[0].changesPercentage} %
              </Card.Text>
              <Card.Title>S&P 500</Card.Title>
              <Card.Text>
                • {_stockData[1].price} / {_stockData[1].change}{" "} / {_stockData[1].changesPercentage}%
              </Card.Text>
              <Card.Title>NASDAQ</Card.Title>
              <Card.Text>
                • {_stockData[2].price} / {_stockData[2].change}{" "} / {_stockData[2].changesPercentage}%
              </Card.Text>
            </Card.Body>
            <Card.Header as="h5">
              <Button onClick={this.fetchStockData} variant="primary">
                Update
              </Button>
            </Card.Header>
          </Card>
        </div>
      );
    }
  }
}

export default RightNav;
