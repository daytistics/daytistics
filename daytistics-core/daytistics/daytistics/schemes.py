from typing import List

from ninja import Schema

from ..users.schemes import UserProfileResponse
from ..wellbeing.schemes import WellbeingResponse
from ..activities.schemes import ActivityEntryResponse
from ..diary.schemes import DiaryResponse


class CreateDaytisticRequest(Schema):
    date: str


class CreateDaytisticResponse(Schema):
    id: int


class DaytisticResponse(Schema):
    id: int
    date: str
    average_wellbeing: float
    total_activities: int
    total_duration: int
    user: UserProfileResponse
    wellbeing: List[WellbeingResponse]
    activities: List[ActivityEntryResponse]
    diary: DiaryResponse


class CreateActivityEntryRequest(Schema):
    id: int
    start_time: str
    end_time: str


class CreateActivityEntryResponse(Schema):
    activities: List[ActivityEntryResponse]
