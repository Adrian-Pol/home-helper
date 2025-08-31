import App from "../pages/App"
import Apptest from "../pages/Apptest"
import Deleteday from "../pages/Deleteday"
import GoalReactC from "../components/GoalReactC"
import Layout from "../components/Base"

const routes = [
    {
        path: "/",
        element: <Layout />,
        children: [
            {path: "cele", element: <GoalReactC />}
        ]
    }
]
export default routes;