"""This module contains the AssistantCreator class."""

from openai import OpenAI
from openai.types.beta import Assistant


class AssistantCreator:

    """A class to create and retrieve an assistant from the OpenAI platform."""

    def __init__(self, client: OpenAI, assistant_id: str = "") -> None:
        """Initializes the AssistantCreator object.

        ### Parameters:
        ----
        client: OpenAI
            The OpenAI client object.

        assistant_id: str (optional, default="")
            The ID of the assistant to retrieve. If no ID is provided,
            a new assistant will be created.

        ### Usage:
        ----
            >>> from openai import OpenAI
            >>> from finbrain import AssistantCreator
            >>> client = OpenAI(api_key)
            >>> assistant_creator = AssistantCreator(client=client)
            >>> assistant = assistant_creator.assistant
        """

        self._client = client
        self._assistant_id = assistant_id
        self.assistant = self.initalize_assistant()

    def initalize_assistant(self) -> Assistant:
        """Creates or retrieves an assistant from the OpenAI platform."""

        if self._assistant_id != "":
            return self._retrieve_assistant()

        return self._create_assistant()

    def _create_assistant(self) -> Assistant:
        """Creates an assistant on the OpenAI platform."""

        return self._client.beta.assistants.create(
            name="FinanceAgent",
            instructions="You are financial analyst who helps individuals answer questions related to their financials.",
            model="gpt-4o-mini",
            tools=[{"type": "file_search"}],
            temperature=0.2
        )

    def _retrieve_assistant(self) -> Assistant:
        """Retrieves an assistant from the OpenAI platform."""

        return self._client.beta.assistants.retrieve(
            assistant_id=self._assistant_id
        )
