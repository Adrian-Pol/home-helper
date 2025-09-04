import React, { useEffect, useMemo, useState } from 'react';
import GoalReactC from '../components/GoalReactC.jsx';
import GoalDelete from '../components/GoalDelete.jsx';
import GoalAdd from '../components/GoalAdd.jsx';
import styles from '../styles/GoalReact.module.css';


export default function GoalReact({}) {
    const endpoints = useMemo(() => ({
        list: `/api/cele`,
        add: `/cele`,
        del:(id) => `/cele/${id}`,

    }), []);
    const [entries, setEntries] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [deleteMode , setDeleteMode] = useState(false);

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
                console.log("Dane:", data);
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

    const reloadGoals = async () => {
        const res = await fetch(endpoints.list,{credentials:"same-origin"});
        setEntries(await res.json());
    }

   const deleteGoal = async (goalId) => {
        if (!goalId) {
            alert("Wybierz cel do usunięcia.");
            return;
        }
        try {
            const response = await fetch(endpoints.del(goalId), {
                method: "DELETE",
            });

            if (response.ok) {
                alert("Usunięto cel");
                setEntries(entries.filter(entry => entry.id !== goalId)); 
            } else {
                alert("Błąd przy usuwaniu");
            }
        } catch (error) {
            alert("Wystąpił błąd: " + error.message);
        
        }
    };
    

    return(
        <>
            <div className={styles.list}>
                <GoalReactC entries={entries}/>
            </div>
            <div className={styles.actions}>
                <GoalAdd addEndpoint={endpoints.add} onAdded={reloadGoals} />
                <GoalDelete entries={entries} deleteGoal={deleteGoal}/>
            </div>
        </>
    )
}
