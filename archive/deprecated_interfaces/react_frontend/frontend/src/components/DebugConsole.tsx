import React, { useState, useEffect } from 'react';
import debugMonitor from '../services/debugMonitor';

const DebugConsole: React.FC = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [events, setEvents] = useState<any[]>([]);
  const [filter, setFilter] = useState<string>('all');

  useEffect(() => {
    if (isVisible) {
      // Get initial events
      setEvents(debugMonitor.getEvents());
      
      // Set up polling for new events (simplified approach)
      const interval = setInterval(() => {
        setEvents(debugMonitor.getEvents());
      }, 1000);

      return () => clearInterval(interval);
    }
  }, [isVisible]);

  const toggleVisibility = () => {
    setIsVisible(!isVisible);
    if (!isVisible) {
      debugMonitor.enableDebugMode();
    }
  };

  const clearEvents = () => {
    debugMonitor.clearEvents();
    setEvents([]);
  };

  const exportData = () => {
    const data = {
      timestamp: new Date().toISOString(),
      events: debugMonitor.getEvents(),
      stats: debugMonitor.getEventStats()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `debug-data-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const filteredEvents = events.filter(event => {
    if (filter === 'all') return true;
    return event.type === filter;
  });

  const eventTypes = ['all', 'debug', 'api', 'error', 'component', 'user'];

  if (!isVisible) {
    return (
      <button
        onClick={toggleVisibility}
        className="fixed bottom-4 left-4 bg-blue-600 text-white px-3 py-2 rounded-md text-sm hover:bg-blue-700 z-50"
        title="Open Debug Console"
      >
        🐛 Debug
      </button>
    );
  }

  return (
    <div className="fixed bottom-4 left-4 w-96 h-80 bg-white border border-gray-300 rounded-lg shadow-lg z-50 flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-3 border-b border-gray-200 bg-gray-50 rounded-t-lg">
        <h3 className="text-sm font-medium text-gray-900">Debug Console</h3>
        <div className="flex items-center space-x-2">
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="text-xs border border-gray-300 rounded px-2 py-1"
          >
            {eventTypes.map(type => (
              <option key={type} value={type}>
                {type.charAt(0).toUpperCase() + type.slice(1)}
              </option>
            ))}
          </select>
          <button
            onClick={clearEvents}
            className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded hover:bg-red-200"
          >
            Clear
          </button>
          <button
            onClick={exportData}
            className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded hover:bg-green-200"
          >
            Export
          </button>
          <button
            onClick={toggleVisibility}
            className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded hover:bg-gray-200"
          >
            ✕
          </button>
        </div>
      </div>

      {/* Events List */}
      <div className="flex-1 overflow-y-auto p-2 space-y-1">
        {filteredEvents.length === 0 ? (
          <div className="text-xs text-gray-500 text-center py-4">
            No events to display
          </div>
        ) : (
          filteredEvents.slice(-50).reverse().map((event, index) => (
            <div
              key={event.id || index}
              className={`text-xs p-2 rounded border-l-2 ${
                event.type === 'error' ? 'bg-red-50 border-red-400' :
                event.type === 'api' ? 'bg-blue-50 border-blue-400' :
                event.type === 'user' ? 'bg-green-50 border-green-400' :
                'bg-gray-50 border-gray-400'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-medium text-gray-900">{event.type}</span>
                <span className="text-gray-500">
                  {new Date(event.timestamp).toLocaleTimeString()}
                </span>
              </div>
              <div className="text-gray-700 mt-1">{event.message}</div>
              {event.data && (
                <div className="text-gray-600 mt-1 text-xs">
                  {JSON.stringify(event.data, null, 1).substring(0, 100)}...
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Footer */}
      <div className="p-2 border-t border-gray-200 bg-gray-50 rounded-b-lg">
        <div className="text-xs text-gray-600">
          {filteredEvents.length} events • Debug mode: {debugMonitor.isDebugEnabled() ? 'ON' : 'OFF'}
        </div>
      </div>
    </div>
  );
};

export default DebugConsole; 