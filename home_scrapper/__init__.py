from pathlib import Path

__version__ = '0.1.0'

data_dir = Path(__file__).parent.parent / "data"
if not data_dir.exists():
    data_dir.mkdir(parents=True)
