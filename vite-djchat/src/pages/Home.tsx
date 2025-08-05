import { Box, CssBaseline } from "@mui/material"
import PrimaryAppBar from "./templates/PrimaryAppBar"
import PrimaryDraw from "./templates/PrimaryDraw"
import SecondaryDraw from "./templates/SecondaryDraw"

const Home = () => {
    return (
        <>
            <Box sx={{ display: "flex" }}>
                <CssBaseline />
                
                <PrimaryAppBar /> {/* theme.tsx -> App.tsx -> PrimaryAppBar.tsx -> Home.tsx */}
                
                <PrimaryDraw></PrimaryDraw>
                
                <SecondaryDraw></SecondaryDraw>
            </Box>
        </>
    )
}

export default Home