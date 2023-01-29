# Eventful

Eventful is a hybrid messaging + HTTP server that drives events and event response state-tracking in AI Hero. HTTP endpoints are used to subscribe to event types for each Superpower which can be triggered through the UI or from updates to the data. Once triggered, Eventful sends the event for the Superpower to the subscribers on the channel they were asked to listen to.

More specifically, Eventful works like this:

1. Subscribe Request - Any microservices interested in listening to an event (e.g. for a Superpower or a UI event) subscribe by providing the event type with an HTTP request. It also mentions how it is interested in listening to the events - using a webhook (if the microservcice is HTTP) or a queue (if the microservice is a message queue listener).
2. Subscription Details in Response - Eventful's response for this HTTP request is confirmation of the subscription. It creates the topic if it doesn't exist and returns the details for listening to the topic back to the subscriber.
3. Start listening - For webhooks, the subscriber listens for HTTP calls. For message-queue based listeners, the subscriber then opens a connection to the event queue. Our message queues are currently implemented with Redis for each consumer group for an event type, but can be Kafka in the future.
4. Triggers and Forwards - When an event is triggered, Eventful pulls up its list of listeners for each consumer group, and sends the event payload with headers (e.g. Authorization, event-chain identifier, previous event identifier, etc.) to the webhook or the message queue.

# Looking for Contributors

We've open-sourced Eventful, and are interested in using it we are also looking for contributors. We want to make Eventful more robust:

- Create a `pip` installable library for subscribers.
- If there are no listeners, the topic for the event type can be deleted.
- Eventful could also set pod requirements to 0.
