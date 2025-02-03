import astropy.time as time
from typing import Optional, Union, Any
import re
import astropy
import astropy.timeseries
from pathlib import Path
import os
import itertools


class Header:
    def __init__(
        self,
        cic_type: str,
        version: str,
        creation_date: Union[time.Time, str],
        originator: str,
        comment: Optional[str],
    ):
        cic_type = cic_type.upper()
        if cic_type not in ["OEM", "AEM", "MEM", "MPM"]:
            raise ValueError("Unsupported CIC type")
        self.cic_type = cic_type
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
                self.creation_date: time.Time = creation_date
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


class CICFile:
    def __init__(
        self, header: Header, meta: dict[str, Any], data: astropy.table.QTable
    ):
        self.header = header
        self.meta = meta
        self.data = data

    def write(self, path: Path):
        pass

    @classmethod
    def read(cls, path: os.PathLike):

        with Path(path).open("r") as f:
            line = f.readline()
            [cic_type, version] = line.split("=")
            version = version.strip()
            cic_type = cic_type.split("_")[1]
            match cic_type:
                case "OEM":
                    cls_inst = OEMFile
                case "AEM":
                    raise NotImplementedError("AEM file parsing is not implemented yet")
                case "MEM":
                    raise NotImplementedError("MEM file parsing is not implemented yet")
                case "MPM":
                    raise NotImplementedError("MPM file parsing is not implemented yet")
                case _:
                    raise ValueError("Invalid CIC type in header")
            if cls not in [CICFile, cls_inst]:
                raise TypeError(
                    f"expected to create an instance of {cls} but read file wath of type {cic_type}"
                )
            line = f.readline()
            if line.startswith("COMMENT"):
                comment = line[8:].rstrip()
                line = f.readline()
            else:
                comment = None
            creation_date = line.split("=")[1].strip()
            line = f.readline()
            originator = line.split("=")[1].strip()
            try:
                header = Header(cic_type, version, creation_date, originator, comment)
            except ValueError as e:
                raise ValueError("Invalid header") from e

            while f.readline() != "META_START\n":
                pass
            meta_iter = itertools.takewhile(lambda x: x != "META_END\n", f)
            meta = (
                line.split("=")
                for line in meta_iter
                if line.strip()
                if not line.startswith("COMMENT")
            )
            meta = ((k_v[0].strip(), k_v[1].strip()) for k_v in meta if len(k_v) == 2)
            meta = {k: v for k, v in meta}

            data=astropy.table.QTable.read(f, format="ascii.ecsv")
            return cls_inst(header, meta, data)


class OEMFile(CICFile):
    def __init__(
        self, header: Header, meta: dict[str, Any], data: astropy.timeseries.TimeSeries
    ):
        
        self.data: astropy.timeseries.TimeSeries
        if header.cic_type != "OEM":
            raise ValueError("Not an OEM file")
        try:
            self.object_name: str = meta["OBJECT_NAME"]
            self.object_id: str = meta["OBJECT_ID"]
            self.center_name: str = meta["CENTER_NAME"]
            if meta["REF_FRAME"] != "EME2000":
                raise ValueError("REF_FRAME must be EME2000")
            self.time_system: str = meta["TIME_SYSTEM"]
            if self.time_system not in ["TAI", "UTC", "TT", "TDB"]:
                raise ValueError("TIME_SYSTEM must be TAI or UTC")
        except KeyError as e:
            raise ValueError("Missing required metadata") from e
        super().__init__(header, meta, data)
