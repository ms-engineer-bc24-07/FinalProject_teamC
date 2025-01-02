import React from "react";
import { Card, CardContent, Typography, Box } from "@mui/material";
import styles from "./NotificationCard.module.css";

type NotificationCardProps = {
    id: number; 
    title: string;
    body: string;
    timestamp: string;
    isRead: boolean;
    type: string;
    data?: Record<string, any>;
    onClick: () => void;
};

export default function NotificationCard({
    id,
    title,
    body,
    timestamp,
    isRead,
    type,
    data,
    onClick,
}: NotificationCardProps) {
    const renderDetails = () => {
         // 開催決定通知の場合
        if (type === "EVENT_DECISION" && data) {
            return (
                <Box className={styles.detailBox}>
                    <Typography variant="body2" className={styles.detailText}>
                        開催日時: {data.meeting_date}
                    </Typography>
                    <Typography variant="body2" className={styles.detailText}>
                        場所: {data.meeting_location}
                    </Typography>
                    <Typography variant="body2" className={styles.detailText}>
                        参加人数: {data.participant_count}人
                    </Typography>
                </Box>
            );
        }
         // 幹事決定通知の場合
        if (type === "MANAGER_DECISION" && data) {
            return (
                <Box className={styles.detailBox}>
                    <Typography variant="body2" className={styles.detailText}>
                        候補のお店:
                    </Typography>
                    <ul className={styles.restaurantList}>
                        {data.restaurants?.map((restaurant: any, index: number) => (
                            <li key={index} className={styles.restaurantItem}>
                                <a href={restaurant.url} target="_blank" rel="noopener noreferrer">
                                    {restaurant.name}
                                </a>
                            </li>
                        ))}
                    </ul>
                </Box>
            );
        }
        return null;
    };

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
                {renderDetails()}
            </CardContent>
        </Card>
    );
}
