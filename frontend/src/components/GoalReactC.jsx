import React from 'react';
import styles from '../styles/GoalReact.module.css';

export default function GoalReactC({entries}) {
if (!entries?.length) {
    console.log({entries})
    return <p>Brak celów do wyświetlenia</p>;
}
return (
<>
    <div className={styles.container}>
        {entries.map((entry) => (
        <div key = {entry.id} className={styles.list}>
            <h3>{entry.goal}</h3>
            <p>Status: {entry.status}</p>
            <p>Priorytet: {entry.priority}</p>
        </div>

        ))}
        
        
    </div>
  
</>
)}