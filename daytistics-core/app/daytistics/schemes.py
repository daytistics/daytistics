from typing import List

from ninja import Schema

from app import activities
from ..users.schemes import UserProfileResponse
from ..wellbeing.schemes import WellbeingResponse
from ..activities.schemes import ActivityResponse
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
    activities: List[ActivityResponse]
    diary: DiaryResponse


class CreateActivityEntryRequest(Schema):
    name: str
    start_time: int
    end_time: int

class CreateActivityEntryResponse(Schema):
    activities: List[ActivityResponse]
