import React, { useEffect, useMemo, useState } from 'react';
import DeleteDairyDay from '../components/DeleteDairyDay.jsx';

export default function Deleteday({ apiBase }) {
  const endpoints = useMemo(() => ({
    list: `/api/pamietnik`,
    scan: `/scan-diary`,
    del: (id) => `/pamietnik/api/day_delete/${id}`,
  }), [apiBase]);

  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState('');
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState('');
  const [deleteMode, setDeleteMode] = useState(false);

  useEffect(() => {
    const ac = new AbortController();
    async function load() {
      setLoading(true);
      setError('');
      try {
        const res = await fetch(endpoints.list, {
          method: 'GET',
          credentials: 'same-origin',
          signal: ac.signal,
        });
        if (!res.ok) throw new Error(await res.text() || 'Błąd pobierania wpisów');
        const data = await res.json();
        setEntries(Array.isArray(data) ? data : []);
      } catch (err) {
        if (err.name !== 'AbortError') setError(err.message || 'Nieznany błąd');
      } finally {
        setLoading(false);
      }
    }
    load();
    return () => ac.abort();
  }, [endpoints.list]);

  const fetchEntries = async (q = '') => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${endpoints.list}?query=${encodeURIComponent(q)}`,{
        method: 'GET',
        credentials: 'same-origin',
    });
      if (!res.ok) throw new Error(await res.text() || "Błąd pobierania wpisów");
      const data = await res.json();
      setEntries(Array.isArray(data) ? data : []);

  } catch (err) {
      setError(err.message || 'Nieznany błąd');
  } finally {
    setLoading(false);
  }
  }
  useEffect(() => {
    fetchEntries();
  }, [endpoints.list]);
  
  async function scanDiary() {
    setScanning(true);
    setError('');
    try {
      const res = await fetch(endpoints.scan, { method: 'POST', credentials: 'same-origin' });
      if (!res.ok) throw new Error(await res.text() || 'Błąd skanowania');
      const data = await res.json();
      setEntries(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message || 'Nieznany błąd podczas skanowania');
    } finally {
      setScanning(false);
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Czy na pewno chcesz usunąć ten dzień?')) return;
    try {
      const res = await fetch(endpoints.del(id), { method: 'DELETE', credentials: 'same-origin' });
      if (!res.ok) throw new Error(await res.text() || 'Błąd usuwania wpisu');
      setEntries(prev => prev.filter(e => e.id !== id));
    } catch (err) {
      alert(err.message || 'Nie udało się usunąć dnia');
    }
  }

  
  return (
    <div>
      {/* Pole wyszukiawnia */}
      <input
        type='text'
        placeholder='Szukaj wpisów...'
        value={query}
        onChange={(e) => { 
          setQuery(e.target.value);
          fetchEntries(e.target.value);
        }}
      />
      <div className='notifications'>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {loading && <p>Ładowanie wpisów...</p>}
        {scanning && <p>Skanowanie pamiętnika...</p>}
      </div>
      <div className="buttons">
        <button onClick={scanDiary} disabled={scanning}>
          {scanning ? '⏳ Skanowanie…' : 'Skanuj pamiętnik'}
        </button>
        <button onClick={() => setDeleteMode(!deleteMode)}>
          {deleteMode ? 'Wyłącz tryb usuwania' : 'Włącz tryb usuwania'}
        </button>
      </div>
    <DeleteDairyDay entries={entries} deleteMode={deleteMode} onDelete={handleDelete} />
    </div>
  );
}
