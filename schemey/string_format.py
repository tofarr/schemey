from enum import Enum


class StringFormat(Enum):
    DATE_TIME = "date-time"
    TIME = "time"
    DATE = "date"
    EMAIL = "email"
    HOSTNAME = "hostname"
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    UUID = "uuid"
    URI = "uri"
