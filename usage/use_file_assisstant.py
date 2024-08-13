from configparser import ConfigParser

from finbrain.client import FinBrainAssistant

# Path to the configuration file.
config = ConfigParser()
config.read('configs/config.ini')
api_key = config['openai_keys']['openai_secret_key']

# Initialize the FinBrainAssistant object.
assistant = FinBrainAssistant(
    api_key=api_key,
    save_state=True,
    state_file="state.json"
)

# Grab the Save State attribute.
print(assistant.save_state)

# Grab the State File attribute.
print(assistant.state_file)

# Grab the State attribute.
print(assistant.state)

# Add some files to the assistant.
assistant.files.add(file_path="sec_docs/13567242.html")
assistant.files.add(file_path="sec_docs/14564912.html")

# List all the files.
print(assistant.files.list_files())

# Grab a file by name.
file = assistant.files.get_by_name(name="14564912.html")

# Upload the file.
file.upload()

# Print the thread ID.
print(assistant.thread._thread.id)

# Create a prompt message.
new_prompt = assistant.prompt
prompt_msg = new_prompt.create_prompt(file=file)

# Clear all messages in the thread.
assistant.thread.clear_messages()

# Add a new message to the thread.
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

# Create a new run.
run = assistant.thread.create_run()

# Poll the run status.
assistant.thread.poll_run_status()

# Grab all the messages.
all_msgs = assistant.thread.grab_messages()

# Print the assistant messages.
for msg in all_msgs:
    if msg.role == "assistant":
        print(msg.content[0].text.value)
