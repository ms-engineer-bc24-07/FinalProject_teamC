import React from "react";
import { Box, MenuItem, Select, FormControl, InputLabel, SelectChangeEvent } from "@mui/material";
import { generateDateOptions, generateTimeOptions } from "@/utils/dateUtils";
type DateTimePickerProps = {
    value: { date: string; time: string };
    onChange: (field: "date" | "time", value: string) => void;
};

export default function DateTimePicker({ value, onChange }: DateTimePickerProps) {
    const handleDateChange = (event: SelectChangeEvent<string>) => {
        onChange("date", event.target.value); 
    };

    const handleTimeChange = (event: SelectChangeEvent<string>) => {
        onChange("time", event.target.value); 
    };

    const dateOptions = generateDateOptions();
    const timeOptions = generateTimeOptions();

    return (
        <Box sx={{ display: "flex", gap: 2, alignItems: "center", marginBottom: "16px" }}>
            {/* 日付の選択 */}
            <FormControl sx={{ minWidth: 200 }}>
                <InputLabel id="date-label">日付</InputLabel>
                <Select labelId="date-label" value={value.date} onChange={handleDateChange}>
                    {dateOptions.map((date, index) => (
                        <MenuItem key={index} value={date}>
                            {date}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>

            {/* 時刻の選択 */}
            <FormControl sx={{ minWidth: 120 }}>
                <InputLabel id="time-label">時刻</InputLabel>
                <Select labelId="time-label" value={value.time} onChange={handleTimeChange}>
                    {timeOptions.map((time, index) => (
                        <MenuItem key={index} value={time}>
                            {time}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
        </Box>
    );
}