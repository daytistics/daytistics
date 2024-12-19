from fastapi.templating import Jinja2Templates

import os


def create_jinja2() -> Jinja2Templates:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    templates_directory = os.path.join(current_directory, "../templates")
    return Jinja2Templates(directory=templates_directory)


jinja2 = create_jinja2()
