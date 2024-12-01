import React, { useState } from "react";
import DateTimePicker from "./DateTimePicker";
import { Button, Box } from "@mui/material";

type DateTime = { id: number; date: string; time: string };

export default function DateTimeList() {
    const [dateTimeList, setDateTimeList] = useState<DateTime[]>([
        { id: Date.now(), date: "", time: "" },
    ]);

    const handleAdd = () => {
        setDateTimeList([
        ...dateTimeList,
        { id: Date.now(), date: "", time: "" }, // 新しい項目を追加
        ]);
    };

    const handleDateTimeChange = (id: number) => (updatedValue: { date: string; time: string }) => {
        setDateTimeList((prev) =>
        prev.map((item) =>
            item.id === id ? { ...item, ...updatedValue } : item
        )
        );
    };

    return (
        <Box>
        {dateTimeList.map((item) => (
            <DateTimePicker
            key={item.id}
            value={item}
            onChange={handleDateTimeChange(item.id)}
            />
        ))}
        <Button
            variant="contained"
            color="primary"
            onClick={handleAdd}
            sx={{ marginTop: "16px" }}
        >
            ＋
        </Button>
        </Box>
    );
    }
