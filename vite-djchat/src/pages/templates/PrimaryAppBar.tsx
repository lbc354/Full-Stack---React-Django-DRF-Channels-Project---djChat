import { AppBar, Box, Drawer, IconButton, Link, Toolbar, Typography, useMediaQuery } from "@mui/material"
import MenuIcon from "@mui/icons-material/Menu"
import { useTheme } from "@mui/material/styles"
import { useEffect, useState } from "react"

const PrimaryAppBar = () => {
    const theme = useTheme()
    const [sideMenu, setSideMenu] = useState(false)
    const isSmallScreen = useMediaQuery(theme.breakpoints.up("sm")) // sm = 600 (check on mui breakpoints documentation)

    // const toggleDrawer = (open: boolean) => (event: React.MouseEvent) => {
    //     setSideMenu(open)
    // }
    const toggleDrawer = (open: boolean) => (event: React.KeyboardEvent | React.MouseEvent) => {
        if (
            event.type === "keydown" &&
            ((event as React.KeyboardEvent).key === "Tab" ||
                (event as React.KeyboardEvent).key === "Shift")
        ) {
            return
        }
        setSideMenu(open)
    }

    useEffect(() => {
        if (isSmallScreen && sideMenu) { // if both are true
            setSideMenu(false)
        }
    }, [isSmallScreen])

    return (
        <>
            <AppBar sx={{
                // backgroundColor: theme.palette.background.default,
                borderBottom: `1px solid ${theme.palette.divider}`,
                zIndex: (theme) => theme.zIndex.drawer + 2,
            }}>
                <Toolbar variant="dense" sx={{ height: theme.primaryAppBar.height, minHeight: theme.primaryAppBar.height, }}>

                    <Box sx={{ display: { xs: "block", sm: "none" } }}>
                        <IconButton color="inherit" aria-label="open drawer" edge="start" sx={{ mr: 2 }} onClick={toggleDrawer(true)}>
                            <MenuIcon />
                        </IconButton>
                    </Box>

                    <Drawer anchor="left" open={sideMenu} onClose={toggleDrawer(false)}>
                        <Box sx={{ padding: 2 }}>
                            {[...Array(100)].map((_, i) => (
                                <Typography key={i} sx={{ mb: 2 }}>
                                    {i + 1}
                                </Typography>
                            ))}
                        </Box>
                    </Drawer>

                    <Link href='/' underline="none" color="inherit">
                        <Typography variant="h6" noWrap component='div' sx={{ fontWeight: 700, letterSpacing: '-0.5px' }}>
                            DJCHAT
                        </Typography>
                    </Link>

                </Toolbar>
            </AppBar>
        </>
    )
}

export default PrimaryAppBar