// frontend/src/components/Telemetry.tsx
import { useState, useEffect } from 'react';
import { api, ws } from '../lib/api';

// Fungsi helper untuk warna badge mode
const getModeColor = (mode: string) => {
  switch (mode) {
    case 'AUTO': return 'bg-green-500 text-white';
    case 'MANUAL': 
    case 'STABILIZE': return 'bg-blue-500 text-white';
    case 'RTL': return 'bg-red-500 text-white';
    case 'HOLD': return 'bg-yellow-500 text-black';
    default: return 'bg-gray-500 text-white';
  }
};

export default function Telemetry() {
  const [telemetry, setTelemetry] = useState({
    battery: 100,
    altitude: 0,
    latitude: 0,
    longitude: 0,
    speed: 0,
    heading: 0,
    flight_mode: 'STABILIZE'
  });

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'telemetry') {
          setTelemetry({
            battery: data.data.battery,
            altitude: data.data.altitude,
            latitude: data.data.latitude,
            longitude: data.data.longitude,
            speed: data.data.speed,
            heading: data.data.heading,
            flight_mode: data.data.flight_mode
          });
        }
      } catch (e) {
        console.error('Error parsing WebSocket data', e);
      }
    };

    ws.addEventListener('message', handleMessage);
    return () => ws.removeEventListener('message', handleMessage);
  }, []);

  const handleModeChange = async (newMode: string) => {
    try {
      await api.post('/mission/mode', null, { params: { mode: newMode } });
      // Catatan: Di implementasi nyata, kita mungkin perlu menunggu konfirmasi dari WebSocket
    } catch (error) {
      console.error('Failed to change mode', error);
    }
  };

  return (
    <div className="p-4 bg-gray-800 text-white shadow-lg">
      <div className="flex justify-between items-center mb-4">
        <h3 className="font-bold text-xl">Telemetry</h3>
        <span className={`px-3 py-1 rounded-full font-bold text-sm ${getModeColor(telemetry.flight_mode)}`}>
          {telemetry.flight_mode}
        </span>
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-gray-400 text-sm">Battery</p>
          <p className="text-2xl font-mono">{telemetry.battery}%</p>
        </div>
        <div>
          <p className="text-gray-400 text-sm">Altitude</p>
          <p className="text-2xl font-mono">{telemetry.altitude} m</p>
        </div>
        <div>
          <p className="text-gray-400 text-sm">Speed</p>
          <p className="text-2xl font-mono">{telemetry.speed} m/s</p>
        </div>
        <div>
          <p className="text-gray-400 text-sm">Heading</p>
          <p className="text-2xl font-mono">{telemetry.heading}°</p>
        </div>
      </div>

      {/* Software Override Buttons (Backup untuk RC Fisik) */}
      <div className="mt-6 pt-4 border-t border-gray-700">
        <p className="text-xs text-gray-400 mb-2">SOFTWARE OVERRIDE (Backup)</p>
        <div className="flex gap-2">
          <button 
            onClick={() => handleModeChange('STABILIZE')}
            className="flex-1 bg-blue-600 hover:bg-blue-700 py-2 rounded text-sm font-bold"
          >
            MANUAL
          </button>
          <button 
            onClick={() => handleModeChange('AUTO')}
            className="flex-1 bg-green-600 hover:bg-green-700 py-2 rounded text-sm font-bold"
          >
            AUTO
          </button>
          <button 
            onClick={() => handleModeChange('RTL')}
            className="flex-1 bg-red-600 hover:bg-red-700 py-2 rounded text-sm font-bold"
          >
            RTL
          </button>
        </div>
      </div>
    </div>
  );
}