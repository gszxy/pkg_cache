import abc
from datetime import datetime
from enum import Enum
from typing import TypedDict


class FileRecord(TypedDict):
    file_name: str
    created: datetime
    last_download: datetime
    download_count: int
    size_kb: int


class SizeRotateStrategy(str, Enum):
    LRU = 'LRU'
    LFU = 'LFU'


class IndexInterface(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def repo(self) -> str:
        """Name of the package manager that this object implements, like 'pip' and 'apt.ubuntu'"""

    @property
    @abc.abstractmethod
    def size_rotate_strategy(self) -> SizeRotateStrategy:
        """Defines how cache items are expired due to reach of max total size"""

    @property
    @abc.abstractmethod
    def max_size(self) -> int:
        """
        Max size of all cached items in kilobytes.
        Set to 0 or negative value to disable rotation based on max size.
        """

    @property
    @abc.abstractmethod
    def ttl(self) -> int:
        """
        Time to live of items in seconds.
        Set to 0 or negative to disable expiration based on max size.
        """

    async def search(self) -> list[FileRecord]:
        """
        List indexed items.
        TODO: add query parameters and pagination.
        :return: A list of dict, each a file record as defined by class FileRecord
        """

    async def lookup(self, file_name) -> bool:
        """
        Lookup if a file is already inside the cache index.
        If not existed, return False.
        If existed, update last_download, download_count and return true
        """

    async def add(self, file_name, size_kb) -> bool:
        """
        Add a new file to the index.
        """

    async def rotate(self) -> list[str]:
        """
        rotate the cache, return a list file names that should be deleted.
        """
