#----------------------------------------------------
# Miscellanous functions to help in various usages
#----------------------------------------------------

import hashlib, hmac, datetime
from werkzeug.exceptions import Forbidden

# Ref: https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
def verify_signature(payload_body, secret_token, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        raise Forbidden("x-hub-signature-256 header is missing!")
    hash_algorithm, github_signature = signature_header.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(secret_token, 'latin-1')
    mac = hmac.new(encoded_key, msg=payload_body, digestmod=algorithm)
    if not mac:
        raise Forbidden("Request signatures didn't match!")
    
def adjust_color_brightness(color, percent):
    num = int(color[1:], 16)
    amt = round(2.55 * percent)
    r = (num >> 16) + amt
    g = ((num >> 8) & 0x00FF) + amt
    b = (num & 0x0000FF) + amt

    # Clamp the values to the range [0, 255]
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    # Format the result as a hexadecimal color
    return f"#{(r << 16 | g << 8 | b):06x}"

def add_seconds(date, sec:int):
    # date = datetime.datetime(date)
    sec = int(sec)
    output = date + datetime.timedelta(0, sec)
    return output
