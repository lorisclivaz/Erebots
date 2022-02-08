from echo.common.database.mongo_db_pryv_hybrid.models import PryvStoredData
from common.pryv.api_wrapper import PryvAPI

apiWrapper = PryvAPI("pryv.me")

user_api_endpoint_with_token = "https://YourToken@YourUsername.pryv.me/"

for event in apiWrapper.get_events(
        user_api_endpoint_with_token,
        streams=[stream[0] for stream in PryvStoredData.values()]
):
    apiWrapper.delete_event(user_api_endpoint_with_token, event.id)
