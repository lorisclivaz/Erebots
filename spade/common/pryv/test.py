from time import sleep

from common.pryv.api_wrapper import PryvAPI
from common.pryv.model import DataAccessPermission, AccessLevel
from common.pryv.server_domain import PRYV_SERVER_DOMAIN, PRYV_PROJECT_ID

# TODO 09/11/2020: remove this file, when pryv migration completed

apiWrapper = PryvAPI(PRYV_SERVER_DOMAIN)

print(apiWrapper.service_info)
print(apiWrapper.service_info.access)

permission1 = DataAccessPermission({})
permission1.stream_id = 'age-range'
permission1.default_name = 'Age Range Test'
permission1.level = AccessLevel.MANAGE

permission2 = DataAccessPermission({})
permission2.stream_id = 'name-surname'
permission2.default_name = 'Name and Surname Test'
permission2.level = AccessLevel.MANAGE

auth_response = apiWrapper.request_auth(PRYV_PROJECT_ID, [permission1, permission2])
print(auth_response)
print(auth_response.auth_url)

sleep(15)

poll_response = apiWrapper.fetch_poll_url(auth_response)
print(poll_response)

created_event = apiWrapper.create_event(poll_response.pryv_api_endpoint, [permission1.stream_id], "test content2")
print(created_event)

last_1_event = apiWrapper.get_events(poll_response.pryv_api_endpoint, streams=[permission1.stream_id], limit=1)
print(last_1_event[0])

access_info = apiWrapper.get_access_info(poll_response.pryv_api_endpoint)
print(access_info)
print([p.to_json_string() for p in access_info.permissions])
