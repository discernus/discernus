/**
 * Terminal Logger Service
 * Sends debug events to the development server terminal for visibility
 */



class TerminalLogger {
  private isDebugMode = false;
  private eventQueue: any[] = [];
  private maxQueueSize = 100;

  // Window interface for global access
  private initializeWindow() {
    if (typeof window !== 'undefined') {
      (window as any).debugMonitor = {
        enableDebugMode: () => this.setDebugMode(true),
        disableDebugMode: () => this.setDebugMode(false),
        getEventQueue: () => this.eventQueue,
        clearEventQueue: () => this.clearEventQueue()
      };
    }
  }

  constructor() {
    this.initializeWindow();
    this.overrideConsole();
  }

  private setDebugMode(enabled: boolean) {
    this.isDebugMode = enabled;
    if (enabled) {
      this.log('Debug mode enabled - Terminal logging active');
    }
  }

  private clearEventQueue() {
    this.eventQueue = [];
  }

  // Override console methods to capture logs
  private overrideConsole() {
    const originalConsole = { ...console };
    
    ['log', 'warn', 'error', 'info', 'debug'].forEach((method) => {
      (console as any)[method] = (...args: any[]) => {
        // Call original console method
        (originalConsole as any)[method](...args);
        
        if (this.isDebugMode) {
          this.addToQueue({
            type: 'console',
            method,
            args,
            timestamp: Date.now()
          });
        }
      };
    });
  }

  private addToQueue(event: any) {
    this.eventQueue.push(event);
    if (this.eventQueue.length > this.maxQueueSize) {
      this.eventQueue.shift();
    }
  }

  public log(message: string, data?: any) {
    if (this.isDebugMode) {
      console.log(`[DEBUG] ${message}`, data || '');
      this.addToQueue({
        type: 'debug',
        message,
        data,
        timestamp: Date.now()
      });
    }
  }

  public logAPICall(endpoint: string, method: string, data?: any) {
    if (this.isDebugMode) {
      console.log(`[API] ${method} ${endpoint}`, data || '');
      this.addToQueue({
        type: 'api',
        endpoint,
        method,
        data,
        timestamp: Date.now()
      });
    }
  }

  public logError(error: any, context?: string) {
    if (this.isDebugMode) {
      console.error(`[ERROR] ${context || 'Unknown context'}:`, error);
      this.addToQueue({
        type: 'error',
        error: error.toString(),
        context,
        timestamp: Date.now()
      });
    }
  }

  public isEnabled() {
    return this.isDebugMode;
  }
}

export default new TerminalLogger();