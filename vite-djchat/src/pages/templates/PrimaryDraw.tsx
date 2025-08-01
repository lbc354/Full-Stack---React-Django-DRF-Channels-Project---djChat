import { Box, Drawer, Typography, useMediaQuery } from "@mui/material"
import { useEffect, useState } from "react"
import { useTheme } from "@mui/material/styles"
import DrawerToggle from "../../components/PrimaryDraw/DrawToggle"

const PrimaryDraw = () => {
    const theme = useTheme()
    const below600 = useMediaQuery("(max-width:599px)")
    const [open, setOpen] = useState(!below600)

    useEffect(() => {
        setOpen(!below600)
    }, [below600])

    const handleDrawerOpen = () => {
        setOpen(true)
    }

    const handleDrawerClose = () => {
        setOpen(false)
    }

    return (
        <Drawer
            open={open}
            variant={below600 ? "temporary" : "permanent"}
            slotProps={{
                paper: {
                    sx: {
                        mt: `${theme.primaryAppBar?.height}px` || 0, // fallbacks in case `theme.primaryAppBar` is undefined
                        height: `calc(100vh - ${theme.primaryAppBar.height}px)`,
                        width: theme.primaryDraw.width,
                    },
                },
            }}
        >
            <Box>
                <Box sx={{ position: "absolute", top: 0, right: 0, p: 0, width: open ? "auto" : "100%" }}>
                    <DrawerToggle />
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