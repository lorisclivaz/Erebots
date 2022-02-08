import calendar
import datetime
import logging
from typing import TypeVar, List, Optional, Mapping, Callable

T = TypeVar('T')
"""A type variable to be used writing generic functions"""

logger = logging.getLogger(__name__)

UNCATALOGUED_FIELD = "uncatalogued"


async def aggregate_objects_by_field(objects: List[T],
                                     object_field_name: Optional[str]) -> Mapping[str, List[T]]:
    """A function to aggregate objects by a specified profile field"""

    result = dict()
    if not object_field_name:
        logger.info(f" No aggregate categories since field name is empty... object_field_name: `{object_field_name}`")
        result[UNCATALOGUED_FIELD] = objects
    else:
        for an_object in objects:
            aggregate_step(an_object, object_field_name, result,
                           lambda already_catalogued, work_obj: already_catalogued.append(work_obj))

    logger.info(f" Categorized objects in: {[f'{k} -> count({len(v)})' for (k, v) in result.items()]}")
    return result


def aggregate_step(work_on_obj: T, to_consider_field: str, result_dict: dict,
                   side_effect_fun_adding_results: Callable[[List[T], T], None]):
    """Utility function refactoring the aggregation logic"""

    work_json = work_on_obj.to_json()
    if to_consider_field in ["hour", "weekday", "month", "year"]:
        # We have to preprocess data to be catalogued by those fields
        consider_field_value = work_json.get("datetime", UNCATALOGUED_FIELD)
        if consider_field_value == UNCATALOGUED_FIELD:
            # Default to common "else" behaviour
            consider_field_value = work_json.get(to_consider_field, UNCATALOGUED_FIELD)
        else:
            my_date_time: datetime.datetime = work_on_obj.datetime
            if to_consider_field == "hour":
                if not result_dict.keys():  # initialization to have all data keys even if not present data
                    for hour in range(0, 24):
                        result_dict[f"{'{:02d}'.format(hour)}-{'{:02d}'.format((hour + 1) % 24)}"] = []
                consider_field_value = f"{my_date_time.strftime('%H')}-" \
                                       f"{(my_date_time + datetime.timedelta(hours=1)).strftime('%H')}"
            elif to_consider_field == "weekday":
                if not result_dict.keys():  # initialization to have result already ordered
                    for day_name in calendar.day_name:
                        result_dict[day_name] = []
                consider_field_value = my_date_time.strftime('%A')
            elif to_consider_field == "month":
                if not result_dict.keys():  # initialization to have result already ordered
                    for month_name in calendar.month_name[1:]:
                        result_dict[month_name] = []
                consider_field_value = my_date_time.strftime('%B')
            elif to_consider_field == "year":
                consider_field_value = my_date_time.strftime('%Y')
    else:
        # Access directly the json object fields
        consider_field_value = work_json.get(to_consider_field, UNCATALOGUED_FIELD)

    already_catalogued_obj = result_dict.get(str(consider_field_value), [])
    side_effect_fun_adding_results(already_catalogued_obj, work_on_obj)
    result_dict[str(consider_field_value)] = already_catalogued_obj
