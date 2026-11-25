"""A2A executor that bridges incoming A2A messages to an Agent Framework agent."""

import logging
import uuid
from asyncio import CancelledError

from a2a.helpers import new_task_from_user_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import Part, TaskState
from agent_framework_hosting import AgentState
from agent_framework_hosting_a2a import a2a_from_run, a2a_to_run

logger = logging.getLogger(__name__)


class AgentFrameworkExecutor(AgentExecutor):
    """Receives A2A messages, runs the agent, and streams the reply back as A2A artifacts."""

    def __init__(self, state: AgentState) -> None:
        self.state = state

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        updater = TaskUpdater(event_queue, context.task_id or "", context.context_id or "")
        await updater.cancel()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.message is None or context.context_id is None:
            raise ValueError("A2A message and context id are required")

        # Register a new A2A task for this request, then report its progress through the updater
        task = context.current_task
        if task is None:
            task = new_task_from_user_message(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, context.context_id)
        await updater.submit()
        try:
            await updater.start_work()

            # Convert the A2A message into arguments for the Agent Framework agent

            agent = await self.state.get_target()
            session_id = f"a2a:{context.tenant}:{context.context_id}"
            session = await self.state.get_or_create_session(session_id)

            # Run the agent and stream each update back to the caller as an A2A artifact

            default_artifact_id = uuid.uuid4().hex
            streamed_artifact_ids: set[str] = set()
            async for update in stream:
                parts = a2a_from_run(update)
                if parts:
                    artifact_id = update.message_id or default_artifact_id
                    await updater.add_artifact(
                        parts=parts,
                        artifact_id=artifact_id,
                        append=True if artifact_id in streamed_artifact_ids else None,
                    )
                    streamed_artifact_ids.add(artifact_id)

            final_response = await stream.get_final_response()
            if not streamed_artifact_ids:
                parts = a2a_from_run(final_response)
                if parts:
                    await updater.add_artifact(parts=parts, artifact_id=default_artifact_id)
            await self.state.set_session(session_id, session)

            # Mark the task as complete

        except CancelledError:
            await updater.update_status(state=TaskState.TASK_STATE_CANCELED)
        except Exception:
            logger.exception("A2A agent execution failed.")
            await updater.update_status(
                state=TaskState.TASK_STATE_FAILED,
                message=updater.new_agent_message([Part(text="Agent execution failed.")]),
            )
