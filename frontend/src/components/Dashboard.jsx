import React, {useEffect, useState, useRef} from 'react';
import AttackList from './AttackList';
import AttackDetails from './AttackDetails';
import VirtualAttackControl from './VirtualAttackControl';

export default function Dashboard(){
  const [events, setEvents] = useState([]);
  const [selected, setSelected] = useState(null);
  const wsRef = useRef(null);

  useEffect(()=> {
    const ws = new WebSocket('ws://localhost:8000/ws');
    wsRef.current = ws;
    ws.onopen = ()=> console.log('ws open');
    ws.onmessage = (ev)=> {
      try {
        const data = JSON.parse(ev.data);
        // if it's an echo ignore
        if (data.echo) return;
        setEvents(e => [data, ...e].slice(0,200)); // keep last 200
      } catch(e) { console.error(e) }
    };
    ws.onclose = ()=> console.log('ws closed');
    return ()=> { ws.close(); }
  }, []);

  return (
    <div className="grid grid-cols-3 gap-4">
      <div className="col-span-2">
        <div className="mb-4">
          <VirtualAttackControl />
        </div>
        <AttackList events={events} onSelect={setSelected} />
      </div>
      <div>
        <AttackDetails event={selected} />
      </div>
    </div>
  )
}
