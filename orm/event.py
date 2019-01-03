"""
事件循环
"""
import asyncio


class TriggerEvent(object):

    def __init__(self, table, field, action):
        self.table = table
        self.field = field
        self.action = action

    def __str__(self):
        return '_'.join([self.table, self.field, self.action])


class EventBus(object):
    def __init__(self):
        """
        事件总线
        """
        self._listeners = {}
        pass

    def publish(self, event: TriggerEvent,*args, **kwargs):
        """
        并发执行事件
        :param event:
        :param kwargs:
        :return:
        """
        listeners = self._listeners.get(str(event), None)
        if listeners:
            [l(event, *args, **kwargs) for l in listeners]

    def add_listener(self, event: TriggerEvent, func):
        if not self._listeners.get(str(event)):
            self._listeners[str(event)] = list()
        self._listeners[str(event)].append(func)


event_bus = EventBus()
