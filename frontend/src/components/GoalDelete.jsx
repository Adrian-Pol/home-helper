
import styles from '../styles/GoalReact.module.css';
import React, { useState } from 'react';

function GoalDelete({ entries, deleteGoal }) {
    const [selectedId, setselectedId] = useState("");
    return (
        <div>
            
            {entries.length > 0 && (
                <select 
                    value={selectedId}
                    onChange={(e) => setselectedId(e.target.value)}>
                    <option value="" disabled selected>Wybierz cel do usunięcia</option>
                    {entries.map((entry) => (
                        <option key={entry.id} value={entry.id}>
                            {entry.cele}
                        </option>
                    ))}
                </select>
            
            )}
            
            <button className={styles.button} onClick={() => 
                deleteGoal(selectedId)
            } disabled={!selectedId}>
                Usuń cel
            </button>
        </div>
    );
}
export default GoalDelete;