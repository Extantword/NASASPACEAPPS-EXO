// src/WSClient.tsx
import React, { useEffect, useState } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';

type Direction = 'in' | 'out' | 'system';

type LogEntry = {
  dir: Direction;
  data: string;
  ts: number;
};

interface WSClientProps {
  url?: string;
}

export default function WSClient({ url = 'ws://localhost:8080' }: WSClientProps) {
  const [input, setInput] = useState<string>('');
  const [history, setHistory] = useState<LogEntry[]>([]);
  const [autoReconnect, setAutoReconnect] = useState<boolean>(true);

  // helper to add entries to the log (tipado)
  function pushLog(dir: Direction, data: string) {
    const entry: LogEntry = { dir, data, ts: Date.now() };
    setHistory((prev) => {
      // keep last 200
      const next = [...prev.slice(-199), entry];
      return next;
    });
  }

  // useWebSocket hook with typed onError handling
  const { sendMessage, lastMessage, readyState, getWebSocket } = useWebSocket(url, {
    onOpen: () => pushLog('system', 'Connected'),
    onClose: () => pushLog('system', 'Disconnected'),
    onError: (ev: Event) => {
      // Event might be an ErrorEvent in some browsers (has message), otherwise fallback
      let errMsg = 'socket error';
      if (ev instanceof ErrorEvent) {
        errMsg = ev.message;
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      } else if ((ev as any)?.message) {
        // some environments might attach message; fallback to any
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        errMsg = (ev as any).message;
      } else {
        // for debugging you can inspect the event object
        // console.error('WebSocket error event:', ev);
      }
      pushLog('system', 'Error: ' + errMsg);
    },
    shouldReconnect: () => autoReconnect,
    reconnectAttempts: 10,
    reconnectInterval: 3000,
    share: true,
  });

  // handle incoming messages
  useEffect(() => {
    if (!lastMessage) return;
    const text = lastMessage.data;
    try {
      const obj = JSON.parse(text);
      pushLog('in', JSON.stringify(obj));
    } catch {
      pushLog('in', text);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lastMessage]);

  function sendText() {
    if (!input) return;
    try {
      // try to parse as JSON and send canonical JSON
      const parsed = JSON.parse(input);
      const s = JSON.stringify(parsed);
      sendMessage?.(s);
      pushLog('out', `JSON: ${s}`);
    } catch {
      sendMessage?.(input);
      pushLog('out', input);
    }
    setInput('');
  }

  function sendJson(obj: unknown) {
    const s = JSON.stringify(obj);
    sendMessage?.(s);
    pushLog('out', s);
  }

  const connectionStatus = {
    [ReadyState.CONNECTING]: 'Connecting',
    [ReadyState.OPEN]: 'Open',
    [ReadyState.CLOSING]: 'Closing',
    [ReadyState.CLOSED]: 'Closed',
    [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
  }[readyState];

  return (
    <div style={{ fontFamily: 'Inter, system-ui, sans-serif', maxWidth: 900, margin: 12 }}>
      <h3>react-use-websocket — cliente (TypeScript)</h3>
      <div><strong>Status:</strong> {connectionStatus}</div>

      <div style={{ marginTop: 10 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder='Texto o JSON (ej: {"type":"ping"})'
          style={{ width: '60%' }}
        />
        <button onClick={sendText} style={{ marginLeft: 8 }}>Enviar</button>
        <button onClick={() => sendJson({ type: 'ping', ts: Date.now() })} style={{ marginLeft: 8 }}>
          Enviar ping JSON
        </button>
        <label style={{ marginLeft: 12 }}>
          <input type="checkbox" checked={autoReconnect} onChange={(e) => setAutoReconnect(e.target.checked)} />
          AutoReconnect
        </label>
      </div>

      <div style={{ marginTop: 14 }}>
        <strong>Logs (últimos 200)</strong>
        <div style={{ height: 320, overflow: 'auto', background: '#0b1220', color: '#dbeafe', padding: 10, borderRadius: 6 }}>
          {history.map((h, i) => (
            <div key={i} style={{ fontSize: 13, opacity: h.dir === 'system' ? 0.85 : 1 }}>
              <small style={{ color: h.dir === 'in' ? '#7ee787' : h.dir === 'out' ? '#7fb3ff' : '#ffea7f' }}>
                [{h.dir}] {new Date(h.ts).toLocaleTimeString()}:
              </small>
              <div style={{ marginLeft: 6 }}>{h.data}</div>
            </div>
          ))}
        </div>
      </div>

      <div style={{ marginTop: 10 }}>
        <button
          onClick={() => {
            const ws = getWebSocket?.();
            if (ws) {
              pushLog('system', `readyState=${ws.readyState}`);
            } else {
              pushLog('system', 'no websocket object');
            }
          }}
        >
          Inspect socket
        </button>
      </div>
    </div>
  );
}
