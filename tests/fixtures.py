from dataclasses import field, dataclass
from enum import Enum
from typing import List, Optional, ForwardRef, Union


@dataclass
class Band:
    id: Optional[str] = None
    band_name: Optional[str] = None
    year_formed: Optional[int] = None


@dataclass
class Issue:
    id: str
    tags: List[str] = field(default_factory=list)
    status: ForwardRef(f'{__name__}.Status') = None


@dataclass
class Status:
    title: str
    public: bool = False


@dataclass
class Node:
    id: str
    parent: Optional[ForwardRef(f'{__name__}.Node')] = None
    children: List[ForwardRef(f'{__name__}.Node')] = field(default_factory=list)


class TransactionStatus(Enum):
    PENDING = 'pending'
    REJECTED = 'rejected'
    COMPLETED = 'completed'


@dataclass
class Transaction:
    id: Union[str, int, None]
    transaction_status: Optional[TransactionStatus] = None
