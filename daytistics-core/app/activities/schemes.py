from ninja import Schema


class ActivityResponse(Schema):
    id: int
    name: str
    duration: int
    start_time: int
    end_time: int
