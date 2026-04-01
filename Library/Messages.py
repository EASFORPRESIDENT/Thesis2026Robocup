from torch.multiprocessing import Queue as MPQueue
from typing import Any

class Message:
    def __init__(self, agent_id: int, content: Any):
        self.agent_id = agent_id
        self.content = content
    
class MessageQueue:
    def __init__(self):
        self.queue = MPQueue()

    def send_message(self, message: Message):
        self.queue.put(message)

    def receive_message(self) -> Message:
        return self.queue.get()