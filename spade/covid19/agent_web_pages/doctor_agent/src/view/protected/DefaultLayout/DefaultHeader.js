import React, {Component} from 'react';
import {DropdownItem, DropdownMenu, DropdownToggle, Nav, UncontrolledDropdown} from 'reactstrap';
import PropTypes from 'prop-types';

import {AppNavbarBrand, AppSidebarToggler} from '@coreui/react';
import logo from '../../../assets/img/brand/logo.svg'
import sygnet from '../../../assets/img/brand/sygnet.svg'

const propTypes = {
  children: PropTypes.node,
};

const defaultProps = {};

class DefaultHeader extends Component {
  render() {

    // eslint-disable-next-line
    const {children, ...attributes} = this.props;
    const loggedUser = this.props.loggedUser || {};

    return (
      <React.Fragment>
        <AppSidebarToggler className="d-lg-none" display="md" mobile/>
        <AppNavbarBrand
          full={{src: logo, width: 89, height: 25, alt: 'Covid19 Logo'}}
          minimized={{src: sygnet, width: 30, height: 30, alt: 'Covid19 Logo'}}
        />

        <AppSidebarToggler className="d-md-down-none" display="lg"/>

        {/* NOV ITEMS ABOVE MAIN SCREEN WERE REDUNDANT, BUT IF NEEDED RE-ENABLE*/}
        {/*<Nav className="d-md-down-none" navbar>*/}
        {/*  <NavItem className="px-3">*/}
        {/*    <NavLink to="/home/dashboard" className="nav-link" >Dashboard</NavLink>*/}
        {/*  </NavItem>*/}
        {/*  <NavItem className="px-3">*/}
        {/*    <Link to="/home/users" className="nav-link">Users</Link>*/}
        {/*  </NavItem>*/}
        {/*  <NavItem className="px-3">*/}
        {/*    <NavLink to="#" className="nav-link">Settings</NavLink>*/}
        {/*  </NavItem>*/}
        {/*</Nav>*/}
        <Nav className="ml-auto" navbar>
          {/* DISABLED ICONS IN NAVBAR, BECAUSE USELESS FOR NOW*/}
          {/*<NavItem className="d-md-down-none">*/}
          {/*  <NavLink to="#" className="nav-link"><i className="icon-bell"/><Badge pill color="danger">5</Badge></NavLink>*/}
          {/*</NavItem>*/}
          {/*<NavItem className="d-md-down-none">*/}
          {/*  <NavLink to="#" className="nav-link"><i className="icon-list"/></NavLink>*/}
          {/*</NavItem>*/}
          {/*<NavItem className="d-md-down-none">*/}
          {/*  <NavLink to="#" className="nav-link"><i className="icon-location-pin"/></NavLink>*/}
          {/*</NavItem>*/}
          <UncontrolledDropdown nav direction="left">
            <DropdownToggle nav>
              <i className="icon-user px-3"/><span className="pr-5">Doctor</span>
            </DropdownToggle>
            <DropdownMenu right>
              <DropdownItem header tag="div" className="text-center">
                <strong>{(loggedUser.name || "") + " " + (loggedUser.surname || "")}</strong>
                <br/>
                <em>{loggedUser.email || ""}</em>
              </DropdownItem>
              {/* DISABLED UNUSED ACCOUNT DROPDOWN OPTIONS */}
              {/*<DropdownItem><i className="fa fa-bell-o"/> Updates<Badge color="info">42</Badge></DropdownItem>*/}
              {/*<DropdownItem><i className="fa fa-envelope-o"/> Messages<Badge*/}
              {/*  color="success">42</Badge></DropdownItem>*/}
              {/*<DropdownItem><i className="fa fa-tasks"/> Tasks<Badge color="danger">42</Badge></DropdownItem>*/}
              {/*<DropdownItem><i className="fa fa-comments"/> Comments<Badge color="warning">42</Badge></DropdownItem>*/}
              {/*<DropdownItem header tag="div" className="text-center"><strong>Settings</strong></DropdownItem>*/}
              {/*<DropdownItem><i className="fa fa-user"/> Profile</DropdownItem>*/}
              {/*<DropdownItem><i className="fa fa-wrench"/> Settings</DropdownItem>*/}
              {/*<DropdownItem><i className="fa fa-usd"/> Payments<Badge color="secondary">42</Badge></DropdownItem>*/}
              {/*<DropdownItem><i className="fa fa-file"/> Projects<Badge color="primary">42</Badge></DropdownItem>*/}
              {/*<DropdownItem divider/>*/}
              {/*<DropdownItem><i className="fa fa-shield"/> Lock Account</DropdownItem>*/}
              <DropdownItem onClick={e => this.props.onLogout(e)}><i className="fa fa-lock"/> Logout</DropdownItem>
            </DropdownMenu>
          </UncontrolledDropdown>
        </Nav>
        {/* DISABLED TOGGLER FOR ASIDE SINCE DISABLED ASIDE COMPONENT */}
        {/*<AppAsideToggler className="d-md-down-none"/>*/}
        {/*<AppAsideToggler className="d-lg-none" mobile />*/}
      </React.Fragment>
    );
  }
}

DefaultHeader.propTypes = propTypes;
DefaultHeader.defaultProps = defaultProps;

export default DefaultHeader;
