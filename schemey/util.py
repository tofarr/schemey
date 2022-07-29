from typing import Dict


def filter_none(d: Dict):
    return {k: v for k, v in d.items() if v is not None}
