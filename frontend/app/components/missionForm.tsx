// frontend/src/components/MissionForm.tsx
import { useState, useEffect } from 'react';
import { api } from '../lib/api';

export default function MissionForm() {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [waypoints, setWaypoints] = useState([
    { id: 1, latitude: -6.2, longitude: 106.8, altitude: 50 }
  ]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const response = await api.post('/mission', {
        name,
        description,
        waypoints
      });
      
      if (response.status === 201) {
        alert('Mission created successfully!');
        setName('');
        setDescription('');
        setWaypoints([{ id: 1, latitude: -6.2, longitude: 106.8, altitude: 50 }]);
      }
    } catch (error) {
      console.error('Error creating mission:', error);
      alert('Failed to create mission');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4 bg-gray-50 rounded-lg">
      <div>
        <label className="block mb-2">Mission Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
      </div>
      
      <div>
        <label className="block mb-2">Description</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full p-2 border rounded"
          rows={3}
        />
      </div>
      
      <div className="space-y-4">
        {waypoints.map((wp, index) => (
          <div key={wp.id} className="grid grid-cols-4 gap-4">
            <input
              type="number"
              value={wp.latitude}
              onChange={(e) => {
                const newWps = [...waypoints];
                newWps[index].latitude = parseFloat(e.target.value);
                setWaypoints(newWps);
              }}
              className="p-2 border rounded"
              placeholder="Latitude"
            />
            <input
              type="number"
              value={wp.longitude}
              onChange={(e) => {
                const newWps = [...waypoints];
                newWps[index].longitude = parseFloat(e.target.value);
                setWaypoints(newWps);
              }}
              className="p-2 border rounded"
              placeholder="Longitude"
            />
            <input
              type="number"
              value={wp.altitude}
              onChange={(e) => {
                const newWps = [...waypoints];
                newWps[index].altitude = parseFloat(e.target.value);
                setWaypoints(newWps);
              }}
              className="p-2 border rounded"
              placeholder="Altitude"
            />
            <button
              type="button"
              onClick={() => setWaypoints(waypoints.filter((_, i) => i !== index))}
              className="bg-red-500 text-white p-2 rounded"
            >
              Remove
            </button>
          </div>
        ))}
        
        <button
          type="button"
          onClick={() => setWaypoints([
            ...waypoints,
            { 
              id: waypoints.length + 1, 
              latitude: -6.2, 
              longitude: 106.8, 
              altitude: 50 
            }
          ])}
          className="bg-blue-500 text-white p-2 rounded"
        >
          Add Waypoint
        </button>
      </div>
      
      <button
        type="submit"
        className="bg-green-500 text-white p-2 rounded w-full"
      >
        Create Mission
      </button>
    </form>
  );
}