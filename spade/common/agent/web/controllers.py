import datetime
import json
import logging
import os
from types import coroutine
from typing import List, Callable, Mapping, Any, Tuple, Awaitable, Union, Optional, TypeVar

from aiohttp.web_exceptions import HTTPFound, HTTPNotFound
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from common.agent.web.mime_type_utils import get_mime_type_from_extension
from common.data_analysis.aggregation import aggregate_objects_by_field
from common.database.abstract_dao import AbstractDAO
from common.database.cache.abstract_cache_dao import AbstractCacheDAO
from common.database.cache.factory import CacheDataFactory
from common.database.cache.model.abstract_cache_data import AbstractCacheData

logger = logging.getLogger(__name__)

CORS_HEADER = {"Access-Control-Allow-Origin": "*"}
"""The header used to allow requests from other hostname, w.r.t. the hostname where the web page is hosted"""


def create_redirection_controller_to(web_path: str) -> coroutine:
    """Function which returns a controller that redirects to the provided path, raising an HTTPFound exception"""

    async def redirect(request: Request):
        """Coroutine which raises an HTTPFound exception"""
        logger.info(f"Redirecting `{request.path}` to `{web_path}`")
        raise HTTPFound(web_path, headers=CORS_HEADER)

    return redirect


def create_static_file_controller(file_path: str) -> coroutine:
    """Factory to create a controller which always returns the provided file, without watching inside the Request"""

    async def static_file_controller(_: Request):
        """Coroutine which returns a predefined raw file in response"""

        norm_path = os.path.normpath(file_path)
        try:
            with open(norm_path, "rb") as file:
                return Response(body=file.read(), content_type=get_mime_type_from_extension(norm_path))
        except FileNotFoundError:
            raise HTTPNotFound(reason=f"File not found: `{norm_path}`", headers=CORS_HEADER)

    return static_file_controller


async def create_json_response(json_data: Union[str, dict, list], custom_headers: Optional[dict] = None):
    """Utility function to create a Response with provided json body"""

    if custom_headers:
        headers = {
            **custom_headers,
            **CORS_HEADER
        }
    else:
        headers = CORS_HEADER

    if isinstance(json_data, dict) or isinstance(json_data, list):
        return Response(body=json.dumps(json_data), headers=headers, content_type="application/json")
    elif isinstance(json_data, str):
        return Response(body=json_data, headers=headers, content_type="application/json")
    else:
        logger.warning(f" Sending a response with non json nor string payload; actual payload: {str(json_data)}")
        return Response(body=str(json_data), headers=headers, content_type="text/plain")


T1 = TypeVar('T1')
T2 = TypeVar('T2')


async def handle_paginated_request(
        request: Request,
        all_items: List[T1],
        item_pre_processing_function: Callable[[T1], Mapping[str, Any]]
):
    """Utility function to handle paginated requests; returns the Json object to be sent"""

    logger.info(f" Request `{request.rel_url}` paginated with params: `{[it for it in request.query.items()]}`")

    object_pagination_start_index = "start"
    object_pagination_end_index = "end"

    max_index = len(all_items)
    client_start_index = request.query.get(object_pagination_start_index, "0")
    client_start_index = int(client_start_index) if client_start_index else 0

    client_end_index = request.query.get(object_pagination_end_index, str(max_index))
    client_end_index = int(client_end_index) if client_end_index else max_index

    (start_index, end_index) = get_normalized_start_and_end(0, max_index, client_start_index, client_end_index)
    json_body = [item_pre_processing_function(item) for item in all_items[start_index:end_index]]

    return json_body


async def handle_time_windowed_request(
        request: Request,
        all_items: List[T1],
        item_timestamp_getter: Callable[[T1], int],
        item_pre_processing_function: Callable[[T1], T2] = lambda x: x
) -> List[T2]:
    """Utility function to handle time windowed requests; returns the Json objects to be sent"""

    logger.info(f" Request `{request.rel_url}` windowed with parameters `{[it for it in request.query.items()]}`")

    (start_time, end_time) = await get_request_time_window(request)

    json_body = [item_pre_processing_function(item) for item in all_items
                 if start_time < item_timestamp_getter(item) < end_time]

    logger.info(f" {len(json_body)} elements over {len(all_items)} 'survived' the time_window "
                f"'{start_time}-{end_time}' "
                f"[{str(datetime.datetime.fromtimestamp(start_time / 1000.0))} - "
                f"{str(datetime.datetime.fromtimestamp(end_time / 1000.0))}]")

    return json_body


event_time_window_from_query_name = "from_date"
event_time_window_to_query_name = "to_date"


async def get_request_time_window(
        request: Request,
        default_min_timestamp: int = 0,
        default_max_timestamp: int = int((datetime.datetime.now() + datetime.timedelta(days=1)).timestamp() * 1000)
) -> Tuple[int, int]:
    """
    Utility function to retrieve time window params from request, or default with provided values

    Returns the Tuple[int,int] of extracted (or default) values for time window in milliseconds
    """

    client_start_time = request.query.get(event_time_window_from_query_name, str(default_min_timestamp))
    client_start_time = int(float(client_start_time)) if client_start_time else default_min_timestamp

    client_end_time = request.query.get(event_time_window_to_query_name, str(default_max_timestamp))
    client_end_time = int(float(client_end_time)) if client_end_time else default_max_timestamp

    return get_normalized_start_and_end(
        default_min_timestamp, default_max_timestamp,
        client_start_time, client_end_time
    )


def get_normalized_start_and_end(min_value: int, max_value: int,
                                 client_start_value: int, client_end_value: int) -> Tuple[int, int]:
    """
     A function to normalize "start" and "end" numbers sent by clients;
     Returns a tuple with respectively normalized_start and normalized_end
     """

    normalized_start = client_start_value if min_value <= client_start_value < client_end_value else min_value
    normalized_end = client_end_value if normalized_start < client_end_value <= max_value else max_value

    return normalized_start, normalized_end


async def different_number_invalidation_strategy(
        cache: AbstractCacheData,
        obj_count: int,
        cache_dao: AbstractCacheDAO
) -> bool:
    """Strategy for which the cache is invalid if provided number is different from one in cache"""

    if cache.cache_over_number != obj_count:
        cache_dao.delete_cache_with_id(cache.id)
        return True  # Invalid cache
    else:
        return False  # Still valid cache


async def handle_request_with_cache(request: Request,
                                    request_handler: Callable[[Request], Awaitable[Tuple[Union[dict, list], int]]],
                                    invalid_cache_detector: Callable[[Request, AbstractCacheData], Awaitable[bool]],
                                    cache_dao: AbstractCacheDAO):
    """Utility function to handle requests leveraging on cached responses"""

    if not request.query:
        logger.info(f" Request `{request.rel_url}` has no params; serving without cache")
        # Don't cache responses to requests that doesn't need a computation
        return await create_json_response((await request_handler(request))[0])
    elif (event_time_window_from_query_name in request.query.keys() or
          event_time_window_to_query_name in request.query.keys()):
        logger.info(f" Not caching request `{request.rel_url}` which requires time to be computed")
        # Don't cache requests that require time in preparation
        return await create_json_response((await request_handler(request))[0])
    else:
        cache_id = str(request.rel_url)
        cache: Optional[AbstractCacheData] = cache_dao.find_by_id(cache_id)
        if not cache or await invalid_cache_detector(request, cache):
            logger.info(f" No cached data for request `{cache_id}`")
            (to_cache_response, computed_over_number) = await request_handler(request)
            cache_dao.insert_cache(
                CacheDataFactory.new_cache(
                    cache_id,
                    cache_data=json.dumps(to_cache_response),
                    cache_over_number=computed_over_number
                )
            )
            logger.debug(f" Sending:\n{json.dumps(to_cache_response, indent=2)}")
            return await create_json_response(to_cache_response)
        else:
            logger.info(f" Request `{cache_id}` has cached data")
            logger.debug(f" Sending:\n{json.dumps(cache.cache_data, indent=2)}")
            return await create_json_response(cache.cache_data)


def create_objects_controller(
        object_dao: AbstractDAO[T1],
        cache_dao: Optional[AbstractCacheDAO],
        aggregate_first_dimension_query_name: str = "aggregateByDimension1",
        aggregate_second_dimension_query_name: str = "aggregateByDimension2",
):
    """Creates the coroutine handling objects requests, optionally using cache"""

    async def objects_controller(request: Request):
        """The controller called when object data is requests"""

        async def _aggregated_objects_to_json_response(
                aggregated_objects: Mapping[str, List[T1]]
        ) -> Mapping[str, list]:
            """Utility function to convert aggregated objects to the json response to be sent to client"""
            return {aggregation_field: [an_object.to_json() for an_object in objects]
                    for (aggregation_field, objects) in aggregated_objects.items()}

        async def actual_request_handler(client_request: Request) -> Tuple[Union[dict, list], int]:
            """The request handler called to produce a response, and cache it"""
            all_objects: Mapping[str, T1] = object_dao.find_by()

            if client_request.query and aggregate_first_dimension_query_name in client_request.query.keys():
                logger.info(f" objects_controller received aggregate request with parameters "
                            f"`{[it for it in client_request.query.items()]}`")

                aggregated_data: Mapping[str, List[T1]] = await aggregate_objects_by_field(
                    list(all_objects.values()),
                    client_request.query.get(aggregate_first_dimension_query_name, "")
                )

                if aggregate_second_dimension_query_name in client_request.query.keys():
                    logger.info(f" Two dimensional aggregation...")
                    json_body = {}
                    for first_dimension_value, first_dimension_aggregated_data in aggregated_data.items():
                        sub_aggregated_data: Mapping[str, List[T1]] = await aggregate_objects_by_field(
                            first_dimension_aggregated_data,
                            client_request.query.get(aggregate_second_dimension_query_name, "")
                        )
                        json_body[first_dimension_value] = (
                            await _aggregated_objects_to_json_response(sub_aggregated_data)
                        )
                else:
                    json_body = await _aggregated_objects_to_json_response(aggregated_data)
            else:
                json_body = await handle_paginated_request(client_request, list(all_objects.values()),
                                                           lambda x: x.to_json())

            return json_body, len(all_objects)  # Return even on how many objects the response is computed

        async def invalid_cache(_: Request, cache: AbstractCacheData) -> bool:
            """A strategy to be used in determining if the cache is still valid or not"""
            return await different_number_invalidation_strategy(cache, object_dao.count(), cache_dao)

        if cache_dao is None:
            return await create_json_response((await actual_request_handler(request))[0])
        else:
            return await handle_request_with_cache(
                request,
                actual_request_handler,
                invalid_cache,
                cache_dao
            )

    return objects_controller


def create_object_count_controller(object_dao: AbstractDAO[T1]):
    """Creates the coroutine handling the request of counting objects"""

    async def object_count_controller(_: Request):
        """The controller handling object count request"""

        return await create_json_response({'count': object_dao.count()})

    return object_count_controller


OBJECT_ID_URL_MATCHER_STRING = 'id'


def create_object_controller(object_dao: AbstractDAO[T1]):
    """Creates the coroutine handling the request of one specific object"""

    async def object_controller(request: Request):
        """The controller handling single object request"""

        object_id = request.match_info[OBJECT_ID_URL_MATCHER_STRING]
        logger.debug(f" Request for data about object with ID: `{object_id}`")

        an_object: Optional[T1] = object_dao.find_by_id(object_id)
        if an_object:
            return await create_json_response(an_object.to_json())
        else:
            raise HTTPNotFound(reason=f"No object with ID `{object_id}`", headers=CORS_HEADER)

    return object_controller
