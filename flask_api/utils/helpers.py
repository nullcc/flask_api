from datetime import datetime, timedelta


def time_utcnow():
    """Returns a timezone aware utc timestamp."""
    return datetime.now(UTC)
