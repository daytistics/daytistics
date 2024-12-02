import datetime
import pytz
from daytistics.utils.time import minutes_today_as_iso, minutes_as_datetime


class TestMinutesTodayAsIso:

    def test_midnight(self):
        date = datetime.datetime(2024, 9, 29, 12, 0)  # Datum mit beliebiger Zeit
        assert minutes_today_as_iso(date, 0, "+02:00") == "2024-09-29T00:00:00+02:00"

    def test_noon(self):
        date = datetime.datetime(2024, 9, 29, 12, 0)
        assert minutes_today_as_iso(date, 720, "+02:00") == "2024-09-29T12:00:00+02:00"

    def test_end_of_day(self):
        date = datetime.datetime(2024, 9, 29, 12, 0)
        assert minutes_today_as_iso(date, 1439, "+02:00") == "2024-09-29T23:59:00+02:00"

    def test_different_timezone(self):
        date = datetime.datetime(2024, 9, 29, 12, 0)
        assert minutes_today_as_iso(date, 0, "-05:00") == "2024-09-29T00:00:00-05:00"

    def test_overflow_minutes(self):
        date = datetime.datetime(2024, 9, 29, 12, 0)
        assert minutes_today_as_iso(date, 1500, "+02:00") == "2024-09-30T01:00:00+02:00"


class TestMinutesAsDatetime:

    def test_midnight(self):
        # Testet, ob 0 Minuten zu Mitternacht führt
        date = datetime.datetime(2024, 9, 29, 12, 0)
        result = minutes_as_datetime(date, 0, "Europe/Berlin")
        expected = pytz.timezone("Europe/Berlin").localize(
            datetime.datetime(2024, 9, 29, 0, 0)
        )
        assert result == expected

    def test_noon(self):
        # Testet, ob 720 Minuten (12 Stunden) zu Mittag führt
        date = datetime.datetime(2024, 9, 29, 12, 0)
        result = minutes_as_datetime(date, 720, "Europe/Berlin")
        expected = pytz.timezone("Europe/Berlin").localize(
            datetime.datetime(2024, 9, 29, 12, 0)
        )
        assert result == expected

    def test_end_of_day(self):
        # Testet, ob 1439 Minuten zum Ende des Tages (23:59) führt
        date = datetime.datetime(2024, 9, 29, 12, 0)
        result = minutes_as_datetime(date, 1439, "Europe/Berlin")
        expected = pytz.timezone("Europe/Berlin").localize(
            datetime.datetime(2024, 9, 29, 23, 59)
        )
        assert result == expected

    def test_overflow_minutes(self):
        # Testet, ob Minuten über 1440 korrekt auf den nächsten Tag führen
        date = datetime.datetime(2024, 9, 29, 12, 0)
        result = minutes_as_datetime(date, 1500, "Europe/Berlin")
        expected = pytz.timezone("Europe/Berlin").localize(
            datetime.datetime(2024, 9, 30, 1, 0)
        )
        assert result == expected

    def test_different_timezone(self):
        # Testet, ob verschiedene Zeitzonen korrekt verarbeitet werden
        date = datetime.datetime(2024, 9, 29, 12, 0)
        result = minutes_as_datetime(date, 0, "America/New_York")
        expected = pytz.timezone("America/New_York").localize(
            datetime.datetime(2024, 9, 29, 0, 0)
        )
        assert result == expected
