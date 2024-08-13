import json
import pathlib
import logging
from openai import OpenAI


class File:

    """A class to represent a file."""

    def __init__(self, path: str) -> None:
        """Initializes the File object.

        ### Parameters:
        ----
        path : str
            The path to the file
        """

        self._path = pathlib.Path(path)
        self._is_uploaded = False
        self._file_id = ""
        self._size = self._path.stat().st_size
        self._creation_date = self._path.stat().st_ctime
        self._upload_date = None

    @property
    def client(self) -> OpenAI:
        """Returns the client for the file."""
        return self._client

    # Create a setter property for the client.
    @client.setter
    def client(self, client: OpenAI) -> None:
        """Sets the client for the file."""
        self._client = client

    @property
    def name(self) -> str:
        """Returns the name of the file."""
        return self._path.name

    @property
    def is_uploaded(self) -> bool:
        """Returns a boolean flag to indicate whether the file has been uploaded."""
        return self._is_uploaded

    @property
    def file_id(self) -> str:
        """Returns the ID of the file."""
        return self._file_id

    def upload(self) -> None:
        """Uploads the file to the OpenAI API."""

        # Check if the file has already been uploaded.
        if self._is_uploaded:
            logging.info(f"File {self.name} has already been uploaded.")
            return

        # Upload the file to the OpenAI API.
        file_obj = self._client.files.create(
            file=self._path,
            purpose="assistants"
        )

        self._file_id = file_obj.id
        self._is_uploaded = True
        self._upload_date = file_obj.created_at

        logging.info(f"File {self.name} has been uploaded.")

    def delete(self) -> None:
        """Deletes the file from the OpenAI API."""

        # Check if the file has been uploaded.
        if not self._is_uploaded:
            logging.info(f"File {self.name} has not been uploaded.")
            return

        # Delete the file from the OpenAI API.
        self._client.files.delete(file_id=self._file_id)

        # Reset the file ID and is_uploaded flag.
        self._file_id = ""
        self._is_uploaded = False

        logging.info(f"File {self.name} has been deleted.")

    def to_dict(self) -> dict:
        """Returns the file as a dictionary."""

        return {
            "file_id": self.file_id,
            "name": self.name,
            "is_uploaded": self.is_uploaded,
            "path": self._path.as_posix(),
            "size": self._size,
            "creation_date": self._creation_date,
            "upload_date": self._upload_date
        }

    def to_json(self) -> str:
        """Returns the file as a JSON string."""
        return json.dumps(self.to_dict())


class Files:

    def __init__(self, client: OpenAI) -> None:

        self._client = client
        self._files = []
        self._indexes_by_name = {}
        self._indexes_by_id = {}

    def __repr__(self) -> str:
        """Returns the string representation of the object."""
        return f"Files(client={self._client})"

    def __len__(self) -> int:
        """Returns the number of files."""
        return len(self._files)

    def __getitem__(self, index: int) -> File:
        """Returns a file at the given index."""
        return self._files[index]

    def __iter__(self):
        """Iterates over the files."""
        for file in self._files:
            yield file

    def list_files(self) -> list:
        """Lists the files."""
        return self._files

    def _load(self, files: list) -> None:
        """Loads the files from a list of dictionaries.

        ### Parameters:
        ----
        files: list
            A list of dictionaries containing the file information.
        """

        for file in files:
            new_file = File(path=file['path'])
            new_file._file_id = file['file_id']
            new_file._is_uploaded = file['is_uploaded']
            new_file.client = self._client
            self._files.append(new_file)
            self._indexes_by_name[new_file.name] = len(self._files) - 1
            self._indexes_by_id[new_file.file_id] = len(self._files) - 1

    def add(self, file_path: str) -> None:
        """Adds a file to the list of files.

        ### Parameters:
        ----
        file_path: str
            The path to the file to add.
        """

        # Step 1: Check if the file has already been added by checking the name.
        file_name = pathlib.Path(file_path).name
        index = self._indexes_by_name.get(file_name, None)

        # If the file has already been added, return.
        if index is not None:
            logging.info(f"File {file_name} has already been added.")
            print(f"File {file_name} has already been added.")
            return

        # Create a new file object.
        file = File(path=file_path)
        file.client = self._client
        logging.info(f"Adding file {file_name} to the list of files.")
        self._files.append(file)

        # Add the index
        index = len(self._files) - 1
        self._indexes_by_name[file.name] = index

    def get_by_name(self, name: str) -> File:
        """Returns a file by name.

        ### Parameters:
        ----
        name: str
            The name of the file to return.
        """
        index = self._indexes_by_name.get(name, None)
        if index is not None:
            return self._files[index]
        else:
            raise ValueError(f"File with name {name} does not exist.")

    def get_by_id(self, file_id: str) -> File:
        """Returns a file by ID.

        ### Parameters:
        ----
        file_id: str
            The ID of the file to return
        """
        # Get the index of the file.
        index = self._indexes_by_id.get(file_id, None)

        # Check if the file exists.
        if index is not None:
            return self._files[index]
        else:
            raise ValueError(f"File with ID {file_id} does not exist.")

    def delete_by_name(self, name: str) -> None:
        """Deletes a file from the list of files.

        ### Parameters:
        ----
        name: str
            The name of the file to delete.
        """

        # Get the index of the file.
        index = self._indexes_by_name.get(name, None)

        # Check if the file exists.
        if index is not None:
            del self._files[index]
            del self._indexes_by_name[name]
            self._rebuild_indexes()
        else:
            raise ValueError(f"File with name {name} does not exist.")

    def delete_by_index(self, index: int) -> None:
        """Deletes a file from the list of files.

        ### Parameters:
        ----
        index: int
            The index of the file to delete.
        """

        # Get the file name.
        file_name = self._files[index].name

        # Delete the file.
        del self._files[index]
        del self._indexes_by_name[file_name]
        self._rebuild_indexes()

    def delete_by_id(self, file_id: str) -> None:
        """Deletes a file from the list of files.

        ### Parameters:
        ----
        file_id: str
            The ID of the file to delete.
        """

        # Get the index of the file.
        index = self._indexes_by_id.get(file_id, None)

        # Check if the file exists.
        if index is not None:
            file_name = self._files[index].name
            del self._files[index]
            del self._indexes_by_name[file_name]

    def _rebuild_indexes(self) -> None:
        """Rebuilds the indexes."""
        self._indexes_by_name = {
            file.name: idx for idx, file in enumerate(self._files)
        }

    def to_dict(self) -> dict:
        """Returns the files as a dictionary."""
        return {
            "files": [file.to_dict() for file in self._files]
        }

    def to_json(self) -> str:
        """Returns the files as a JSON string."""
        return json.dumps(self.to_dict())
