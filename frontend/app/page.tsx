"use client"
// frontend/src/app/page.tsx
import dynamic from 'next/dynamic';
import Telemetry from './components/Telemetry';
import MissionForm from './components/missionForm';

const DroneMap = dynamic(() => import('./components/Map'), {
  ssr: false,
  loading: () => <p>sek cak loading...</p>
})

export default function Home() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">VTOL Drone Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <Telemetry />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="md:col-span-2">
          <DroneMap />
        </div>
        <div>
          <MissionForm />
        </div>
      </div>
    </div>
  );
}