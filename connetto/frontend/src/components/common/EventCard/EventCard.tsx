import React from "react";
import { Box, Typography } from "@mui/material";

type EventCardProps = {
    date: string;
    station: string;
    attendees: number;
    restaurant?: string; 
    details?: string; // お店の詳細情報 (例えば食べログAPIから取得)
    };

    export default function EventCard({ date, station, attendees, restaurant, details }: EventCardProps) {
    return (
        <Box
        sx={{
            marginBottom: "16px",
            padding: "16px",
            border: "1px solid #ddd",
            borderRadius: "8px",
            backgroundColor: "#f9f9f9",
        }}
        >
        <Typography variant="subtitle1" fontWeight="bold">
            日時: {date}
        </Typography>
        <Typography variant="subtitle1">
            場所: {station}
        </Typography>
        <Typography variant="subtitle1">
            人数: {attendees}人
        </Typography>
        {restaurant ? (
            <>
            <Typography variant="subtitle1" fontWeight="bold">
                お店: {restaurant}
            </Typography>
            <Typography variant="body2" color="textSecondary">
                詳細: {details}
            </Typography>
            </>
        ) : (
            <Typography variant="subtitle1" color="textSecondary">
            お店: 決定待ち
            </Typography>
        )}
        </Box>
    );
}
