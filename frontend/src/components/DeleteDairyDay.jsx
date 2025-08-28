import React from 'react';
import styles from '../styles/DeleteDairy.module.css';


export default function DeleteDairyDay({ entries, deleteMode, onDelete }) {
if (!entries?.length) {
return <p>Brak wpisów do wyświetlenia.</p>;
}


return (
<div className={styles.grid}>
{entries.map((entry) => (
<div key={entry.id} className={`${styles.tile} ${deleteMode ? styles.highlight : ''}`}>
<a className={styles.imageLink} href={`/pamietnik/wpis/${entry.id}`} aria-label={`Przejdź do wpisu ${entry.folder_name || entry.id}`}>
{entry.first_image ? (
<img loading ='lazy'className={styles.image} src={`/${entry.first_image}`} alt="Podgląd zdjęcia dnia" />
) : (
<div className={styles.noImage}>Brak zdjęcia</div>
)}
</a>


{deleteMode && (
<button
type="button"
className={styles.deleteButton}
onClick={() => onDelete(entry.id)}
aria-label={`Usuń wpis ${entry.folder_name || entry.id}`}
title="Usuń ten dzień"
>
🗑️
</button>
)}


<div className={styles.caption}>{entry.folder_name || 'BRAK'}</div>
</div>
))}
</div>
);
}