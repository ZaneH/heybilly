
import os
from openai import OpenAI
from src.graph.action_node import ActionNode

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class UserTextPromptNode(ActionNode):
    create_queue = False
    is_blocking = True

    async def execute(self, input_data=None):
        pass

    def validate_inputs(self) -> bool:
        """
        Validate that text was provided in the data field
        """
        if 'text' not in self.data:
            return False

        return True


class UserTextPromptHelper:
    """
    Helper class for UserTextPromptNode.
    """

    SYSTEM_PROMPT = """### System Prompt Template:

```json
{
    "user_input": "User's spoken text here",
    "state": "Current state here",
    "working_input": "Current value of the text field"
}
```

### Expected Response Format:

```json
{
    "next_state": "Next state based on user input",
    "working_input": "Updated value of the text field, if applicable",
    "response_text": "Text to be read out loud or instructions, if applicable"
}
```

### System Prompt Logic:

1. **Handle `CANCEL` State**: If the user wants to cancel, confirm the cancellation.
   - If the current state is `NONE` and the user says something like "cancel", set the state to `CANCEL`.
   - If the state is `CANCEL` and the user confirms cancellation, set the state to `CANCEL_OK` and end the interaction.

2. **Handle `CONFIRM` State**: If the user wants to confirm, verify the confirmation.
   - If the current state is `NONE` and the user says something like "confirm", set the state to `CONFIRM`.
   - If the current state is CONFIRM, check the user's input. Transition to CONFIRM_OK only if the input explicitly indicates confirmation (like "yes" or "confirm"). For any unrelated input, switch back to NONE to handle it as a new request or query.

3. **Handle `NONE` State**: The default state, pass off to a fine-tuned model or handle general requests.
   - If the state is `NONE`, process the user's input normally, possibly updating the `working_input`.

4. **Handle `REPEAT` State**: Repeat the working input or current information.
   - If the user says "repeat", read the `working_input` out loud.

5. **Handle `SET` State**: Update the working input based on the user's spoken text.
   - If the user intends to update the text field, capture the new text and update the `working_input`.

Incoming data:
```json
{"user_input": "Nevermind, read it back", "state": "CONFIRM", "working_input": "Anyone else thinking about dogs this morning?"}
```"""

    def __init__(self):
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
