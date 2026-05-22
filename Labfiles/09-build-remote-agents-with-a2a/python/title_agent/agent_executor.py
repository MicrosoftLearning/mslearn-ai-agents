""" Azure AI Foundry Agent that generates a title """

from a2a.server.events.event_queue import EventQueue
from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.tasks import TaskUpdater
from a2a.utils import new_agent_text_message
from a2a.types import AgentCard, Part, TaskState
from title_agent.agent import TitleAgent, create_foundry_title_agent

class FoundryAgentExecutor(AgentExecutor):

    def __init__(self, card: AgentCard):
        self._card = card
        self._foundry_agent: TitleAgent | None = None

    async def _get_or_create_agent(self) -> TitleAgent:
        if not self._foundry_agent:
            self._foundry_agent = await create_foundry_title_agent()
        return self._foundry_agent

    async def _process_request(self, message_parts: list[Part], context_id: str, task_updater: TaskUpdater) -> None:
        # Process a user request through the Foundry agent

        try:
            # Retrieve message from A2A parts
            user_message = message_parts[0].root.text

            # Get the title agent


            # Update the task status
            

            # Run the agent conversation
            

            # Update the task with the responses
            

            # Mark the task as complete
            

        except Exception as e:
            print(f'Title Agent: Error processing request - {e}')
            await task_updater.failed(
                message=new_agent_text_message("Title Agent failed to process the request.", 
                context_id=context_id)
            )

    async def execute(self, context: RequestContext, event_queue: EventQueue,):
       
        # Create task updater
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        await updater.submit()

        # Start working
        await updater.start_work()

        # Process the request
        

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        print(f'Title Agent: Cancelling execution for context {context.context_id}')

        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        await updater.failed(
            message=new_agent_text_message('Task cancelled by user', context_id=context.context_id)
        )

def create_foundry_agent_executor(card: AgentCard) -> FoundryAgentExecutor:
    return FoundryAgentExecutor(card)

