import React from "react";
import styles from  "../styles/Days.module.css";
import { useEffect, useState } from "react";

export default function Days({ dayUrl }) {
  const [days, setDays] = useState([]);
  useEffect(() => {
    if (!dayUrl) return;
    fetch(dayUrl)
      .then(res => res.json())
      .then(data => setDays(data))
      .catch(err => console.error("Błąd pobierania dni:", err));
  }, [dayUrl]);

  return (
    <div className={styles.tilesGrid}>
        {days.map((entry, idx) => (
        <a
            key={idx}
            href={`/pomiary/dni/${entry.id}`} // <-- ID wpisu
        >
            <div className={styles.oneTile}>
                <h3>{entry.day}</h3>  
                <p>Kliknij, aby zobaczyć pomiary</p>
            </div>
        </a>
    ))}
    </div>
  );
}