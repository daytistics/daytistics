from ninja import Schema


class DiaryResponse(Schema):
    entry: str
    moment_of_happiness: str