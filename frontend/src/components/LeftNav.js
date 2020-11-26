import React from "react";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import Link from "react-router-dom/Link";
import "./LeftNav.css";

class LeftNav extends React.Component {
  render() {
    return (
      <div>
        <Navbar
          style={{ borderRadius: "10px" }}
          bg="light"
          className="flex-column"
        >
          <Navbar.Brand href="/">
            <img
              style={{ height: "100px" }}
              alt="News img"
              src={require("../images/Logo_no_background_black_news.png")}
            />
          </Navbar.Brand>
          <Nav style={{ fontSize: "20px"  }} className="mr-auto, flex-column">
            <Nav.Link style={{ borderBottom: "2px grey dotted" }} as={Link} to="/">
              Top Stories
            </Nav.Link>
            <Nav.Link style={{ borderBottom: "2px grey dotted" }} as={Link} to="/BusinessNews">
              Business
            </Nav.Link>
            <Nav.Link style={{ borderBottom: "2px grey dotted" }} as={Link} to="/EntertainmentNews">
              Entertainment
            </Nav.Link>
            <Nav.Link style={{ borderBottom: "2px grey dotted" }} as={Link} to="/HealthNews">
              Health
            </Nav.Link>
            <Nav.Link style={{ borderBottom: "2px grey dotted" }} as={Link} to="/ScienceNews">
              Science
            </Nav.Link>
            <Nav.Link style={{ borderBottom: "2px grey dotted" }} as={Link} to="/SportsNews">
              Sports
            </Nav.Link>
            <Nav.Link as={Link} to="/TechnologyNews">
              Technology
            </Nav.Link>
          </Nav>
        </Navbar>
      </div>
    );
  }
}

export default LeftNav;
