import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider } from "react-router-dom"
import Home from "./pages/Home"

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route path="/" element={<Home />} />
    </Route>
  )
)

// const App: React.FC = (name) => {
// const App = (name: string) => {
//   console.log(name)
const App = () => {
  return (
    <RouterProvider router={router} />
  )
}

export default App