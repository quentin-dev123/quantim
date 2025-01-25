#----------------------------------------------------
# Miscellanous functions to help in various usages
#----------------------------------------------------

import hashlib
import hmac
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
