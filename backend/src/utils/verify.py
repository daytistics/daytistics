import random, threading, schedule
from datetime import datetime, timedelta

class Verificator:
    _instance = None
    REGISTRATION = 1
    CHANGE_PASSWORD = 2
    DELETE_ACCOUNT = 3

    def __init__(self):
        scheduler_thread = threading.Thread(
            target=self.remove_expired_requests_scheduler
        )
        scheduler_thread.start()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.requests = []

    def contains_request(self, email, type):
        for request in self.requests:
            if email in request and request[email]["type"] == type:
                return True
        return False

    # TODO: Write tests for this function & document it
    def add_verification_request(
        self, type, email, *args, **kwargs
    ) -> str:
        match type:
            case 1:
                self.requests.append(
            {
                email: {
                    "type": type,
                    "code": self.generate_verification_code(),
                    "password" "timestamp": datetime.now(),
                    "username": kwargs.get("username"),
                    "password_hash": kwargs.get("password_hash"),
                    "role": kwargs.get("role"),
                    "email": email
                }
            })

            case 2:
                self.requests.append(
            {
                email: {
                    "type": type,
                    "code": self.generate_verification_code(),
                    "timestamp": datetime.now(),
                    "email": email,
                    "new_password": kwargs.get("new_password"),
                    "id": kwargs.get("id")
                }
            })

            case 3:
                self.requests.append(
            {
                email: {
                    "type": type,
                    "code": self.generate_verification_code(),
                    "timestamp": datetime.now(),
                    "email": email,
                    "id": kwargs.get("id")
                }
            }
        )
                
        return self.requests[email]["code"]


    def remove_expired_requests(self):
        current_time = datetime.now()
        five_minutes_ago = current_time - timedelta(minutes=5)
        Verificator.requests = [
            request
            for request in Verificator.requests
            if request["timestamp"] > five_minutes_ago
        ]

    def remove_expired_requests_scheduler(self):
        schedule.every(10).seconds.do(Verificator.remove_expired_requests)
        while True:
            schedule.run_pending()
            threading.Event().wait(1)

    def generate_verification_code(self) -> str:
            """
            Generates a verification code.

            Returns:
                str: The generated verification code.
            """

            return str(random.randint(100000, 999999))