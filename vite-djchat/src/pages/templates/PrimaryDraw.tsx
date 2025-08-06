import { Box, Typography, useMediaQuery, styled } from "@mui/material"
import { useEffect, useState } from "react"
import { useTheme } from "@mui/material/styles"
import DrawerToggle from "../../components/PrimaryDraw/DrawToggle"
import MuiDrawer from "@mui/material/Drawer"

const PrimaryDraw = () => {
    const theme = useTheme()
    const below600 = useMediaQuery("(max-width:599px)")
    const [open, setOpen] = useState(!below600)

    const openedMixin = () => ({
        transition: theme.transitions.create("width", {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
        overflowX: "hidden",
        width: theme.primaryDraw.closed,
    })

    const closedMixin = () => ({
        transition: theme.transitions.create("width", {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
        overflowX: "hidden",
    })

    useEffect(() => {
        setOpen(!below600)
    }, [below600])

    const handleDrawerOpen = () => {
        setOpen(true)
    }

    const handleDrawerClose = () => {
        setOpen(false)
    }

    const Drawer = styled(MuiDrawer, {})(({ theme, open }) => ({
        width: theme.primaryDraw.width,
        whiteSpace: "nowrap",
        boxSizing: "border-box",
        ...(open && {
            ...openedMixin(),
            "& .MuiDrawer-paper": openedMixin(),
        }),
        ...(!open && {
            ...closedMixin(),
            "& .MuiDrawer-paper": closedMixin(),
        }),
    }))

    return (
        <Drawer
            open={open}
            variant={below600 ? "temporary" : "permanent"}
            slotProps={{
                paper: {
                    sx: {
                        mt: `${theme.primaryAppBar.height}px` || 0, // fallbacks in case `theme.primaryAppBar` is undefined
                        height: `calc(100vh - ${theme.primaryAppBar.height}px)`,
                        width: theme.primaryDraw.width,
                    },
                },
            }}
        >
            <Box>
                <Box sx={{ position: "absolute", top: 0, right: 0, p: 0, width: open ? "auto" : "100%" }}>
                    <DrawerToggle open={open} handleDrawerOpen={handleDrawerOpen} handleDrawerClose={handleDrawerClose} />
                    {[...Array(50)].map((_, i) => (
                        <Typography key={i} sx={{ mb: 2 }}>
                            {i + 1}
                        </Typography>
                    ))}
                </Box>
            </Box>
        </Drawer>
    )
}

export default PrimaryDraw