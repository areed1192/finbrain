import logging
from openai import OpenAI
from openai.types.beta.thread import Thread as ThreadType
from openai.types.beta.threads import Message as MessageType
from openai.types.beta.threads import Run

class Thread():

    """A class to represent a thread."""

    def __init__(self, client: OpenAI, thread_id: str = "") -> None:
        """Initializes the `Thread` object."""

        self._client = client

        if thread_id:
            logging.info(f"Retrieving thread with ID: {thread_id}")
            self._thread = self.retrieve(thread_id=thread_id)
        else:
            logging.info("Creating a new thread.")
            self._thread = self.create()

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
        all_messages = self._client.beta.threads.messages.list(thread_id=self._thread.id)
        all_messages = list(all_messages)

        for msg in all_messages:
            self._client.beta.threads.messages.delete(
                thread_id=self._thread.id,
                message_id=msg.id
            )

    def add_message(self, role: str, message: str, attachment: list = []) -> MessageType:
        """Adds a message to the thread."""

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
    
    def create_and_poll_run(self, assistant_id: str) -> Run:
        """Creates a new thread and polls the run."""
        
        run = self._client.beta.threads.runs.create_and_poll(
            thread_id=self._thread.id,
            assistant_id=assistant_id,
            truncation_strategy={"type": "last_messages", "last_messages": 2}
        )

        self._run = run

        if run.status == "completed":
            logging.info("Run completed.")
        
        return self._run


    def poll_run_status(self, run: Run) -> str:
        """_summary_

        ### Parameters:
        ----
        run: Run
            The run object you want to poll for status.

        ### Returns:
        ----
        Run :
            The run object once it's completed.

        ### Raise:
        ----
        valueError:
            If the thread object is None.
        """

        time_waiting = 0

        while self._run.status != "completed" and time_waiting < 60:
            logging.info("Run status: %s for run %s", run.status, run.id)
            run = self._client.beta.threads.runs.poll(
                thread_id=self._thread.id,
                run_id=self._run.id
            )
            time_waiting += 1

        return run.status
    
    def grab_messages(self) -> list:
        """Returns a list of messages in the thread."""

        msgs = self._client.beta.threads.messages.list(thread_id=self._thread.id)
        msgs = list(msgs)

        return msgs

class Threads():

    """A class to manage threads."""

    def __init__(self, client: OpenAI) -> None:
        """Initializes the `Threads` object."""
        self._client = client
