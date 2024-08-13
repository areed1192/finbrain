import pathlib
from configparser import ConfigParser

from finbrain.client import FinBrainAssistant


# Path to the configuration file.
config = ConfigParser()
config.read('configs/config.ini')
api_key = config['openai_keys']['openai_secret_key']

# Initialize the FinBrainAssistant object.
assistant = FinBrainAssistant(
    api_key=api_key, save_state=True, state_file="state.json")

# # Grab the Save State attribute.
# print(assistant.save_state)

# # Grab the State File attribute.
# print(assistant.state_file)

# # Grab the State attribute.
# print(assistant.state)

assistant.files.add(file_path="sec_docs/13567242.html")
assistant.files.add(file_path="sec_docs/14564912.html")

# print(assistant.files.list_files())

# Grab a file by name.
file = assistant.files.get_by_name(name="14564912.html")
file.upload()

# print(assistant.files.to_dict())
# print((assistant.thread._thread.id))

new_prompt = assistant.prompt
prompt_msg = new_prompt.create_prompt(file=file)

# Clear all messages in the thread.
assistant.thread.clear_messages()

new_message = assistant.thread.add_message(
    role="user",
    message=prompt_msg,
    attachment=[
        {
            "file_id": file.file_id,
            "tools": [
                {
                    "type": "file_search"
                }
            ]
        }
    ]
)


run = assistant.thread.create_and_poll_run(assistant_id=assistant.assistant.id)
assistant.thread.poll_run_status(run=run)

all_msgs = assistant.thread.grab_messages()

for msg in all_msgs:

    if msg.role == "assistant":
        print(msg.content[0].text.value)

