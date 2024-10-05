from ninja import Schema

class WellbeingResponse(Schema):
    id: int
    name: str
    rating: int