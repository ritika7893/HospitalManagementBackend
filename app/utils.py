import uuid


def generate_id(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:6].upper()}"