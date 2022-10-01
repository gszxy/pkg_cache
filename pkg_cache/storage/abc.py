import abc
from typing import AsyncIterable


class StorageEngineError(Exception):
    """
    This is intended for storage engine internal errors, such as lack of space, permission denied and so on.
    Implementations should supplement additional information about the error.
    """


class DuplicatedFileError(StorageEngineError):

    def __init__(self, file_name):
        self.file_name = file_name
        super().__init__(f"File {file_name} already exists.")


class HashValueIncorrectError(StorageEngineError):

    def __init__(self, file_name, hash_type: str, expected: str, actual: str):
        self.file_name = file_name
        self.hash_type = hash_type
        self.expected = expected
        self.actual = actual
        super().__init__(f"{hash_type} value of {file_name} is incorrect.\n"
                         f"Expected: {expected}\n"
                         f"Actual: {actual}")


class StorageInterface(metaclass=abc.ABCMeta):
    """
    Interface defining properties and methods a storage engine needs to implement.
    """

    @property
    @abc.abstractmethod
    def repo(self) -> str:
        """Name of the package manager that this object implements, like 'pip' and 'apt.ubuntu'"""

    @abc.abstractmethod
    async def store(self,
                    file_name: str,
                    file: AsyncIterable[bytes],
                    hash_type: str | None = None,
                    hash_value: str | None = None) -> int:
        """
        Store a new file, optionally verify its hash value.
        :return: The size of the file occupies in the storage in kilobytes.
        :raise HashValueIncorrectError: If a hash value is provided and the verification failed.
        :raise DuplicatedFileError: When the file name is duplicated
        :raise StorageEngineError: When other verification fails(e.g. illegal file name)
            or an internal error occurs.
        """

    async def get(self, file_name: str) -> AsyncIterable[bytes] | None:
        """Get the content of a stored file. returns None if not found."""

    async def delete(self, file_name: str) -> bool:
        """Delete a stored file. returns False if not found, else True"""

    async def sync(self, files: list[str]) -> list[str]:
        """
        Given a list of file names,
        delete those in storage but not in the list, and return those not in the storage but in the list
        """
