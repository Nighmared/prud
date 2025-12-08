"""Generic library for easier loading of
configurations from env variables"""

import os
from typing import Optional

TypeOfOptional = type(
    Optional[str]
)  # ugly but less ugly than importing typing._UnionGenericAlias

boolean_true_strings_lower = ["true", "yes", "1", "t"]


class Config:
    """Parent class to be subclassed by client programs
    Fields for the subclass have to be typed and can
    optionally have a default value
    ``
    class ProgramConfig(Config):
        field_a: int
        field_b: complex = 3+2j

    config = ProgramConfig(prefix="program")
    ``
    the above example will raise an error unless the
    environment variable (case optional) PROGRAM_FIELD_A
    is present and set to an integer.
    Optionally the default value for field_b can be overwritten
    by defining the environment variable PROGRAM_FIELD_B

    Handled types are int, float, complex, bool
    everything else will be set as a string

    """

    __prefix: str
    __field_types: dict[str, type]
    __cached_print_string = ""

    def __init__(self, prefix: str) -> None:
        self.__prefix = prefix
        self.__field_types = {}
        cls = self.__class__

        for k in cls.__annotations__.keys():
            is_optional = False
            env_v = os.environ.get(prefix.upper() + "_" + k.upper())
            try:
                field_type = cls.__annotations__[k]
                if isinstance(field_type, TypeOfOptional):
                    is_optional = True
                    field_type = field_type.__args__[0]
            except KeyError as exc:
                raise ValueError(f"No type given for field {cls.__name__}.{k}") from exc
            self.__field_types[k] = field_type
            if env_v is None:
                if is_optional:
                    continue  # allowed to be empty
                else:
                    if cls.__dict__[k] is None:
                        raise ValueError(
                            "No value was given for required"
                            + f"field {cls.__name__}.{k} of type "
                            + f"{cls.__annotations__[k]}"
                        )

            elif field_type is int:
                self.__dict__[k] = int(env_v)
            elif field_type is float:
                self.__dict__[k] = float(env_v)
            elif field_type is complex:
                use_j_for_imaginary = env_v.replace("i", "j")
                self.__dict__[k] = complex(use_j_for_imaginary)
            elif field_type is bool:
                self.__dict__[k] = env_v.lower() in boolean_true_strings_lower
            else:
                self.__dict__[k] = env_v

    def __repr__(self) -> str:
        if self.__cached_print_string != "":
            return self.__cached_print_string
        res_str = f"Config[{self.__prefix}]\n"
        for field_name, field_type in self.__field_types.items():
            res_str += f"  .{field_name}:{field_type} = {self.__dict__[field_name]}\n"
        self.__cached_print_string = res_str
        return res_str
