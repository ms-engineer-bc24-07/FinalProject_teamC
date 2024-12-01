import React from "react";
import { Box, MenuItem, Select, FormControl, InputLabel, SelectChangeEvent } from "@mui/material";

type DateTimePickerProps = {
  value: { date: string; time: string }; // 日付と時刻の値
  onChange: (value: { date: string; time: string }) => void; // 変更イベントのコールバック関数
};

export default function DateTimePicker({ value, onChange }: DateTimePickerProps) {
    const handleDateChange = (event: SelectChangeEvent<string>) => {
        const updatedValue = { ...value, date: event.target.value };
        onChange(updatedValue);
    };

    const handleTimeChange = (event: SelectChangeEvent<string>) => {
        const updatedValue = { ...value, time: event.target.value };
        onChange(updatedValue);
    };

    return (
        <Box sx={{ display: "flex", gap: 2, alignItems: "center", marginBottom: "16px" }}>
        {/* 日付の選択 */}
        <FormControl sx={{ minWidth: 120 }}>
            <InputLabel id="date-label">日付</InputLabel>
            <Select
            labelId="date-label"
            value={value.date}
            onChange={handleDateChange}
            >
            {Array.from({ length: 30 }, (_, i) => (
                <MenuItem key={i} value={`2024-12-${i + 1}`}>{`2024-12-${i + 1}`}</MenuItem>
            ))}
            </Select>
        </FormControl>

        {/* 時刻の選択 */}
        <FormControl sx={{ minWidth: 120 }}>
            <InputLabel id="time-label">時刻</InputLabel>
            <Select
            labelId="time-label"
            value={value.time}
            onChange={handleTimeChange}
            >
            {Array.from({ length: 24 }, (_, i) =>
                Array.from({ length: 4 }, (_, j) => (
                <MenuItem key={`${i}-${j}`} value={`${i}:${j * 30}`}>{`${i}:${j * 30}`}</MenuItem>
                ))
            )}
            </Select>
        </FormControl>
        </Box>
    );
    }


