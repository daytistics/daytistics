import random, threading, schedule
from datetime import datetime, timedelta
import src.errors as errors
import time

class Verificator:
    """
    A singleton class for managing verification requests.

    This class handles the creation, storage, and expiration of verification requests
    for user actions such as registration, password changes, and account deletion.

    Attributes:
        REGISTRATION (int): Constant representing a registration request type.
        CHANGE_PASSWORD (int): Constant representing a password change request type.
        DELETE_ACCOUNT (int): Constant representing an account deletion request type.

    The class uses a background thread to automatically remove expired requests
    every 10 seconds. Verification requests are stored with a 5-minute expiration time.
    """

    _instance = None
    REGISTRATION = 1
    CHANGE_PASSWORD = 2
    DELETE_ACCOUNT = 3

    def __init__(self):
        self.requests = {}
        self._stop_event = threading.Event()
        self._scheduler_thread = threading.Thread(target=self._remove_expired_requests_loop)
        self._scheduler_thread.daemon = True
        self._scheduler_thread.start()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def remove_expired_requests(self):
        """
        Removes expired requests from the requests dictionary.

        This method iterates over the requests dictionary and removes any requests
        that have a timestamp older than five minutes ago.

        Args:
            None

        Returns:
            None
        """

        current_time = datetime.now()
        five_minutes_ago = current_time - timedelta(minutes=5)
        self.requests = {
            email: request
            for email, request in self.requests.items()
            if request["timestamp"] > five_minutes_ago
        }

    def _remove_expired_requests_loop(self):
        """
        Continuously removes expired requests until the stop event is set.

        This method runs in a loop and calls the `remove_expired_requests` method
        to remove any expired requests. It sleeps for 10 seconds between each
        iteration.

        """

        while not self._stop_event.is_set():
            self.remove_expired_requests()
            time.sleep(10)  # Sleep for 10 seconds

    def stop_scheduler(self):
        """
        Stops the scheduler by setting the stop event and joining the scheduler thread.
        """

        self._stop_event.set()
        self._scheduler_thread.join()

    def contains_request(self, email, type):
        """
        Checks if the given email is present in the requests dictionary and has the specified type.

        Args:
            email (str): The email to check.
            type (str): The type to compare against.

        Returns:
            bool: True if the email is present and has the specified type, False otherwise.
        """
        
        return email in self.requests and self.requests[email]["type"] == type

    def add_verification_request(
        self, type, email, *args, **kwargs
    ) -> str:
        """
        Adds a verification request to the requests dictionary.

        Args:
            type (int): The type of verification request.
            email (str): The email associated with the verification request.
        
            username (str): The username associated with the request (required for: registration).
            password_hash (str): The hashed password associated with the request (required for: registration). 
            role (str): The role associated with the request (required for: registration).
            new_password (str): The new password associated with the request (required for: changing the password). 
            id (int): The id associated with the request (required for: changing the password or deleting a user).

        Returns:
            str: The verification code associated with the request.

        Raises:
            MissingFieldError: If the type, email, args or kwargs are missing.
            VerificationError: If the type is invalid or if a request with the email already exists.

        """

        if type == None or email == None or args == None or kwargs == None or email == "":
            raise errors.MissingFieldError("Type, email, args and kwargs are required.")

        if type not in [1, 2, 3]:
            raise errors.VerificationError("Invalid verification type.")

        if self.contains_request(email, type):
            raise errors.VerificationError("A request with this email and type already exists.")

        match type:
            case 1:
                if not kwargs.get("username") or not kwargs.get("password_hash") or not kwargs.get("role"):
                    raise errors.MissingFieldError("Username, password_hash and role are required for registration.")

                self.requests[email] = {
                    "type": type,
                    "code": self.generate_verification_code(),
                    "timestamp": datetime.now(),
                    "email": email,
                    "username": kwargs.get("username"),
                    "password_hash": kwargs.get("password_hash"),
                    "role": kwargs.get("role"),
                }

            case 2:
                self.requests[email] = {
                    "type": type,
                    "code": self.generate_verification_code(),
                    "timestamp": datetime.now(),
                    "email": email,
                    "new_password": kwargs.get("new_password"),
                    "id": kwargs.get("id"),
                }

            case 3:
                self.requests[email] = {
                    "type": type,
                    "code": self.generate_verification_code(),
                    "timestamp": datetime.now(),
                    "email": email,
                    "id": kwargs.get("id"),
                }
                
        return self.requests[email]["code"]


    def generate_verification_code(self) -> str:
            """
            Generates a verification code.

            Returns:
                str: The generated verification code.
            """

            return str(random.randint(100000, 999999))