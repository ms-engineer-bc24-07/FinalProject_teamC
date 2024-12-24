import React from "react";
import { FormControl, InputLabel, MenuItem, Select, SelectChangeEvent } from "@mui/material";
import styles from "./DropDownCondition.module.css"

type DropdownConditionProps = {
    value: string;
    onChange: (event: SelectChangeEvent) => void;
    options: { value: string; label: string }[];
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
            className={styles.formControl}
            >
            <Select 
                value={value} 
                onChange={onChange}
                displayEmpty
                className={`${styles.select} ${
                    value === "" ? styles.selectPlaceholder : styles.selectValue
                }`}
            >
                <MenuItem value="">
                    {placeholder}
                </MenuItem>
                {options.map((option, index) => (
                <MenuItem key={index} value={option.value}>
                    {option.label}
                </MenuItem>
                ))}
            </Select>
        </FormControl>
    );
}
