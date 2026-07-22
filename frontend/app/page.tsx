"use client";
// frontend/src/app/page.tsx
import dynamic from "next/dynamic";
import Telemetry from "./components/Telemetry";
import MissionForm from "./components/missionForm";

const DroneMap = dynamic(() => import("./components/Map"), {
  ssr: false,
  loading: () => <p>sek cak loading...</p>,
});

export default function Home() {
  return (
    <main className="w-full h-screen ">
      <div className="w-full h-[10%] text-white font-bold flex justify-center items-center bg-black">
        <h1>SKY_WAY</h1>
      </div>

      <div className="flex w-full h-[90%]">
        <div className="w-[30%] flex flex-col h-full">
          <section className="bg-red-400 h-1/2">naik turun</section>
          <section className="bg-sky-400 h-1/2">
          <Telemetry/>
          </section>
        </div>
        <div className="w-[70%] bg-green-400">
          <DroneMap/>
        </div>
      </div>
    </main>
  );
}
