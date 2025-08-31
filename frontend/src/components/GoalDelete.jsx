import React from 'react';
import styles from '../styles/GoalReact.module.css';

function GoalDelete({ entries, deleteGoal }) {
    return (
        <div>
            
            {entries.length > 0 && (
                <select id="goal_select">
                    <option value="" disabled selected>Wybierz cel do usunięcia</option>
                    {entries.map((entry) => (
                        <option key={entry.id} value={entry.id}>
                            {entry.cele}
                        </option>
                    ))}
                </select>
            
            )}
            
            <button className={styles.button} onClick={() => {
                const select = document.getElementById('goal_select');
                deleteGoal(select.value); // Wywołanie funkcji usuwania
            }}>
                Usuń cel
            </button>
        </div>
    );
}
export default GoalDelete;