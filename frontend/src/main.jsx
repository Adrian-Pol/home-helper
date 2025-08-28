import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './pages/App.jsx';
import Apptest from './pages/Apptest.jsx';
import Deleteday from './pages/Deleteday.jsx';
import GoalReact from './pages/GoalReact.jsx';


// Helper to safely mount a React tree into an optional container
function mount(id, render) {
const el = document.getElementById(id);
if (!el) return;
const root = createRoot(el);
root.render(<StrictMode>{render(el)}</StrictMode>);
}


// Mount list/manage view (unchanged from your structure)
mount('react-pomiary', (el) => {
const listUrl = el.dataset.listUrl;
const manageUrl = el.dataset.manageUrl;
return <App listUrl={listUrl} manageUrl={manageUrl} />;
});


// Mount chosen-day view
mount('chosen-day', (el) => {
const dayUrl = el.dataset.dayUrl;
return <Apptest dayUrl={dayUrl} />;
});


// Mount delete-day view (unified API base is passed as a prop if you want to override)
mount('delete-day', (el) => {
// Optional: allow overriding API base via data attribute (defaults used in component)
const apiBase = el.dataset.apiBase; // e.g. "/api/pamietnik"
return <Deleteday apiBase={apiBase} />;
});

mount('goal-view', (el) =>{
    const goalviewUrl = el.dataset.goalviewUrl;
    return <GoalReact goalviewUrl={goalviewUrl} />;
});