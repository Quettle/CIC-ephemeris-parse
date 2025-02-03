from cic_data_parser.cic_file import CICFile, OEMFile
from pathlib import Path
from icecream import ic

def test_OEM_from_file():
    file=Path.cwd()/"tests"/"ressources"/"OEM_test.txt"

    cic=OEMFile.read(file)
    assert cic.header.cic_type=="OEM"
    assert cic.header.version=="1.0"
    assert cic.header.creation_date.to_string()=="2009-12-08T09:00:00.000"
    assert cic.header.originator=="CNES"
    assert cic.header.comment=="Sample position file for CubeSat"
    assert cic.meta["OBJECT_NAME"]=="CubeSat"
    assert cic.meta["OBJECT_ID"]=="CubeSat"
    assert cic.meta["CENTER_NAME"]=="EARTH" 

    assert cic.data.time.scale=="utc"

