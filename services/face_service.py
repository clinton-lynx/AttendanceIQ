import json
import math
from config import CONFIDENCE_THRESHOLD


def match_face(live_encoding, stored_encoding_json):
    """
    Compares a live face encoding against a stored encoding.
    Returns True if they match, False if they don't.
    """
    if not live_encoding or not stored_encoding_json:
        return False

    stored_encoding = json.loads(stored_encoding_json)

    if len(live_encoding) != len(stored_encoding):
        return False

    distance = math.sqrt(
        sum((a - b) ** 2 for a, b in zip(live_encoding, stored_encoding))
    )

    return distance < CONFIDENCE_THRESHOLD


def encode_face(image_path):
    """
    Not needed - face encoding is handled by face-api.js on the frontend.
    """
    pass