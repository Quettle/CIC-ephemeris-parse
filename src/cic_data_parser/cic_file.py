import astropy.time as time
from typing import Optional, Union
import re


class Header:
    def __init__(
        self,
        version: str,
        creation_date: Union[time.Time, str],
        originator: str,
        comment: Optional[str],
    ):
        if re.match(r"\d+\.\d+", version) is None:
            raise ValueError("Invalid version number")
        self.version = version
        match creation_date:
            case time.Time():
                if creation_date.scale not in ["utc", "tai", "tt", "tdb"]:
                    raise ValueError("Unsupported time scale")
                if creation_date.ndim != 0:
                    try:
                        creation_date = creation_date.reshape(())
                    except ValueError as e:
                        raise ValueError("Creation date must be a scalar") from e
                self.creation_date = creation_date
            case str():
                try:
                    self.creation_date = time.Time(
                        creation_date, format="isot", scale="utc"
                    )
                except ValueError as e:
                    raise ValueError("Invalid date format") from e
            case _:
                raise ValueError("Invalid date type")

        self.originator = originator
        self.comment = comment
