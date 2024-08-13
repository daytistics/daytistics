from daytistics.models import Daytistic, ActivityEntry
from queue import Queue
from typing import Any, Callable, Dict
from django.db.models import QuerySet

class EditDaytisticStorage:
    def __init__(self, daytistic: Daytistic) -> None:
        self.daytistic = daytistic
        self.change_queue: Queue = Queue()

    def add_change(self, change: Callable[[], Any]) -> None:
        self.change_queue.put(change)

    def save(self) -> None:
        while not self.change_queue.empty():
            change = self.change_queue.get()
            change()
        self.daytistic.save()

    def add_activity(self, activity_data: dict) -> None:
        def change():
            activity_entry = ActivityEntry.objects.create(**activity_data)
            self.daytistic.activities.add(activity_entry)
        self.add_change(change)

    def remove_activity(self, activity_id: int) -> None:
        def change():
            activity_entry = self.daytistic.activities.filter(id=activity_id).first()
            if activity_entry:
                self.daytistic.activities.remove(activity_entry)
                activity_entry.delete()
        self.add_change(change)

    def edit_activity_duration(self, activity_id: int, new_duration: int) -> None:
        def change():
            activity_entry = self.daytistic.activities.filter(id=activity_id).first()
            if activity_entry:
                activity_entry.duration = new_duration
                activity_entry.save()
        self.add_change(change)

    def reset(self) -> None:
        self.change_queue = Queue()

    def stop_editing(self) -> None:
        self.reset()
        CurrentEditingsStorage().remove_storage(self.daytistic.id)
        del self

    @property
    def activities(self) -> QuerySet:
        return self.daytistic.activities.all()
    

class CurrentEditingsStorage:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.currently_editing = {}
        return cls._instance
    
    def __init__(self):
        self.currently_editing: Dict[int, EditDaytisticStorage] = {}

    def get_storage(self, daytistic_id: int) -> EditDaytisticStorage:
        return self.currently_editing.get(daytistic_id)

    def add_storage(self, daytistic_id: int) -> EditDaytisticStorage:
        storage = EditDaytisticStorage(Daytistic.objects.get(id=daytistic_id))
        self.currently_editing[daytistic_id] = storage
        return storage

    def remove_storage(self, daytistic_id: int) -> bool:
        try:
            if daytistic_id in self.currently_editing:
                self.currently_editing.pop(daytistic_id)
                return True
            return False
        except Exception as e:
            return False