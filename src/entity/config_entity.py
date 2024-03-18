from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    raw_data_file: Path
    train_data_file: Path
    test_data_file: Path

@dataclass
class ModelTrainerConfig:
    model_file: Path
    