// frontend/src/components/Map.tsx
"use client"; // <-- WAJIB: Memberitahu Next.js ini adalah Client Component

import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css'; // <-- WAJIB: Import CSS Leaflet
import L from 'leaflet';
import { ws } from '../lib/api';

// FIX: Memperbaiki icon default Leaflet yang hilang di Next.js
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

export default function DroneMap() {
  const [position, setPosition] = useState<[number, number]>([-6.200000, 106.816666]);
  const [flightMode, setFlightMode] = useState("DISARMED");

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data.type === 'telemetry') {
          setPosition([data.data.latitude, data.data.longitude]);
          setFlightMode(data.data.flight_mode);
        }
      } catch (e) {
        console.error('Error parsing WebSocket data', e);
      }
    };

    ws.addEventListener('message', handleMessage);
    return () => ws.removeEventListener('message', handleMessage);
  }, []);

  return (
    <div className="h-[500px] w-full rounded-lg overflow-hidden border-2 border-gray-700 z-0">
      <MapContainer 
        center={position} 
        zoom={16} 
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={position}>
          <Popup>
            Drone Position<br />Mode: {flightMode}
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}