from src.utils.exceptions import HttpAwareException

def generate_openapi_responses(*error_classes: type[HttpAwareException]) -> dict:
    return {err.status_code: {"description": err.__doc__ or err.__name__} for err in error_classes}
