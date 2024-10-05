from typing import List, Optional

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
    wellbeing: List[Optional[WellbeingResponse]]
    activities: List[Optional[ActivityEntryResponse]]
    diary: DiaryResponse


class DaytisticsListResponse(Schema):
    daytistics: List[DaytisticResponse]


class AddActivityEntryRequest(Schema):
    id: int
    start_time: str
    end_time: str


class AddActivityEntryResponse(Schema):
    activities: List[ActivityEntryResponse]
