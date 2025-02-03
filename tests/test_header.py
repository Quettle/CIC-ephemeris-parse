import pytest
from cic_data_parser.cic_file import Header
from astropy.time import Time


@pytest.mark.parametrize(
    "cic_type, version, creation_date, originator, comment",
    [
        ("OEM", "1.0", Time("2023-01-01T00:00:00"), "Test Originator", "Test Comment"),
        ("AEM", "1.0", "2023-01-01T00:00:00", "Test Originator", "Test Comment"),
    ],
)
def test_header_valid(cic_type, version, creation_date, originator, comment):
    header = Header(
        cic_type=cic_type,
        version=version,
        creation_date=creation_date,
        originator=originator,
        comment=comment,
    )
    assert header.version == version
    assert header.creation_date == Time("2023-01-01T00:00:00")
    assert header.originator == originator
    assert header.comment == comment


def test_header_valid_datetime_creation_date():
    header = Header(
        cic_type="OEM",
        version="1.0",
        creation_date=Time("2023-01-01T00:00:00"),
        originator="Test Originator",
        comment="Test Comment",
    )
    assert header.version == "1.0"
    assert header.creation_date == Time("2023-01-01T00:00:00")
    assert header.originator == "Test Originator"
    assert header.comment == "Test Comment"


def test_header_valid_string_creation_date():
    header = Header(
        cic_type="OEM",
        version="1.0",
        creation_date="2023-01-01T00:00:00",
        originator="Test Originator",
        comment="Test Comment",
    )
    assert header.version == "1.0"
    assert header.creation_date == Time("2023-01-01T00:00:00")
    assert header.originator == "Test Originator"
    assert header.comment == "Test Comment"


def test_header_invalid_version():
    with pytest.raises(ValueError, match="Invalid version number"):
        Header(
            cic_type="OEM",
            version="invalid",
            creation_date=Time("2023-01-01T00:00:00"),
            originator="Test Originator",
            comment="Test Comment",
        )


def test_header_invalid_string_creation_date():
    with pytest.raises(ValueError, match="Invalid date format"):
        Header(
            cic_type="OEM",
            version="1.0",
            creation_date="invalid-date",
            originator="Test Originator",
            comment="Test Comment",
        )


def test_header_invalid_creation_date_type():
    with pytest.raises(ValueError, match="Invalid date type"):
        Header(
            cic_type="OEM",
            version="1.0",
            creation_date=12345,
            originator="Test Originator",
            comment="Test Comment",
        )

def test_header_invalid_cic_type():
    with pytest.raises(ValueError, match="Unsupported CIC type"):
        Header(
            cic_type="INVALID",
            version="1.0",
            creation_date=Time("2023-01-01T00:00:00"),
            originator="Test Originator",
            comment="Test Comment",
        )
