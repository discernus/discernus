import terminalLogger from './terminalLogger';

/**
 * Enhanced Debug Monitor - v2.1 Phase 1
 * Provides comprehensive debugging capabilities with terminal output
 */
export class DebugMonitor {
  private isEnabled = false;
  private eventQueue: DebugEvent[] = [];
  private maxEvents = 100;
  private performanceMarks: Map<string, number> = new Map();

  constructor() {
    this.setupGlobalHandlers();
  }

  private setupGlobalHandlers() {
    // Global error handler
    window.addEventListener('error', (event) => {
      this.logError(event.error, `Global Error: ${event.message}`);
    });

    // Unhandled promise rejection handler
    window.addEventListener('unhandledrejection', (event) => {
      this.logError(event.reason, 'Unhandled Promise Rejection');
    });
  }

  enableDebugMode() {
    this.isEnabled = true;
    terminalLogger.log('Debug Monitor enabled - Full event tracking active');
    this.addEvent('debug', 'Debug mode enabled', { timestamp: Date.now() });
  }

  disableDebugMode() {
    this.isEnabled = false;
    terminalLogger.log('Debug Monitor disabled');
  }

  private addEvent(type: string, message: string, data?: any) {
    if (!this.isEnabled) return;

    const event: DebugEvent = {
      id: `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
      timestamp: Date.now(),
      type,
      message,
      data
    };

    this.eventQueue.push(event);
    if (this.eventQueue.length > this.maxEvents) {
      this.eventQueue.shift();
    }
  }

  // Simplified logging methods
  logError(error: any, context?: string) {
    if (!this.isEnabled) return;
    
    const errorMessage = error?.message || error?.toString() || 'Unknown error';
    terminalLogger.logError(error, context);
    this.addEvent('error', `${context || 'Error'}: ${errorMessage}`, {
      error: errorMessage,
      context,
      stack: error?.stack
    });
  }

  logAPICall(method: string, url: string, status?: number, duration?: number, error?: string) {
    if (!this.isEnabled) return;
    
    const message = `API ${method} ${url}${status ? ` (${status})` : ''}${duration ? ` - ${duration}ms` : ''}`;
    terminalLogger.logAPICall(url, method, { status, duration, error });
    this.addEvent('api', message, { method, url, status, duration, error });
  }

  logPerformance(metric: string, value: number, unit: string, threshold?: number) {
    if (!this.isEnabled) return;
    
    const message = `Performance: ${metric} = ${value}${unit}${threshold ? ` (threshold: ${threshold}${unit})` : ''}`;
    terminalLogger.log(message);
    this.addEvent('performance', message, { metric, value, unit, threshold });
  }

  logComponentEvent(componentName: string, action: string, details?: any) {
    if (!this.isEnabled) return;
    
    const message = `${componentName}: ${action}`;
    terminalLogger.log(message, details);
    this.addEvent('component', message, { component: componentName, action, details });
  }

  logUserAction(action: string, details?: any) {
    if (!this.isEnabled) return;
    
    const message = `User: ${action}`;
    terminalLogger.log(message, details);
    this.addEvent('user', message, { action, details });
  }

  // Performance timing helpers
  startTiming(label: string) {
    if (!this.isEnabled) return;
    this.performanceMarks.set(label, performance.now());
  }

  endTiming(label: string, threshold?: number) {
    if (!this.isEnabled) return;
    
    const startTime = this.performanceMarks.get(label);
    if (startTime) {
      const duration = performance.now() - startTime;
      this.logPerformance(label, Math.round(duration), 'ms', threshold);
      this.performanceMarks.delete(label);
      return duration;
    }
    return null;
  }

  // Event queue access
  getEvents(): DebugEvent[] {
    return [...this.eventQueue];
  }

  clearEvents() {
    this.eventQueue = [];
    terminalLogger.log('Debug event queue cleared');
  }

  getEventStats() {
    const stats = this.eventQueue.reduce((acc, event) => {
      acc[event.type] = (acc[event.type] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return {
      total: this.eventQueue.length,
      types: stats,
      oldestEvent: this.eventQueue[0]?.timestamp,
      newestEvent: this.eventQueue[this.eventQueue.length - 1]?.timestamp
    };
  }

  isDebugEnabled(): boolean {
    return this.isEnabled;
  }
}

// Event interface
interface DebugEvent {
  id: string;
  timestamp: number;
  type: string;
  message: string;
  data?: any;
}

// Create singleton instance
export const debugMonitor = new DebugMonitor();

// Make it globally available
if (typeof window !== 'undefined') {
  (window as any).debugMonitor = debugMonitor;
}

export default debugMonitor; 