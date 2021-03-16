import json

from core_data_modules.data_models import CodeScheme


def _open_scheme(filename):
    with open(f"code_schemes/{filename}", "r") as f:
        firebase_map = json.load(f)
        return CodeScheme.from_firebase_map(firebase_map)


class CodeSchemes(object):
    INVITATION_RESPONSE = _open_scheme("invitation_response.json")

    # The pipeline doesn't need a WS correct dataset because there is only one possible dataset, so return
    # a near-empty placeholder for pipeline compatibility.
    WS_CORRECT_DATASET = _open_scheme("ws_correct_dataset.json")
