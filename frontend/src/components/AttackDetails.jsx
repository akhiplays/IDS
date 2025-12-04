import React from 'react';

export default function AttackDetails({event}){
  if(!event) return <div className="bg-[#071019] p-4 rounded shadow">Select an event</div>;
  return (
    <div className="bg-[#071019] p-4 rounded shadow">
      <h3 className="text-lg font-semibold mb-2">Event Details</h3>
      <pre className="text-sm text-cyan-100">{JSON.stringify(event, null, 2)}</pre>
    </div>
  )
}
