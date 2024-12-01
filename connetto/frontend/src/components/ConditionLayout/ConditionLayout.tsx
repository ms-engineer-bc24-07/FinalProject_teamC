import React from "react";
import { Box, Divider, Typography } from "@mui/material";
import styles from "./ConditionLayout.module.css"

type ConditionLayoutProps = {
    label: string; 
    children: React.ReactNode; 
};

export default function ConditionLayout({ label, children }: ConditionLayoutProps) {
    return (
        <Box className={styles.container}>
            <Box className={styles.row}>
                <Typography variant="body1" className={styles.label}>
                    {label}
                </Typography>
                <Box className={styles.content}>{children}</Box>
            </Box>
            <Divider className={styles.divider} />
        </Box>
    );
    }
