import React from 'react';
import axios from 'axios';

export default function VirtualAttackControl(){
  const start = async () => {
    try{ await axios.post('http://localhost:8000/simulate/start', null, {params:{interval:1.0}}); }catch(e){console.error(e)}
  };
  const stop = async () => {
    try{ await axios.post('http://localhost:8000/simulate/stop'); }catch(e){console.error(e)}
  };
  return (
    <div className="bg-[#071019] p-4 rounded shadow">
      <h2 className="text-lg font-semibold">Virtual Attack Simulator</h2>
      <div className="mt-2 space-x-2">
        <button onClick={start} className="px-3 py-1 bg-cyan-500 rounded">Start</button>
        <button onClick={stop} className="px-3 py-1 bg-gray-600 rounded">Stop</button>
      </div>
    </div>
  )
}
