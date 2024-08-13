import pathlib
from finbrain.utils import File


class Prompt():

    """The `Prompt` class creates prompts for that will be used by the agent."""

    def __init__(self) -> None:
        """Initializes the `Prompt` object."""

        parent_dir = pathlib.Path(__file__).parent
        self._templates_folder = parent_dir.joinpath("templates")

    def create_prompt(self, file: File) -> str:
        """Creates a prompt for the document summary task.

        ### Parameters:
        ----
        file: File
            The file to be summarized.

        ### Returns:
        ----
        str :
            The prompt for the document summary task.
        """

        # Define the full path to the prompt file.
        file_path = self._templates_folder.joinpath("document_summary.md")

        # Open the markdown file of the prompt that needs to be created
        with open(file=file_path, mode="r", encoding="utf-8") as prompt_file:
            prompt = prompt_file.read()
            prompt = prompt.format(document_name=file.name)

        return prompt

    def write_prompt(self, file: File, output_path: str) -> None:
        """Writes the prompt to a file.

        ### Parameters:
        ----
        file: File
            The file to be summarized.

        output_path: str
            The path to write the prompt to.
        """

        # Create the prompt.
        prompt = self.create_prompt(file=file)

        # Write the prompt to the output path.
        with open(file=output_path, mode="w+", encoding="utf-8") as output_file:
            output_file.write(prompt)
