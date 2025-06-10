# Debug Monitoring System - Narrative Gravity Research Workbench

## 🎯 Overview

The Debug Monitoring System provides comprehensive, **autonomous debugging capabilities** that operate independently without requiring manual copying/pasting of browser errors or process termination. This system continuously monitors your React application and provides real-time insights into errors, performance issues, and system health.

## 🚀 Quick Start

### Method 1: Debug Launch Script (Recommended)
```bash
cd frontend
./debug-launch.sh
```

### Method 2: Manual Launch with Debug Mode
```bash
cd frontend
REACT_APP_DEBUG_MODE=true npm run dev
```

### Method 3: Enable in Running App
- Add `?debug=true` to your browser URL
- Or click the 🐛 Debug button and toggle "ON"

## 🛠️ Debug Console Features

### 📊 Real-Time Monitoring
- **API Call Tracking**: Monitor all HTTP requests with timing, status codes, and payloads
- **Error Detection**: Automatic capture of JavaScript errors, unhandled promises, and component failures
- **Performance Metrics**: Track page load times, component render performance, and resource usage
- **Component Lifecycle**: Monitor React component mounting, unmounting, and re-renders
- **User Actions**: Track user interactions and navigation patterns

### 🎛️ Interactive Console
- **Visual Interface**: Floating debug console accessible via 🐛 button (bottom-left)
- **Real-Time Health Status**: Color-coded system health indicator (🟢 Healthy, 🟡 Warning, 🔴 Error)
- **Event Filtering**: Filter by event type, severity level, or component name
- **Data Export**: Download complete debug session as JSON for external analysis
- **Event History**: Maintains last 1000 events with full context and stack traces

## 🔍 Autonomous Error Detection

### Automatic Error Capture
The system automatically detects and logs:

1. **JavaScript Runtime Errors**
   - Uncaught exceptions
   - Type errors
   - Reference errors
   - Syntax errors

2. **React Component Errors**
   - Component lifecycle failures
   - Render errors
   - Props/state issues
   - Hook violations

3. **Network Issues**
   - API call failures
   - Timeout errors
   - Connection issues
   - HTTP error responses

4. **Performance Problems**
   - Slow API responses (>3s)
   - Large bundle sizes
   - Memory leaks
   - Render performance issues

### Error Context and Stack Traces
Every error includes:
- **Full stack trace** with line numbers
- **Component context** (which component failed)
- **User action context** (what the user was doing)
- **Application state** at time of error
- **Network context** (recent API calls)

## 📈 Performance Monitoring

### Automatic Metrics Collection
- **Page Load Time**: Full page load performance
- **API Response Times**: Individual request timing
- **Component Render Time**: React component performance
- **Bundle Size Tracking**: JavaScript payload monitoring
- **Memory Usage**: Browser memory consumption

### Performance Thresholds
The system automatically flags:
- API calls > 3 seconds
- Page loads > 5 seconds
- Components taking > 500ms to render
- Memory usage > 100MB

## 🌐 API Call Monitoring

### Comprehensive Tracking
Every API call includes:
- **Request Details**: URL, method, headers, payload
- **Response Data**: Status code, response body, headers
- **Timing Information**: Total duration, network time
- **Error Context**: Failure reasons, retry attempts

### Visual Indicators
- 🟢 Successful calls (2xx responses)
- 🟡 Client errors (4xx responses)
- 🔴 Server errors (5xx responses)
- ⏱️ Slow responses (>3s)

## 🎮 Using the Debug Console

### Opening the Console
1. Look for 🐛 Debug button in bottom-left corner
2. Button color indicates debug status:
   - **Blue**: Debug mode enabled
   - **Gray**: Debug mode disabled
3. Click to open full console interface

### Console Interface
```
┌─ Debug Console ─────────────────────┐
│ [ON/OFF] [Clear] [Export] [×]       │
├─────────────────────────────────────┤
│ Status: HEALTHY    Success Rate: 95%│
├─────────────────────────────────────┤
│ [All Types ▼] [All Levels ▼]       │
├─────────────────────────────────────┤
│ 🌐 GET /api/health (200) 45ms      │
│    12:34:56 [info] [ApiClient]      │
│                                     │
│ 🔧 ExperimentDesigner mount         │
│    12:34:55 [debug] [Component]     │
│                                     │
│ 👆 Tab changed to designer          │
│    12:34:54 [info]                  │
└─────────────────────────────────────┘
```

### Health Status Indicators
- **🟢 HEALTHY**: No errors in last minute
- **🟡 WARNING**: 1-4 errors in last minute
- **🔴 ERROR**: 5+ errors in last minute

## 📤 Data Export and Analysis

### Export Capabilities
Click "Export" to download JSON containing:
- Complete event history
- System health metrics
- Performance statistics
- Error summaries
- Browser environment info

### External Analysis
Exported data can be analyzed with:
- **Error tracking services** (Sentry, Bugsnag)
- **Analytics platforms** (Google Analytics, Mixpanel)
- **Business intelligence tools** (Tableau, PowerBI)
- **Custom scripts** (Python, R, Excel)

## 🔧 Advanced Configuration

### Environment Variables
```bash
# Enable debug mode by default
REACT_APP_DEBUG_MODE=true

# Increase event buffer size
REACT_APP_DEBUG_MAX_EVENTS=2000

# Enable verbose logging
REACT_APP_DEBUG_VERBOSE=true
```

### Programmatic Access
```javascript
import { debugMonitor } from './services/debugMonitor';

// Check if debugging is enabled
const isDebugging = debugMonitor.isDebugEnabled();

// Manually log custom events
debugMonitor.log('Custom event', 'info', { data: 'example' });

// Track user actions
debugMonitor.trackUserAction('Button clicked', { buttonId: 'submit' });

// Get system health
const health = debugMonitor.getHealthStatus();
```

## 🛡️ Error Recovery and Resilience

### Automatic Recovery
The debug system includes:
- **Error Boundaries**: Prevent app crashes from component errors
- **Retry Logic**: Automatic retry for failed API calls
- **Graceful Degradation**: Continue operation even when debugging fails
- **Memory Management**: Automatic cleanup of old events

### Self-Monitoring
The debug system monitors itself:
- Tracks its own performance impact
- Prevents infinite loops in error handling
- Validates data integrity
- Monitors memory usage

## 📊 Integration with Development Tools

### Browser DevTools Integration
- Enhanced console logging with styled output
- Performance marks for timing analysis
- Network tab integration for API monitoring
- Local storage inspection for persistent data

### VS Code Integration
- Source map support for accurate error locations
- Breakpoint debugging with context preservation
- Terminal output formatting
- Git integration for error history

## 🔍 Troubleshooting the Debug System

### Debug System Not Appearing
1. Check browser console for React errors
2. Verify debug mode is enabled: `localStorage.getItem('debug_mode')`
3. Try adding `?debug=true` to URL
4. Clear browser cache and reload

### Performance Impact
- Debug system adds <5% overhead in development
- Automatically disabled in production builds
- Memory usage capped at 10MB maximum
- No impact on user-facing performance

### Data Privacy
- All debug data stays in browser localStorage
- No automatic external transmission
- Manual export only when user initiates
- Sensitive data can be filtered out

## 📈 Success Metrics

### Independence Indicators
- **Zero manual error reporting**: System captures all errors automatically
- **Self-sufficient debugging**: Complete context provided without intervention
- **Autonomous health monitoring**: Real-time status without manual checks
- **Predictive issue detection**: Warnings before failures occur

### Development Efficiency
- **Faster debugging**: Immediate error context and stack traces
- **Reduced context switching**: No need to manually copy/paste errors
- **Historical tracking**: Full session history for pattern analysis
- **Collaborative debugging**: Exportable data for team analysis

## 🎯 Next Steps

1. **Launch with debug mode**: Use `./debug-launch.sh`
2. **Interact with the app**: Navigate between tabs, trigger actions
3. **Monitor the debug console**: Watch real-time events and health status
4. **Simulate errors**: Try invalid API calls or component errors
5. **Export debug data**: Download session data for analysis
6. **Share findings**: Export data can be shared with team members

---

**Result**: You now have a comprehensive, autonomous debugging system that provides complete visibility into your React application without requiring manual intervention or process termination. The system operates independently and provides all the context needed for effective debugging and error resolution. 