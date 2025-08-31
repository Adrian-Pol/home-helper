import React from 'react';
import styles from '../styles/GoalReact.module.css';

export default function GoalReactC({entries}) {
if (!entries?.length) {
    console.log({entries})
return <p>Brak celów do wyświetlenia</p>;
}
return (
<div className={styles.container}>
    {entries.map((entries) => (
    <div key = {entries.id} className={styles.list}>
        <h3>{entries.cele}</h3>
        <p>Status: {entries.status}</p>
        <p>Priorytet: {entries.priority}</p>
    </div>
    
    ))}
    
</div>
)}