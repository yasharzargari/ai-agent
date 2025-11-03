"""Communication protocols between agents"""


class MessageProtocol:
    """Protocol for inter-agent messages"""
    
    @staticmethod
    def create_message(sender: str, receiver: str, content: str, 
                      message_type: str = "task") -> dict:
        return {
            "sender": sender,
            "receiver": receiver,
            "content": content,
            "type": message_type
        }

    @staticmethod
    def create_task_message(sender: str, receiver: str, task: str) -> dict:
        return MessageProtocol.create_message(
            sender, receiver, task, "task"
        )

    @staticmethod
    def create_result_message(sender: str, receiver: str, result: str) -> dict:
        return MessageProtocol.create_message(
            sender, receiver, result, "result"
        )
