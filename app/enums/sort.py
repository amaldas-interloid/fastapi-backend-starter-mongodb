from enum import StrEnum


class UserSortField(StrEnum):
    CREATED_AT = "created_at"
    USERNAME = "username"
    EMAIL = "email"


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"