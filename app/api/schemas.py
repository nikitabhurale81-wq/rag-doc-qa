"""Request payload validation helpers for the API layer."""


def require_fields(payload: dict | None, *fields: str) -> str | None:
    """Return an error message if the payload is missing any field."""
    if not payload:
        return "JSON body is required"
    for f in fields:
        if not payload.get(f):
            return f"'{f}' is required"
    return None








