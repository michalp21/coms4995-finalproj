import json
import sys

from acpc_python_client import wrappers
from acpc_python_client.data.action_type import ActionType
from acpc_python_client.data.betting_type import BettingType

_NUMBERS = (int, float)


def wrapper_to_str(wrapper_object, formatted=True, contents_only=False):
    if isinstance(wrapper_object, str):
        return wrapper_object
    elif isinstance(wrapper_object, _NUMBERS):
        return str(wrapper_object)
    elif isinstance(wrapper_object, bool):
        return 'true' if wrapper_object else 'false'
    elif hasattr(wrapper_object, '_length_'):
        # Object is special C array wrapper class
        return '[ %s ]' % ', '.join([wrapper_to_str(e, False, True) for e in wrapper_object])
    else:
        # Object is wrapped structure
        has_contents = hasattr(wrapper_object, 'contents')
        type_fields = wrapper_object.contents._fields_ if has_contents else wrapper_object._fields_

        # Create strings containing "name": value from fields on the object in json format
        attribute_names = [field[0] for field in type_fields]
        attribute_vals = [getattr(wrapper_object.contents if has_contents else wrapper_object, field[0])
                          for field in type_fields]
        attribute_vals_strings = [wrapper_to_str(attr_val, False, True) for attr_val in attribute_vals]
        attribute_strings = ['"%s": %s' % attr for attr in zip(attribute_names, attribute_vals_strings)]

        # Pretty print it with json module
        json_string = '{ %s }' % ', '.join(attribute_strings)
        if formatted:
            try:
                json_object = json.loads(json_string)
            except:
                print('Unexpected error:', sys.exc_info()[0])
                print('Error while json parsing following json string:')
                print(json_string)
                raise
            json_string = json.dumps(json_object, sort_keys=False, indent=4)
        if contents_only:
            return json_string
        else:
            object_name = \
                (wrapper_object._type_ if hasattr(wrapper_object, '_type_') else type(wrapper_object)).__name__
            return '%s: %s' % (object_name, json_string)


def action_type_enum_to_int(action_type):
    if action_type == ActionType.FOLD:
        return wrappers.a_fold
    elif action_type == ActionType.CALL:
        return wrappers.a_call
    elif action_type == ActionType.RAISE:
        return wrappers.a_raise
    else:
        raise ValueError('Unknown action type')


def action_type_int_to_enum(action_type_int):
    if action_type_int == wrappers.a_fold:
        return ActionType.FOLD
    elif action_type_int == wrappers.a_call:
        return ActionType.CALL
    elif action_type_int == wrappers.a_raise:
        return ActionType.RAISE
    else:
        raise ValueError('Unknown action type')


def betting_type_int_to_enum(betting_type):
    if betting_type == wrappers.limitBetting:
        return BettingType.LIMIT
    elif betting_type == wrappers.noLimitBetting:
        return BettingType.NO_LIMIT
    else:
        raise ValueError('Unknown betting type')
