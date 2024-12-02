import React from "react";
import { FormControl, InputLabel, MenuItem, Select, SelectChangeEvent } from "@mui/material";


type DropdownConditionProps = {
    value: string;
    onChange: (event: SelectChangeEvent) => void;
    options: string[];
    placeholder?: string, 
};

export default function DropdownCondition({ 
    value,
    onChange,
    options,
    placeholder = "未選択",
}:DropdownConditionProps) {
    return (
        <FormControl
            variant="outlined"
            sx={{
                width: "150px", 
                backgroundColor: "#ffffff", 
                borderRadius: "8px", 
                "& .MuiOutlinedInput-notchedOutline": {
                borderColor: "#ddd", 
                },
            }}
            >
            <Select 
                value={value} 
                onChange={onChange}
                displayEmpty
                disableUnderline 
                sx={{
                    color: value === "" ? "#9e9e9e" : "#000000", // プレースホルダーの色と選択後の色
                    fontSize: "14px",
                }}
            >
                <MenuItem value="">
                    {placeholder} {/* 未選択時に表示するテキスト */}
                </MenuItem>
                {options.map((option, index) => (
                <MenuItem key={index} value={option}>
                    {option}
                </MenuItem>
                ))}
            </Select>
        </FormControl>
    );
}
