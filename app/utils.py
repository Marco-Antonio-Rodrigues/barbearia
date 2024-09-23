import json
from typing import Dict, List, Union

from flask import Response


def generate_response(
    body: Union[Dict[str, Union[int, str]], List], status: int = 200, message: str = ""
):
    if isinstance(body, dict) and message:
        body["message"] = message
    return Response(
        json.dumps(body, default=str), status=status, mimetype="application/json"
    )
