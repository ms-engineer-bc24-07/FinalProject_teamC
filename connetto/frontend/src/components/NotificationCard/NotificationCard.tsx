import React from "react";
import { Card, CardContent, Typography, Box } from "@mui/material";
import styles from "./NotificationCard.module.css";

type NotificationCardProps = {
    title: string;
    body: string;
    timestamp: string;
    isRead: boolean;
    onClick: () => void;
};

export default function NotificationCard({ title, body, timestamp, isRead, onClick }: NotificationCardProps) {
    return (
        <Card
        onClick={onClick} 
        className={`${styles.card} ${isRead ? styles.cardRead : styles.cardUnread}`}
        >
        <CardContent>
            <Box className={styles.cardContent}>
            <Typography
                variant="subtitle1"
                className={isRead ? styles.cardTitleRead : styles.cardTitle} // タイトルのスタイル変更
            >
                {title}
            </Typography>
            <Typography variant="caption" color="textSecondary">
                {timestamp}
            </Typography>
            </Box>
            <Typography variant="body2" className={styles.cardBody}>
            {body.length > 50 ? `${body.substring(0, 50)}...` : body} {/* 本文を2行程度に切り詰める */}
            </Typography>
        </CardContent>
        </Card>
    );
}
