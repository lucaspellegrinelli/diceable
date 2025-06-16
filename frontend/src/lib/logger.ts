import winston from 'winston';
import LokiTransport from 'winston-loki';

// Get Loki configuration from environment variables
const lokiUrl = process.env.LOKI_URL || '';
const lokiUsername = process.env.LOKI_USERNAME || '';
const lokiPassword = process.env.LOKI_PASSWORD;

const transports: winston.transport[] = [
    // Console transport for development
    new winston.transports.Console({
        format: winston.format.combine(
            winston.format.colorize(),
            winston.format.simple()
        )
    })
];

// Only add Loki transport if password is provided
if (lokiPassword) {
    const lokiTransport = new LokiTransport({
        host: lokiUrl,
        basicAuth: `${lokiUsername}:${lokiPassword}`,
        labels: {
            service: 'frontend',
            namespace: 'diceable',
            environment: 'production'
        },
        json: true,
        format: winston.format.json(),
        replaceTimestamp: true,
        onConnectionError: (err: any) => console.error('Loki connection error:', err)
    });

    transports.push(lokiTransport);
} else {
    console.warn('LOKI_PASSWORD environment variable not set. Loki logging will be disabled.');
}

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json()
    ),
    transports: transports
});

// Wrapper functions for easier usage
export const logInfo = (message: string, meta?: any) => {
    logger.info(message, meta);
};

export const logError = (message: string, error?: Error, meta?: any) => {
    if (error) {
        logger.error(message, { ...meta, error: error.message, stack: error.stack });
    } else {
        logger.error(message, meta);
    }
};

export const logWarn = (message: string, meta?: any) => {
    logger.warn(message, meta);
};

export const logDebug = (message: string, meta?: any) => {
    logger.debug(message, meta);
};

export default logger; 
