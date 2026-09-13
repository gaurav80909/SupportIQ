import pytest
import pandas as pd
from pathlib import Path
from src.config import get_raw_dataset_path, RAW_DATA_DIR
from scripts.create_sample import create_sample

@pytest.fixture
def sample_twcs_csv(tmp_path):
    """Creates a miniature TWCS CSV for fast testing."""
    data = {
        'tweet_id': [1, 2, 3, 4, 5, 6, 7, 8],
        'author_id': ['cust1', 'AppleSupport', 'cust2', 'AppleSupport', 'cust3', 'AmazonHelp', 'cust4', 'AmazonHelp'],
        'inbound': [True, False, True, False, True, False, True, False],
        'created_at': ['2023-01-01'] * 8,
        'text': [
            'My battery is dying',
            'Please DM your serial number',
            'Screen is black',
            'Force restart your device',
            'Package lost',
            'Please send tracking number',
            'Item broken',
            'We can replace it'
        ],
        'response_tweet_id': [2, None, 4, None, 6, None, 8, None],
        'in_response_to_tweet_id': [None, 1, None, 3, None, 5, None, 7]
    }
    df = pd.DataFrame(data)
    csv_file = tmp_path / "mock_twcs.csv"
    df.to_csv(csv_file, index=False)
    return csv_file

def test_sampling_determinism(sample_twcs_csv, tmp_path):
    out1 = tmp_path / "sample1.csv"
    out2 = tmp_path / "sample2.csv"
    
    df1 = create_sample(sample_twcs_csv, out1, sample_size=4, seed=42)
    df2 = create_sample(sample_twcs_csv, out2, sample_size=4, seed=42)
    
    pd.testing.assert_frame_equal(df1.reset_index(drop=True), df2.reset_index(drop=True))

def test_sampling_seed_variation(sample_twcs_csv, tmp_path):
    out1 = tmp_path / "sample_seed1.csv"
    out2 = tmp_path / "sample_seed2.csv"
    
    df1 = create_sample(sample_twcs_csv, out1, sample_size=4, seed=42, uniform=True)
    df2 = create_sample(sample_twcs_csv, out2, sample_size=4, seed=999, uniform=True)
    
    # Different seeds should yield different row selections (or order)
    assert not df1['tweet_id'].tolist() == df2['tweet_id'].tolist()

def test_sampling_size_configurable(sample_twcs_csv, tmp_path):
    out = tmp_path / "sample_size6.csv"
    df = create_sample(sample_twcs_csv, out, sample_size=6, seed=42)
    assert len(df) == 6

def test_dynamic_raw_dataset_path_preferred(tmp_path):
    custom = tmp_path / "custom.csv"
    resolved = get_raw_dataset_path(custom)
    assert resolved == custom

def test_dynamic_raw_dataset_path_resolution():
    resolved = get_raw_dataset_path()
    assert resolved.exists()
    assert resolved.name in ["twcs.csv", "twcs_sample.csv"]
