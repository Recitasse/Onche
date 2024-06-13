import datetime

def serialize_date(date: datetime) -> str:
    """Serialize datetime to str"""
    return date.strftime("%Y-%m-%d %H:%M:%S")


def serialize_time(date: datetime) -> str:
    """Serialize datetime to str"""
    return date.strftime("%Y-%m-%d %H:%M:%S")


def serialize_datetime(date: datetime) -> str:
    """Serialize datetime to str"""
    return date.strftime("%Y-%m-%d %H:%M:%S")


def serialize_timestamp(date: datetime) -> str:
    """Serialize datetime to str"""
    return date.strftime("%Y-%m-%d %H:%M:%S")