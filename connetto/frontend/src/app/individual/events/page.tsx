"use client";

import React, { useState, useEffect } from "react";
import { Box, Tabs, Tab, Typography } from "@mui/material";
import DrawerAppBar from "@/components/layout/DrawerAppBar/DrawerAppBar";
import BottomMenu from "@/components/layout/BottomMenu/BottomMenu";
import EventCard from "@/components/common/EventCard/EventCard";
import axios from "axios";
import { getFirebaseToken } from "@/utils/auth";

type Event = {
    identifier: string;
    meeting_date: string;
    meeting_location: string;
    number_of_members: number;
};

export default function Events() {
    const [currentTab, setCurrentTab] = useState(0);
    const [confirmedEvents, setConfirmedEvents] = useState<Event[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let isMounted = true;

        const fetchEvents = async () => {
            try {
                setError(null);
                setLoading(true);

                const token = await getFirebaseToken();
                if (!token) return;

                const response = await axios.get<Event[]>("http://localhost:8000/api/groups/", {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                if (isMounted) {
                    setConfirmedEvents(response.data);
                }
            } catch (err) {
                if (isMounted) {
                    setError("データの取得に失敗しました。もう一度お試しください。");
                }
            } finally {
                if (isMounted) {
                    setLoading(false);
                }
            }
        };

        fetchEvents();

        return () => {
            isMounted = false;
        };
    }, []);

    const handleChange = (event: React.SyntheticEvent, newValue: number) => {
        setCurrentTab(newValue);
    };

    const formatDate = (date: string) => {
        try {
            const options: Intl.DateTimeFormatOptions = {
                year: "numeric",
                month: "2-digit",
                day: "2-digit",
                weekday: "short",
                hour: "2-digit",
                minute: "2-digit",
            };
            return new Intl.DateTimeFormat("ja-JP", options).format(new Date(date));
        } catch (error) {
            console.error("日付フォーマットエラー:", error);
            return "無効な日付";
        }
    };

    return (
        <Box sx={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
            <DrawerAppBar />
            <Box
                sx={{
                    marginTop: "20px",
                    position: "sticky",
                    top: "60px",
                    zIndex: 100,
                    backgroundColor: "#fff",
                    padding: "8px 0",
                    borderBottom: "1px solid #ddd",
                }}
            >
                <Tabs
                    value={currentTab}
                    onChange={handleChange}
                    centered
                    sx={{
                        "& .MuiTab-root": {
                            minWidth: "50%",
                            fontWeight: "bold",
                            fontSize: "16px",
                            padding: "12px 0",
                            backgroundColor: "#fff",
                            color: "#A09CAB",
                        },
                        "& .Mui-selected": {
                            backgroundColor: "#fff",
                            color: "#000 !important",
                        },
                        "& .MuiTabs-indicator": {
                            backgroundColor: "#000",
                            height: "4px",
                            borderRadius: "2px",
                        },
                    }}
                >
                    <Tab label="開催予定" />
                    <Tab label="参加履歴" />
                </Tabs>
            </Box>
            <Box sx={{ flex: 1, overflowY: "auto", padding: "16px" }}>
                {loading ? (
                    <Typography>Loading...</Typography>
                ) : error ? (
                    <Typography color="error">{error}</Typography>
                ) : currentTab === 0 ? (
                    confirmedEvents.length > 0 ? (
                        confirmedEvents.map((event) => (
                            <EventCard
                                key={event.identifier}
                                date={formatDate(event.meeting_date)}
                                station={event.meeting_location}
                                attendees={event.number_of_members}
                            />
                        ))
                    ) : (
                        <Typography>現在、開催予定のイベントはありません。</Typography>
                    )
                ) : (
                    <Typography>参加履歴はありません。</Typography>
                )}
            </Box>
            <BottomMenu />
        </Box>
    );
}

