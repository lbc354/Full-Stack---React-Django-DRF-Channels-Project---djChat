import { Box, CssBaseline } from "@mui/material"
import PrimaryAppBar from "./templates/PrimaryAppBar"

const Home = () => {
    return (
        <>
            <Box sx={{ display: "flex" }}>
                <CssBaseline />
                <PrimaryAppBar /> {/* theme.tsx -> App.tsx -> PrimaryAppBar.tsx -> Home.tsx */}
            </Box>
        </>
    )
}

export default Home