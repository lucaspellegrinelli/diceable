// Browser-compatible Loki logger
interface LokiLog {
    streams: LokiStream[];
}

interface LokiStream {
    stream: { [key: string]: string };
    values: string[][];
}

interface LokiConfig {
    url?: string;
    username?: string;
    password?: string;
}

class BrowserLokiLogger {
    private lokiUrl: string;
    private username: string;
    private password: string;
    private labels: { [key: string]: string };

    constructor(config?: LokiConfig) {
        this.lokiUrl = config?.url || '';
        this.username = config?.username || '';
        this.password = config?.password || '';
        this.labels = {
            service: 'frontend',
            namespace: 'diceable',
            environment: 'production'
        };
    }

    private async sendToLoki(level: string, message: string, meta?: any): Promise<void> {
        // Skip Loki if password is not set
        if (!this.password) {
            return;
        }

        const timestamp = (Date.now() * 1000000).toString(); // nanoseconds

        const logMessage = meta ? `${message} ${JSON.stringify(meta)}` : message;

        const stream: LokiStream = {
            stream: {
                ...this.labels,
                level: level
            },
            values: [[timestamp, logMessage]]
        };

        const payload: LokiLog = {
            streams: [stream]
        };

        try {
            const auth = btoa(`${this.username}:${this.password}`);

            await fetch(this.lokiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Basic ${auth}`
                },
                body: JSON.stringify(payload)
            });
        } catch (error) {
            console.error('Failed to send log to Loki:', error);
        }
    }

    info(message: string, meta?: any): void {
        console.info(`[INFO] ${message}`, meta || '');
        this.sendToLoki('info', message, meta);
    }

    error(message: string, error?: Error, meta?: any): void {
        const errorMeta = error ? {
            ...meta,
            error: error.message,
            stack: error.stack
        } : meta;

        console.error(`[ERROR] ${message}`, errorMeta || '');
        this.sendToLoki('error', message, errorMeta);
    }

    warn(message: string, meta?: any): void {
        console.warn(`[WARN] ${message}`, meta || '');
        this.sendToLoki('warn', message, meta);
    }

    debug(message: string, meta?: any): void {
        console.debug(`[DEBUG] ${message}`, meta || '');
        this.sendToLoki('debug', message, meta);
    }
}

// Create and export logger instance with default config
export const logger = new BrowserLokiLogger();

// Export convenience functions  
export const logInfo = (message: string, meta?: any) => logger.info(message, meta);
export const logError = (message: string, error?: Error, meta?: any) => logger.error(message, error, meta);
export const logWarn = (message: string, meta?: any) => logger.warn(message, meta);
export const logDebug = (message: string, meta?: any) => logger.debug(message, meta);

// Export factory function for configuring logger
export const createLogger = (config: LokiConfig) => new BrowserLokiLogger(config);

export default logger; 
