
from typing import Dict, List, Callable, Any
from enum import Enum
import inspect
from dataclasses import dataclass
from datetime import datetime

class EventType(Enum):
    MESSAGE = "message"
    TASK_START = "task_start"
    TASK_END = "task_end"
    AGENT_START = "agent_start"
    AGENT_END = "agent_end"
    ERROR = "error"
    CUSTOM = "custom"

@dataclass
class Event:
    type: EventType
    data: Dict[str, Any]
    sender: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class EventEmitter:
    def __init__(self):
        self._listeners: Dict[EventType, List[Callable]] = {}

    def on(self, event_type: EventType, listener: Callable):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def off(self, event_type: EventType, listener: Callable):
        if event_type in self._listeners:
            self._listeners[event_type].remove(listener)

    def emit(self, event: Event):
        listeners = self._listeners.get(event.type, [])
        for listener in listeners:
            try:
                if inspect.iscoroutinefunction(listener):
                    import asyncio
                    asyncio.create_task(listener(event))
                else:
                    listener(event)
            except Exception as e:
                error_event = Event(
                    type=EventType.ERROR,
                    data={"error": str(e), "original_event": event},
                    sender=self.__class__.__name__
                )
                self.emit(error_event)

class EventBus(EventEmitter):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

def register_agent_events(agent_class):
    """Decorator to add event emission to agent methods"""
    class EventWrappedAgent(agent_class):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.event_bus = EventBus()

        def process_request(self, request: str) -> str:
            self.event_bus.emit(Event(
                type=EventType.AGENT_START,
                data={"request": request},
                sender=self.__class__.__name__
            ))
            
            try:
                result = super().process_request(request)
                self.event_bus.emit(Event(
                    type=EventType.AGENT_END,
                    data={"result": result},
                    sender=self.__class__.__name__
                ))
                return result
            except Exception as e:
                self.event_bus.emit(Event(
                    type=EventType.ERROR,
                    data={"error": str(e)},
                    sender=self.__class__.__name__
                ))
                raise

    return EventWrappedAgent
