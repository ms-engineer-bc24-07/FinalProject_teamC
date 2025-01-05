import React from "react";
import { Box, Typography } from "@mui/material";
import styles from "./EventCard.module.css"; // CSSモジュールをインポート

type EventCardProps = {
    date: string;
    station: string;
    attendees: number;
};

export default function EventCard({ date, station, attendees }: EventCardProps) {
    return (
        <Box className={styles.card}>
            <Box className={styles.row}>
                <Typography variant="subtitle1" className={styles.label}>
                    日時
                </Typography>
                <Typography variant="subtitle1" className={styles.value}>
                    {date}
                </Typography>
            </Box>

            <Box className={styles.row}>
                <Typography variant="subtitle1" className={styles.label}>
                    場所
                </Typography>
                <Typography variant="subtitle1" className={styles.value}>
                    {station}
                </Typography>
            </Box>

            <Box className={styles.row}>
                <Typography variant="subtitle1" className={styles.label}>
                    人数
                </Typography>
                <Typography variant="subtitle1" className={styles.value}>
                    {attendees} 人
                </Typography>
            </Box>
        </Box>
    );
}
