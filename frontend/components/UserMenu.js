import React, { Component, PropTypes } from 'react';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group';
import { Link } from 'react-router';

export default class UserMenu extends Component {
  constructor(props) {
    super(props);

    this.state = { showDropdown: false };
    this.onToggleDropdown = this.onToggleDropdown.bind(this);
  }

  onToggleDropdown() {
    this.setState({ showDropdown: !this.state.showDropdown });
  }

  render() {
    return (
      <div className="UserMenu pull-right dropdown-wrapper">
        {this.props.isAuthenticated ?
          <span onClick={this.onToggleDropdown}>
            {`${this.props.firstName || ''} ${this.props.lastName || ''}`}
          </span>
        :
          <span>
            <Link to="">Login</Link>
          </span>
        }

        <div className="dropdown">
          <ReactCSSTransitionGroup
            appear={this.state.showDropdown}
            transitionName="dropdown"
            transitionEnterTimeout={300}
            transitionLeaveTimeout={300}
          >
          {this.state.showDropdown &&
            <div key={0} className="dropdown-inner">
              <Link to="/me" onClick={this.onToggleDropdown}>View profile</Link>
              {this.props.isStaff && <a href="/admin/">Admin</a>}
              <a href="/logout/" onClick={this.onToggleDropdown}>Logout</a>
            </div>
          }
          </ReactCSSTransitionGroup>
        </div>
      </div>
    );
  }
}

UserMenu.propTypes = {
  firstName: PropTypes.string,
  lastName: PropTypes.string,
  isStaff: PropTypes.bool,
  isAuthenticated: PropTypes.bool,
};
