// Unified Loki sender that works in both server and browser environments
async function sendToLoki(level: string, message: string, metadata?: any) {
    // Check if we're in a server environment (Node.js)
    const isServer = typeof process !== 'undefined' && process.env;

    if (!isServer) {
        // In browser: Loki logging not supported (no secure way to get credentials)
        return;
    }

    const lokiUrl = process.env.LOKI_URL;
    const lokiUsername = process.env.TELEMETRY_USERNAME;
    const lokiPassword = process.env.TELEMETRY_PASSWORD;

    if (!lokiPassword) return;

    try {
        // Detect environment
        const isProduction = process.env.NODE_ENV === 'production';
        const environment = isProduction ? 'production' : 'development';

        const timestamp = (Date.now() * 1000000).toString();
        const allMetadata = metadata || {};
        const logMessage = Object.keys(allMetadata).length > 0 ? `${message} ${JSON.stringify(allMetadata)}` : message;

        const payload = {
            streams: [
                {
                    stream: {
                        service_name: 'frontend',
                        namespace: 'diceable',
                        environment: environment,
                        instance: 'cloud',
                        level: level
                    },
                    values: [[timestamp, logMessage]],
                },
            ],
        };

        const auth = Buffer.from(`${lokiUsername}:${lokiPassword}`).toString('base64');

        await fetch(lokiUrl!, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Basic ${auth}`
            },
            body: JSON.stringify(payload)
        });
    } catch (error) {
        // Silently fail - Loki logging is optional
    }
}

// Simple logging functions that log to console and Loki
export const logInfo = (message: string, meta?: any) => {
    console.info(`[INFO] ${message}`, meta || '');
    sendToLoki('info', message, meta);
};

export const logError = (message: string, error?: Error, meta?: any) => {
    const errorMeta = error ? { ...meta, error: error.message, stack: error.stack } : meta;
    console.error(`[ERROR] ${message}`, errorMeta || '');
    sendToLoki('error', message, errorMeta);
};

export const logWarn = (message: string, meta?: any) => {
    console.warn(`[WARN] ${message}`, meta || '');
    sendToLoki('warn', message, meta);
};

export const logDebug = (message: string, meta?: any) => {
    console.debug(`[DEBUG] ${message}`, meta || '');
    sendToLoki('debug', message, meta);
}; 
