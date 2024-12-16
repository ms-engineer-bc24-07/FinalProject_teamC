import React from "react";
import { Card, CardContent, Typography, Box } from "@mui/material";
import styles from "./NotificationCard.module.css";

type NotificationCardProps = {
    id: number; 
    title: string;
    body: string;
    timestamp: string;
    isRead: boolean;
    onClick: () => void;
};

export default function NotificationCard({
    id,
    title,
    body,
    timestamp,
    isRead,
    onClick,
}: NotificationCardProps) {
    return (
        <Card
            onClick={onClick}
            className={`${styles.card} ${isRead ? styles.cardRead : styles.cardUnread}`}
        >
            <CardContent>
                <Box className={styles.cardContent}>
                    <Typography
                        variant="subtitle1"
                        className={isRead ? styles.cardTitleRead : styles.cardTitle}
                    >
                        {title}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                        {new Date(timestamp).toLocaleString("ja-JP", {
                            year: "numeric",
                            month: "2-digit",
                            day: "2-digit",
                            hour: "2-digit",
                            minute: "2-digit",
                        })}
                    </Typography>
                </Box>
                <Typography variant="body2" className={styles.cardBody}>
                    {body.length > 50 ? `${body.substring(0, 21)}...` : body}
                </Typography>
            </CardContent>
        </Card>
    );
}
