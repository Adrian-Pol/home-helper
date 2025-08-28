import React, { useEffect, useMemo, useState } from 'react';
import GoalReactC from '../components/GoalReactC.jsx';

export default function GoalReact({}) {
    const endpoints = useMemo(() => ({
        list: `/api/cele`,
        add: `/cele`,
        del:(id) => `/cele/${id}`,

    }), []);
    const [entries, setEntries] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        const ac = new AbortController()
        async function load() {
            setLoading(true);
            setError('');
            try{
                const res = await fetch(endpoints.list, {
                    method: 'GET',
                    credentials: 'same-origin',
                    signal: ac.signal,

                });
                if (!res.ok) throw new Error(await res.text() || "Błąd pobierania wpisów");
                const data = await res.json();
                setEntries(Array.isArray(data) ? data : []);
            } catch (err) {
                if (err.name !== "AbortError") setError(err.message || "Nieznany błąd");
            } finally {
                setLoading(false);

            }            
        }
        load();
        return () => ac.abort();
    }, [endpoints.list]);

    return(
        <div>
        <GoalReactC entries = {entries}/>
        </div>
    )
}