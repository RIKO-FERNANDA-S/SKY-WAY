
// frontend/src/components/Map.tsx
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet'; // Tambahkan ini untuk custom icon
import { useState, useEffect } from 'react';
import { ws } from '../lib/api';

delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Definisikan tipe data untuk Waypoint agar lebih rapi
interface Waypoint {
  latitude: number;
  longitude: number;
  active?: boolean;
}

export default function DroneMap() {
  // PERBAIKAN DI SINI: Tambahkan <[number, number]> agar TypeScript tahu ini adalah Tuple
  const [position, setPosition] = useState<[number, number]>([0, 6]);
  
  const [waypoints, setWaypoints] = useState<Waypoint[]>([]);

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data.type === 'telemetry') {
          // Pastikan data dari WebSocket valid sebelum di-set
          if (data.data.latitude && data.data.longitude) {
            setPosition([data.data.latitude, data.data.longitude]);
          }
        }
        
        if (data.type === 'waypoint_update') {
          // Update logic waypoint jika diperlukan
          // (Bisa di-expand nanti saat integrasi misi nyata)
        }
      } catch (e) {
        console.error('Error parsing WebSocket data', e);
      }
    };

    ws.addEventListener('message', handleMessage);
    return () => ws.removeEventListener('message', handleMessage);
  }, []);

  return (
    <div className="h-full rounded-lg overflow-hidden border border-gray-300">
      <MapContainer 
        center={position} 
        zoom={15} 
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        
        {/* Marker Posisi Drone */}
        <Marker position={position}>
          <Popup>
            <div className="text-center">
              <strong> Drone Position</strong><br />
              Lat: {position[0].toFixed(6)}<br />
              Lng: {position[1].toFixed(6)}
            </div>
          </Popup>
        </Marker>
        
        {/* Marker Waypoints (Contoh statis untuk visualisasi) */}
        {waypoints.map((wp, index) => (
          <Marker 
            key={index} 
            position={[wp.latitude, wp.longitude]}
          >
            <Popup>
              Waypoint {index + 1}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}