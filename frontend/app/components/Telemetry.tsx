'use client'
import {useState, useEffect} from 'react';
import {api, ws} from '../lib/api'

export default function Telemetry() {
    const [telemetry, setTelemetry] = useState({
        battery: 100,
        altitude: 0,
        latitude: 0,
        longtitude: 0,
        speed: 0,
        heading: 0
   
    });

    useEffect(() => {
        const handleMessage = (event: MessageEvent) => {
            try{
                const data  = JSON.parse(event.data);
                if (data.type === 'telemetry') {
                    setTelemetry({
                        battery: data.data.battery,
                        altitude: data.data.altitude,
                        latitude: data.data.latitude,
                        longtitude: data.data.longtitude,
                        speed: data.data.speed,
                        heading: data.data.heading
                    });
                }
            } catch (e) {
                console.log('Error bos parsing websocket data e', e);
            }
        };

        ws.addEventListener('message', handleMessage);
        return () => ws.removeEventListener('message', handleMessage)
    }, [])

    return (
        <div className='flex gap-4 p-4 bg-red-300 rounded-lg'>
            <div>
                <h3 className='font-bold text-lg mb2'>Battery</h3>
                <div className='text-2xl'>{telemetry.battery}%</div>
            </div>
            <div>
                <h3 className='font-bold text-lg mb2'>Altitude</h3>
                <div className='text-2xl'>{telemetry.altitude} m</div>
            </div>
            <div>
                <h3 className='font-bold text-lg mb2'>Latitude</h3>
                <div className='text-2xl'>{telemetry.latitude.toFixed(6)}</div>
            </div>
            <div>
                <h3 className='font-bold text-lg mb2'>Longtitude</h3>
                <div className='text-2xl'>{telemetry.longtitude.toFixed(6)}</div>
            </div>
        </div>
    )
}