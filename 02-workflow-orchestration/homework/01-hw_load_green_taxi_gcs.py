from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
import pandas as pd 

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    """
    Template for loading data from a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'louise-mage-bucket'
    pre_path = 'mage-homework/'
    object_keys = ['green_tripdata_2020-10.csv', 'green_tripdata_2020-11.csv', 'green_tripdata_2020-12.csv']

    data = pd.concat((
            GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
                bucket_name,
                pre_path + object_key,
        ) for object_key in object_keys), ignore_index = True)
    return data
