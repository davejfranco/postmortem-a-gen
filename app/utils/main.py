from datetime import datetime


def convert_timestamp_to_readable(timestamp: str, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    ts_float = float(timestamp)
    dt = datetime.fromtimestamp(ts_float)
    return dt.strftime(format)
