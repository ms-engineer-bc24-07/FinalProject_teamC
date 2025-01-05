import React from "react";
import { Box, Typography } from "@mui/material";
import styles from "./EventCard.module.css"; 
import { formatDateTime } from "@/utils/dateUtils";

type EventCardProps = {
    date: string;
    station: string;
    attendees: number;
};

export default function EventCard({ date, station, attendees }: EventCardProps) {
    const formattedDate = formatDateTime(date); 

    return (
        <div className={styles.box}>
            {/* ステータスボックス */}
            <div className={styles.statusBox}>
                <p className={styles.statusText}>開催決定／お店確定待ち</p>
            </div>
            <div className={styles.card}>
                <div className={styles.row}>
                    <p className={styles.label}>日時</p>
                    <p className={styles.value}>{formattedDate}</p>
                </div>

                <div className={styles.row}>
                    <p className={styles.label}>場所</p>
                    <p className={styles.value}>{station}</p>
                </div>

                <div className={styles.row}>
                    <p className={styles.label}>人数</p>
                    <p className={styles.value}>{attendees} 人</p>
                </div>
            </div>
        </div>
    );
}
