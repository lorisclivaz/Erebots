import React, {Component} from 'react';
import {Card, CardBody, CardHeader, Col, Row} from 'reactstrap';
import {getAll, SERVER_USER_ENDPOINT} from "../../../../controller/ServerApi";
import {
  createLoading,
  createPartialInitialStateFromFields,
  load,
  noDataAvailableComponent,
  showLoadingOrRender
} from "../../../../utils/DataLoadingUtils";
import {convertToUTCMillis, extractDateObject} from "../../../../model/DatetimeExtractor";
import {
  USER_FIRST_NAME_FIELD_NAME,
  USER_ID_FIELD_NAME,
  USER_LANGUAGE_FIELD_NAME,
  USER_LAST_INTERACTION_FIELD_NAME,
  USER_SEX_FIELD_NAME
} from "../../../../model/ProfileFieldNamesDictionaryToHandlers";
import DataTable from "react-data-table-component";
import {ONE_DAY_IN_MILLIS} from "../../../../utils/DateUtils";
import Badge from "reactstrap/es/Badge";
import {Link} from "react-router-dom";
import './Users.css'
import {OBJECT_REFERENCE_ID_FIELD_NAME} from "../../../../model/ModelUtils";
import {getKeyHandlerFor, prettifyFieldName} from "../../../../model/FieldPrettifyHandler";

// const currentScriptName = "Users.js";


/** Function to compute users status */
const computeUserStatus = user =>
  Date.now() - convertToUTCMillis(extractDateObject(user[USER_LAST_INTERACTION_FIELD_NAME])) > ONE_DAY_IN_MILLIS * 3
    ? "Inactive"
    : "Active"

/** Function to get color badge from user status */
const getBadgeColorFromStatus = status => {
  return status === 'Active' ? 'success' :
    status === 'Inactive' ? 'secondary' :
      status === 'Pending' ? 'warning' :
        status === 'Banned' ? 'danger' :
          'primary';
}

const getUserLink = userID => `/home/users/${userID}`;

class Users extends Component {

  allUsersField = "allUsers";
  fieldNames = [this.allUsersField];

  constructor(props) {
    super(props);
    this.state = {
      ...(createPartialInitialStateFromFields(this.fieldNames)),

    }
  }

  componentDidMount() {
    load(this, this.allUsersField, getAll, {serverEndPoint: SERVER_USER_ENDPOINT});
  }


  render() {
    return (
      <div className="animated fadeIn">
        <Row>
          <Col xl={12}>
            <Card>
              <CardHeader>
                <i className="fa fa-align-justify"/> Users
              </CardHeader>
              <CardBody>
                {
                  showLoadingOrRender(this, this.allUsersField,
                    allUsers => {
                      const shownProfileFields = [
                        USER_ID_FIELD_NAME,
                        USER_FIRST_NAME_FIELD_NAME,
                        USER_LANGUAGE_FIELD_NAME,
                        USER_SEX_FIELD_NAME,
                        "Status",
                        USER_LAST_INTERACTION_FIELD_NAME,
                      ];

                      const getColumnWidthProportion = columnName => {
                        if ([USER_ID_FIELD_NAME].includes(columnName))
                          return "8"; // largest
                        else if ([USER_LAST_INTERACTION_FIELD_NAME].includes(columnName))
                          return "6"; // medium
                        else if ([USER_LANGUAGE_FIELD_NAME, USER_SEX_FIELD_NAME, 'Status'].includes(columnName))
                          return "1" // smallest
                        else return "4" // normal
                      }

                      const dataColumns = shownProfileFields.map(profileField => {
                        return {
                          name: prettifyFieldName(profileField, true),
                          sortable: true,
                          grow: getColumnWidthProportion(profileField),
                          // center:true,

                          // callback to produce data to be sorted
                          selector: user => {
                            if (profileField === 'Status')
                              return computeUserStatus(user)
                            else if (profileField === USER_LAST_INTERACTION_FIELD_NAME)
                              return convertToUTCMillis(extractDateObject(user[profileField]));
                            else
                              return getKeyHandlerFor(profileField).valuePrettifier(user[profileField], true, false);
                          },

                          // callback to produce views to be shown
                          format: user => {
                            if (profileField === 'Status') {
                              const userStatus = computeUserStatus(user)
                              return <Badge color={getBadgeColorFromStatus(userStatus)}>{userStatus}</Badge>
                            } else if ([USER_FIRST_NAME_FIELD_NAME].includes(profileField))
                              return (
                                <Link to={getUserLink(user[USER_ID_FIELD_NAME][OBJECT_REFERENCE_ID_FIELD_NAME])}>
                                  <span className="font-weight-bold">
                                    {getKeyHandlerFor(profileField).valuePrettifier(user[profileField])}
                                  </span>
                                </Link>
                              )
                            else
                              return getKeyHandlerFor(profileField).valuePrettifier(user[profileField], true, true)
                          },
                        }
                      })

                      return <DataTable noHeader={true}
                                        columns={dataColumns}
                                        data={allUsers}
                                        keyField={`${USER_ID_FIELD_NAME}.${OBJECT_REFERENCE_ID_FIELD_NAME}`}
                                        striped={true}
                                        highlightOnHover={true}
                                        noDataComponent={noDataAvailableComponent()}
                                        dense={true} // enable if wanted more compact rows
                                        pagination={true}
                                        paginationPerPage={10}
                                        paginationRowsPerPageOptions={[5, 10, 20, 50, 100, 200, 500]}
                                        className={"users-table"}
                      />
                    },
                    createLoading({})
                  )
                }
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    )
  }
}

export default Users;
