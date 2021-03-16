import csv
import os.path

from core_data_modules.logging import Logger
from core_data_modules.traced_data import Metadata
import time

from src.lib import PipelineConfiguration

log = Logger(__name__)


class ListeningGroups(object):
    @classmethod
    def tag_listening_groups_participants(cls, user, data, pipeline_configuration, raw_data_dir):
        """
        This tags uids who participated in repeat listening groups and/or weekly listening
        group sessions.
        :param user: Identifier of the user running this program, for TracedData Metadata.
        :type user: str
        :param data: TracedData objects to tag listening group participation to.
        :type data: iterable of TracedData
        :param raw_data_dir: Directory containing de-identified listening groups contacts CSVs containing
                                    listening groups data stored as `Name` and `avf-phone-uuid` columns.
        :type user: str
        :param pipeline_configuration: Pipeline configuration.
        :type pipeline_configuration: PipelineConfiguration
        """
        repeat_listening_group_participants = [] # Contains uids of listening group participants who will participate
                                                 # in all listening group sessions.
        listening_group_participants = dict()   # Contains lists of weekly listening group participants. The participants
                                                # will change each week.

        # Read repeat listening group participants CSV and add their uids to repeat_listening_group_participants lists
        if os.path.exists(f'{raw_data_dir}/s01_kalobeyei_repeat_listening_group.csv'):
            with open(f'{raw_data_dir}/s01_kalobeyei_repeat_listening_group.csv', "r", encoding='utf-8-sig') as f:
                repeat_listening_group_data = list(csv.DictReader(f))
                for row in repeat_listening_group_data:
                    repeat_listening_group_participants.append(row['avf-phone-uuid'])
                log.info(f'Loaded {len(repeat_listening_group_participants)} repeat listening group participants')
        else:
            log.warning(f'Skipping loading {raw_data_dir}/repeat_listening_group.csv, file not found!')

        # Read weekly listening group participants CSVs and add their uids to the respective radio-show
        # listening_group_participants lists
        listening_group_csvs = []
        for listening_group_csv_url in pipeline_configuration.listening_group_csv_urls:
            listening_group_csvs.append(listening_group_csv_url.split("/")[-1])
        for plan in PipelineConfiguration.RQA_CODING_PLANS:
            listening_group_participants[plan.dataset_name] = set()
            if plan.listening_group_filename in listening_group_csvs:
                with open(f'{raw_data_dir}/{plan.listening_group_filename}', "r",
                          encoding='utf-8-sig') as f:
                    plan_listening_group_data = list(csv.DictReader(f))
                    for row in plan_listening_group_data:
                        listening_group_participants[plan.dataset_name].add(row['avf-phone-uuid'])
                    log.info(f'Loaded {len(listening_group_participants[f"{plan.dataset_name}"])} '
                             f'{plan.dataset_name} listening group participants')
            else:
                log.warning(f'Skipping loading {plan.listening_group_filename},file not found!')

        # 1.Check if a participant is part of the repeat listening groups contacts then tag true or false otherwise
        #   Example - "repeat_listening_group_participant": true
        # 2.Check if a participant participated in a radio show listening group then tag true or false otherwise
        #   Example - "kakuma_s01e01_listening_group_participant": false
        for td in data:
            listening_group_participation = dict() # of uid repeat and weekly listening group participation data
            listening_group_participation["repeat_listening_group_participant"] = td["uid"] in repeat_listening_group_participants
            for plan in PipelineConfiguration.RQA_CODING_PLANS:
                listening_group_participation[f'{plan.dataset_name}_listening_group_participant'] =  td['uid'] in listening_group_participants[plan.dataset_name]

            td.append_data(listening_group_participation, Metadata(user, Metadata.get_call_location(), time.time()))
