import { Box, CssBaseline } from "@mui/material"
import PrimaryAppBar from "./templates/PrimaryAppBar"
import PrimaryDraw from "./templates/PrimaryDraw"
import SecondaryDraw from "./templates/SecondaryDraw"
import Main from "./templates/Main"

const Home = () => {
    return (
        <>
            <Box sx={{ display: "flex" }}>
                <CssBaseline />
                
                <PrimaryAppBar /> {/* theme.tsx -> App.tsx -> PrimaryAppBar.tsx -> Home.tsx */}
                
                <PrimaryDraw></PrimaryDraw>
                
                <SecondaryDraw></SecondaryDraw>
                
                <Main></Main>
            </Box>
        </>
    )
}

export default Home