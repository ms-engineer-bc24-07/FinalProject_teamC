import React, { useState, useEffect } from "react";
import DateTimePicker from "./DateTimePicker";
import { Button, Box } from "@mui/material";
import styles from "./DateTimeList.module.css";

type DateTimeListProps = {
    onChange: (dates: string[]) => void; 
    initialDates?: { date: string; time: string }[];
};

export default function DateTimeList({ onChange, initialDates = [{ date: "", time: "" }] }: DateTimeListProps) {
    const [dateTimeList, setDateTimeList] = useState<{ date: string; time: string }[]>([
        { date: "", time: "" },
    ]);

    const handleDateTimeChange = (index: number, field: "date" | "time", value: string) => {
        setDateTimeList((prev) =>
            prev.map((item, i) => (i === index ? { ...item, [field]: value } : item))
        );
    };

    useEffect(() => {
        const formattedDates = dateTimeList
            .filter((item) => item.date && item.time) 
            .map((item) => {
                const date = item.date.replace(/年|月/g, "-").replace(/日（.+）/, ""); // 日本語形式を変換
                const time = item.time;
                const isoDateTime = `${date}T${time}:00Z`; 
                return isoDateTime;
            });

            onChange(formattedDates);
        }, [dateTimeList, onChange]);

        useEffect(() => {
            if (initialDates && initialDates.length > 0) {
                setDateTimeList(initialDates); 
            }
        }, []);
    
        const handleAdd = () => {
            setDateTimeList([...dateTimeList, { date: "", time: "" }]);
        };

    return (
        <Box className={styles.container}>
            {dateTimeList.map((item, index) => (
                <DateTimePicker
                    key={index}
                    value={item}
                    onChange={(field, value) => handleDateTimeChange(index, field, value)}
                />
            ))}
            <Button
                onClick={handleAdd}
                className={styles.addButton}
                variant="contained"
            >
                ＋
            </Button>
        </Box>
    );
}


