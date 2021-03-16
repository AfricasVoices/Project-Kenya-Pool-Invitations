from functools import partial

from core_data_modules.data_models import CodeScheme
from core_data_modules.traced_data.util.fold_traced_data import FoldStrategies

from configurations.code_schemes import CodeSchemes
from src.lib.configuration_objects import CodingConfiguration, CodingModes, CodingPlan


def get_rqa_coding_plans(pipeline_name):
    return [
        CodingPlan(
            raw_field="invitation_response_raw",
            dataset_name="invitation_response",
            time_field="sent_on",
            run_id_field="invitation_response_run_id",
            coda_filename="Kenya-Pool-Invitations_invitation_response.json",
            icr_filename="invitation_response.csv",
            coding_configurations=[
                CodingConfiguration(
                    coding_mode=CodingModes.MULTIPLE,
                    code_scheme=CodeSchemes.INVITATION_RESPONSE,
                    coded_field="invitation_response_coded",
                    analysis_file_key="invitation_response",
                    fold_strategy=partial(FoldStrategies.list_of_labels, CodeSchemes.INVITATION_RESPONSE)
                )
            ],
            raw_field_fold_strategy=FoldStrategies.concatenate
        )
    ]


def get_demog_coding_plans(pipeline_name):
    return []


def get_ws_correct_dataset_scheme(pipeline_name):
    # Return an empty placeholder code scheme, as we're not using WS codes in this project because there is only
    # one possible dataset.
    return CodeSchemes.WS_CORRECT_DATASET


def get_follow_up_coding_plans(pipeline_name):
    return []
