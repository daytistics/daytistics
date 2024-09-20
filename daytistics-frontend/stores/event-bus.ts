import { defineStore } from 'pinia';

type EventPayload = any;

type EventTypes = 'user-login';

type Payloads = {
    'user-login': {};
};

interface EventBusState {
    events: Record<string, ((payload: EventPayload) => void)[]>;
}

export const useEventBusStore = defineStore('eventBus', {
    state: (): EventBusState => ({
        events: {},
    }),
    actions: {
        // Subscribe to an event
        on(
            event: EventTypes,
            callback: (payload: Payloads[typeof event]) => void
        ) {
            if (!this.events[event]) {
                this.events[event] = [];
            }
            this.events[event].push(callback);
        },

        // Emit an event
        emit(event: string, payload?: EventPayload) {
            const eventListeners = this.events[event];
            if (eventListeners) {
                eventListeners.forEach((callback) => callback(payload));
            }
        },

        // Unsubscribe from an event
        off(event: string, callback: (payload: EventPayload) => void) {
            if (!this.events[event]) return;

            this.events[event] = this.events[event].filter(
                (cb) => cb !== callback
            );
        },
    },
});
