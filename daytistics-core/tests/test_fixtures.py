import pytest
from datetime import datetime, timedelta


@pytest.mark.django_db
class TestDayGeneratorFixture:
    def test_day_generator_length(self, day_generator):
        start_date = datetime(year=2024, month=1, day=1)
        n = 10

        generated_days = list(day_generator(start_date, n))

        assert (
            len(generated_days) == n
        )  # Ensure the correct number of days is generated

    def test_day_generator_order(self, day_generator):
        start_date = datetime(year=2024, month=1, day=1)
        n = 10

        generated_days = list(day_generator(start_date, n))

        # Ensure that each date is greater than the previous one (increasing order)
        for i in range(1, len(generated_days)):
            assert generated_days[i] > generated_days[i - 1]

    def test_day_generator_large_jump(self, day_generator):
        start_date = datetime(year=2024, month=1, day=1)
        n = 10

        generated_days = list(day_generator(start_date, n))

        # Check that the jumps between consecutive dates are within the expected range (1 to 10 days)
        for i in range(1, len(generated_days)):
            delta = generated_days[i] - generated_days[i - 1]
            assert timedelta(days=1) <= delta <= timedelta(days=10)
