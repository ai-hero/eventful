import helpers.cache as cache_helper


class Subscriptions:
    @classmethod
    def subscribe(cls, event_type: str, listener: dict):
        listeners = cache_helper.get("event_subscribers", event_type)
        if not listeners:
            listeners = []
        listeners.append(listener)
        cache_helper.put("event_subscribers", event_type, listeners)

    @classmethod
    async def noitfy_event(cls, event_type: str):
        listeners = cache_helper.get("event_subscribers", event_type)
        if listeners:
            print(f"Should notify: {listeners}")

    @classmethod
    def waiting_on(cls, trace_id: str, event_type: str, listener: dict):
        event_listeners = cache_helper.get("trace_waiters", trace_id)
        if not event_listeners:
            event_listeners = {}
        if event_type not in event_listeners:
            event_listeners[event_type] = []
        event_listeners[event_type].append(listener)
        cache_helper.put("trace_waiters", trace_id, listener)

    @classmethod
    async def noitfy_trace_event(cls, trace_id: str, event_type: str):
        event_listeners = cache_helper.get("trace_waiters", trace_id)
        if event_listeners and event_type in event_listeners:
            listeners = event_listeners[event_type]
            print(f"Should notify: {listeners}")
