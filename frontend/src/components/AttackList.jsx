import React from 'react';

export default function AttackList({events, onSelect}){
  return (
    <div className="bg-[#071019] p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-3">Recent Events</h2>
      <div className="space-y-2 max-h-[60vh] overflow-auto">
        {events.map((ev, idx) => (
          <div key={idx} onClick={()=>onSelect(ev)} className="p-2 border-l-4 border-cyan-500 hover:bg-[#0a1a1f] cursor-pointer rounded">
            <div className="flex justify-between">
              <div className="font-semibold">{ev.attack_type || ev.label || 'event'}</div>
              <div className="text-sm">{new Date((ev.timestamp||Date.now())*1000).toLocaleTimeString()}</div>
            </div>
            <div className="text-sm text-gray-300">{ev.src_ip || ev.src || 'src'} → {ev.dst_ip || ev.dst || 'dst'}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
