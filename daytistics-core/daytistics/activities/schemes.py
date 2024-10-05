from ninja import Schema


class ActivityEntryResponse(Schema):
    id: int
    name: str
    duration: int
    start_time: str
    end_time: str


class ActivityTypeResponse(Schema):
    id: int
    name: str
    category: str
    available: bool
    active: bool
