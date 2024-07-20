from src.main import bp


@bp.route("/")
def index():
    return "Hallo Daytistics"
