from marshy.types import ExternalItemType


def filter_none(item: ExternalItemType) -> ExternalItemType:
    return {k: v for k, v in item.items() if v is not None}
