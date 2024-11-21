import datetime

def time_passed(time: str) -> str:
    time = datetime.fromisoformat(time)
    delta = datetime.now() - time
    if delta.days:
        return f"{delta.days} days ago"
    elif delta.seconds // 3600:
        return f"{delta.seconds // 3600} hours ago"
    elif delta.seconds // 60:
        return f"{delta.seconds // 60} minutes ago"
    else:
        return f"{delta.seconds} seconds ago"