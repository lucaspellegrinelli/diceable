type MessageType = {
    user: string;
    event: string;
    events: string[];
};

const areArraysEqual = (a: string[] | undefined, b: string[] | undefined) => {
    if (!a || !b) {
        return false;
    }

    const sortedA = [...a].sort();
    const sortedB = [...b].sort();
    return JSON.stringify(sortedA) === JSON.stringify(sortedB);
};

export const assetMessageParser = (callback: (extra?: Record<string, any>) => void) => {
    let recievedEvents: string[] = [];
    let expectedEvents: string[] | undefined = undefined;

    return (message: MessageType, extra: Record<string, any>) => {
        const alreadyRecievedEvent = recievedEvents.includes(message.event);
        const nonExpectedEvent =
            expectedEvents !== undefined && !expectedEvents.includes(message.event);
        const differentExpectedEvents =
            expectedEvents !== undefined && !areArraysEqual(expectedEvents, message.events);
        if (alreadyRecievedEvent || nonExpectedEvent || differentExpectedEvents) {
            recievedEvents = [];
            expectedEvents = undefined;
        }

        if (expectedEvents === undefined) {
            expectedEvents = message.events;
        }

        recievedEvents.push(message.event);

        const allEventsRecieved =
            expectedEvents && expectedEvents.every((event) => recievedEvents.includes(event));

        if (allEventsRecieved) {
            callback(extra);
            recievedEvents = [];
            expectedEvents = undefined;
        }
    };
};
