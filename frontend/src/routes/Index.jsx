import App from "../pages/App"
import Apptest from "../pages/Apptest"
import Deleteday from "../pages/Deleteday"
import GoalReactC from "../components/GoalReactC"
import Layout from "../components/Base"
import styles from "../styles/Layout.module.css";
import GoalReact from "../pages/GoalReact"


const routes = [
    {
        path: "/",
        element: <Layout />,
        children: [
            
        ]
    },
    {
        path:"/cele",
        element:<Layout extraClass={styles.goals}/>,
        children: [
            {path: "", element: <GoalReact />}
        ]
    }
]
export default routes;