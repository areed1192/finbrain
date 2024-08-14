"""This script demonstrates how to use the OpenAI File Assistant to process multiple files and save the responses to a file."""

import json
import pathlib
import logging

from openai import OpenAI

from finbrain.utils import Files
from finbrain.thread import Thread
from finbrain.prompts import Prompt
from finbrain.validator import Validator
from finbrain.assistant import AssistantCreator

# Create a logging object
logging.basicConfig(filename="agent_log.log", level=logging.INFO)


class FinBrainAssistant:

    def __init__(self, api_key: str, save_state: bool = False, state_file: str = "") -> None:
        """Initializes the FinBrainAssistant object.

        ### Parameters:
        ----
        api_key: str
            The OpenAI API key.

        save_state: bool (optional, default=False)
            A boolean flag to indicate whether to save the assistant state.

        state_file: str (optional, default="")
            The name of the file to save the assistant state to, this will
            allow you to resume the assistant at a later time.
        """

        # Initialize the OpenAI client.
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)

        # Initialize the state of the assistant.
        self._state = {}
        self._save_state = save_state
        self._state_file = pathlib.Path(state_file)

        # Load the state of the assistant.
        self._read_state()

        # Initialize the assistant and other helper objects.
        self.json_validator = Validator()

        # Initialize the assistant and thread objects.
        self.assistant = self._manage_assistant_creation().assistant
        self.thread = self._manage_thread_creation()

        # Initialize the Files collection object.
        self._files = Files(client=self.client)

        # If we have files already, add them to the files collection.
        if "files" in self._state:
            self._files._load(files=self._state["files"])

        # If we are allowed to save the state, update the state so we can show the assistant ID.
        if self._save_state:
            self._update_state()

    def __del__(self) -> None:
        """Saves the state of the assistant before it is destroyed."""
        self._write_state()

    @property
    def files(self) -> Files:
        """Returns the Files collection object."""
        return self._files

    @property
    def prompt(self) -> Prompt:
        """Returns the Prompt object."""
        return Prompt()

    @property
    def assistant_id(self) -> str:
        """Returns the ID of the assistant."""
        return self.assistant.id

    @property
    def thread_id(self) -> Thread:
        """Returns the ID of the thread."""
        return self.thread

    @property
    def save_state(self) -> bool:
        """Returns the value of the save_state attribute."""
        return self._save_state

    @property
    def state_file(self) -> str:
        """Returns the value of the state_file attribute."""

        if self._state_file == "":
            return "No state file provided."

        return self._state_file.as_posix()

    @property
    def state(self) -> dict:
        """Returns the value of the state attribute."""
        return self._state

    def _validate_state(self) -> bool:
        """Validates the state of the assistant.

        ### Returns:
        ----
        bool :
            A boolean value indicating whether the state is valid.
            If the state is valid, the function returns True, otherwise
            it returns False.
        """

        # Define the valid state.
        valid_state = {
            "assistant_id": str,
            "files": list,
            "thread": str
        }

        # Check if the state file is missing any keys.
        for key, value in valid_state.items():

            if key not in self._state:
                logging.error(f"State file is missing the key: {key}")
                print(f"State file is missing the key: {key}")
                return False

            if not isinstance(self._state[key], value):
                logging.error(f"State file key: {key} has an invalid value.")
                print(f"State file key: {key} has an invalid value.")
                return False

        # Now check if we have any extra keys in the state file.
        for key in self._state.keys():

            if key not in valid_state:
                logging.error(f"State file has an invalid key: {key}")
                print(f"State file has an invalid key: {key}")
                return False

        return True

    def _read_state(self) -> None:
        """Loads the state of the assistant."""

        # Step 1: Check if the state file is provided.
        if self._state_file == pathlib.Path(""):
            logging.info("No state file provided.")
            return

        # Step 2: Check if the state file exists.
        if not self._state_file.exists():
            logging.error("State file does not exist.")
            raise FileNotFoundError(
                f"State file `{self._state_file.name}` does not exist."
            )

        # Step 3: Load the state file.
        with open(file=self._state_file, mode="r", encoding="utf-8") as file:
            self._state = json.load(file)
            logging.info(
                f"State file loaded successfully: {self._state_file.name}"
            )

        # Step 4: Validate the state file.
        if not self._validate_state():
            logging.error("State file is invalid.")
            raise ValueError("State file is invalid.")

    def _update_state(self) -> None:
        """Updates the state of the assistant, before saving it."""

        self.state["assistant_id"] = self.assistant_id
        self.state["files"] = self.files.to_dict()["files"]
        self.state["thread"] = self.thread._thread.id

    def _write_state(self) -> None:
        """Saves the state of the assistant."""

        # Step 1: Check if we need to save the state.
        if not self._save_state:
            logging.info("State saving is disabled.")
            return

        # Step 2: Check if the state file is provided.
        if self._state_file == pathlib.Path(""):
            logging.info("No state file provided.")
            return

        # Step 3: Check if the state file exists.
        if not self._state_file.exists():
            logging.error("State file does not exist.")
            raise FileNotFoundError(
                f"State file `{self._state_file.name}` does not exist."
            )

        # Step 4: Update the state file.
        self._update_state()

        # Step 5: Validate the state file.
        if not self._validate_state():
            logging.error("State file is invalid.")
            raise ValueError("State file is invalid.")

        # Step 6: Save the state file.
        with open(file=self._state_file, mode="w+", encoding="utf-8") as file:
            json.dump(self._state, file, indent=4)
            logging.info(
                f"State file saved successfully: {self._state_file.name}"
            )

    def _manage_assistant_creation(self) -> AssistantCreator:
        """Manages the creation of the assistant.

        ### Returns:
        ----
        AssistantCreator :
            An AssistantCreator object that can be used to create or
            retrieve an assistant.
        """

        assistant_id = self._state.get("assistant_id", None)

        # Check if the assistant ID is in the state.
        if assistant_id is not None and assistant_id != "":
            assistant_creator = AssistantCreator(
                client=self.client,
                assistant_id=assistant_id
            )
        else:
            assistant_creator = AssistantCreator(client=self.client)

        return assistant_creator

    def _manage_thread_creation(self) -> Thread:
        """Manages the creation of the thread.

        ### Returns:
        ----
        Thread :
            A Thread object that can be used to create or
            retrieve a thread.
        """

        thread_id = self._state.get("thread", None)

        # Check if the thread ID is in the state.
        if thread_id is not None and thread_id != "":
            thread = Thread(
                client=self.client,
                thread_id=thread_id
            )
        else:
            thread = Thread(client=self.client)

        # Set the assistant for the thread.
        thread.assistant = self.assistant

        return thread
