import os
from boto3 import Session
from logic import utils


class Database:
    AWS_ACCESS_KEY = "AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
    AWS_REGION_NAME_KEY = "AWS_REGION_NAME"

    def __init__(self):
        utils.load_environment_variables()
        self.session = Session(
            aws_access_key_id=os.environ[Database.AWS_ACCESS_KEY],
            aws_secret_access_key=os.environ[Database.AWS_SECRET_ACCESS_KEY],
            region_name=os.environ[Database.AWS_REGION_NAME_KEY]
        )
        self.database = self.session.resource('dynamodb')

    def init_tables(self):
        candidate_table = self.create_candidate_table()
        interviewer_table = self.create_interviewer_table()
        position_table = self.create_position_table()
        stage_table = self.create_stage_table()
        logger = utils.get_logger()

        logger.debug(f"Candidate table status: {candidate_table.table_status}")
        print(f"Interviewer table status: {interviewer_table.table_status}")
        print(f"Position table status: {position_table.table_status}")
        print(f"Stage table status: {stage_table.table_status}")

    def create_candidate_table(self):
        table = self.database.create_table(
            TableName='Candidate',
            KeySchema=[
                {
                    'AttributeName': 'phone',
                    'KeyType': 'HASH'  # Primary key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'phone',
                    'AttributeType': 'S'  # String type
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        return table

    def create_interviewer_table(self):
        table = self.database.create_table(
            TableName='Interviewer',
            KeySchema=[
                {
                    'AttributeName': 'user_name',
                    'KeyType': 'HASH'  # Primary key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'user_name',
                    'AttributeType': 'S'  # String type
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        return table

    def create_position_table(self):
        table = self.database.create_table(
            TableName='Position',
            KeySchema=[
                {
                    'AttributeName': 'linkdin_url',
                    'KeyType': 'HASH'  # Primary key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'linkdin_url',
                    'AttributeType': 'S'  # String type
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        return table

    def create_stage_table(self):
        table = self.database.create_table(
            TableName='Stage',
            KeySchema=[
                {
                    'AttributeName': 'reviewer_user_name',
                    'KeyType': 'HASH'  # Primary key
                },
                {
                    'AttributeName': 'type',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'reviewer_user_name',
                    'AttributeType': 'S'  # String type
                },
                {
                    'AttributeName': 'type',
                    'AttributeType': 'S'  # String type
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        return table
