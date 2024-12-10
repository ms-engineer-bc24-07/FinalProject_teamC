import React, { useState, useEffect } from "react";
import DateTimePicker from "./DateTimePicker";
import { Button, Box } from "@mui/material";
import styles from "./DateTimeList.module.css";

type DateTimeListProps = {
    onChange: (dates: string[]) => void; // ISO形式の日時リストを親コンポーネントに渡す
};

export default function DateTimeList({ onChange }: DateTimeListProps) {
    const [dateTimeList, setDateTimeList] = useState<{ date: string; time: string }[]>([
        { date: "", time: "" },
    ]);

    const handleAdd = () => {
        setDateTimeList([...dateTimeList, { date: "", time: "" }]);
    };

    const handleDateTimeChange = (index: number, field: "date" | "time") => (value: string) => {
        setDateTimeList((prev) =>
            prev.map((item, i) => (i === index ? { ...item, [field]: value } : item))
        );
    };

    useEffect(() => {
        const formattedDates = dateTimeList
            .filter((item) => item.date && item.time) // 日付と時刻が両方選択されている場合
            .map((item) => {
                const isoDateTime = `${item.date}T${item.time}:00Z`; // ISO形式に変換
                return isoDateTime;
            });

        onChange(formattedDates); // 親コンポーネントに通知
    }, [dateTimeList, onChange]);

    return (
        <Box>
            {dateTimeList.map((item, index) => (
                <DateTimePicker
                    key={index}
                    value={item}
                    onChange={(field, value) => handleDateTimeChange(index, field)(value)}
                />
            ))}
            <Button
                onClick={handleAdd}
                className={styles.addButton}
                variant="contained"
                color="primary"
                style={{ marginTop: "10px" }}
            >
                ＋
            </Button>
        </Box>
    );
}


