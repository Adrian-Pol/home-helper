import React, {useState } from 'react';
//import styles from '../styles/GoalReact.module.css';


function GoalAdd({ addEndpoint, onAdded}) {
    const [cele, setCele] = useState("");
    const [ ocena, setOcena] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        const res = await fetch(addEndpoint, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            credentials: "same-origin",
            body: JSON.stringify({cele, ocena: Number(ocena)}),
        });

        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            alert("Błąd" + (err.error || " Nie udało się dodać celu"));
            return;
        }

        await res.json().catch(() => null);

        setCele("");
        setOcena("");

        onAdded?.()
    };

    return(
        <>
      
        <form onSubmit={handleSubmit}>
            <input
            type="text"
            placeholder='Twój cel'
            value={cele}
            onChange={(e) => setCele(e.target.value)}
            required />
        <select
        value={ocena}
        onChange={(e) => setOcena(e.target.value)}
        required>
            <option value="" disabled>Wybierz wagę priorytetu</option>
            <option value={1}>1</option>
            <option value={2}>2</option>
            <option value={3}>3</option>
        </select>
        <button type="submit">Dodaj</button>

        </form>
        </>
    )
}
export default GoalAdd;