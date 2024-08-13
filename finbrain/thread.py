import logging
from openai import OpenAI
from openai.types.beta import Assistant
from openai.types.beta.threads import Run
from openai.types.beta.thread import Thread as ThreadType
from openai.types.beta.threads import Message as MessageType


class Thread():

    """A class to represent a thread."""

    def __init__(self, client: OpenAI, thread_id: str = "") -> None:
        """Initializes the `Thread` object.

        ### Parameters:
        ----
        client : OpenAI
            The OpenAI client object.

        thread_id : str (optional, default="")
            The ID of the thread to retrieve. If no ID is provided,
            a new thread will be created.
        """

        self._client = client

        if thread_id:
            logging.info(f"Retrieving thread with ID: {thread_id}")
            self._thread = self.retrieve(thread_id=thread_id)
        else:
            logging.info("Creating a new thread.")
            self._thread = self.create()

    @property
    def assistant(self) -> Assistant:
        """Returns the assistant ID of the thread."""
        return self._assistant

    @assistant.setter
    def assistant(self, assistant: Assistant) -> None:
        """Sets the assistant ID of the thread."""
        self._assistant = assistant

    def create(self) -> ThreadType:
        """Creates a new thread."""
        return self._client.beta.threads.create()

    def retrieve(self, thread_id: str) -> ThreadType:
        """Retrieves a thread by ID."""
        return self._client.beta.threads.retrieve(thread_id)

    def delete(self) -> None:
        """Deletes a thread."""
        self._client.beta.threads.delete(thread_id=self._thread.id)

    def clear_messages(self) -> None:
        """Clears all messages in the thread."""

        # Grab all the message ids
        all_messages = self._client.beta.threads.messages.list(
            thread_id=self._thread.id)
        all_messages = list(all_messages)

        for msg in all_messages:
            self._client.beta.threads.messages.delete(
                thread_id=self._thread.id,
                message_id=msg.id
            )

    def add_message(self, role: str, message: str, attachment: list = []) -> MessageType:
        """Adds a message to the thread.

        ### Parameters:
        ----
        role : str
            The role of the user. Must be either 'user' or 'assistant'.

        message : str
            The message to add to the thread.

        attachment : list
            A list of attachments to add to the message.

        ### Returns:
        ----
        Message :
            The message that was added to the thread.
        """

        if role != 'user' and role != 'assistant':
            raise ValueError("Role must be either 'user' or 'assistant'.")

        if attachment != {}:
            new_message = self._client.beta.threads.messages.create(
                thread_id=self._thread.id,
                role=role,
                content=message,
                attachments=attachment
            )
        else:
            new_message = self._client.beta.threads.messages.create(
                thread_id=self._thread.id,
                role=role,
                content=message
            )

        return new_message

    def create_run(self) -> Run:
        """Creates a new thread and polls the run.

        ### Returns:
        ----
        Run :
            The run object that was created.
        """

        self._run = self._client.beta.threads.runs.create_and_poll(
            thread_id=self._thread.id,
            assistant_id=self.assistant.id,
            truncation_strategy={"type": "last_messages", "last_messages": 2}
        )

        return self._run

    def poll_run_status(self) -> str:
        """Polls the run to grab the status.

        ### Returns:
        ----
        str :
            The status of the run.
        """

        time_waiting = 0

        while self._run.status != "completed" and time_waiting < 60:
            logging.info(
                "Run status: %s for run %s",
                self._run.status,
                self._run.id
            )
            run = self._client.beta.threads.runs.poll(
                thread_id=self._thread.id,
                run_id=self._run.id
            )
            time_waiting += 1

        return self._run.status

    def grab_messages(self) -> list:
        """Returns a list of messages in the thread."""

        msgs = self._client.beta.threads.messages.list(
            thread_id=self._thread.id)
        msgs = list(msgs)

        return msgs

