import React from "react";
import styles from "./CustomSelectField.module.css";

interface CustomSelectFieldProps {
    label: string;
    value: string;
    options: { value: string; label: string }[];
    onChange: (value: string) => void;
    }

    export default function CustomSelectField({
    label,
    value,
    options,
    onChange,
    }: CustomSelectFieldProps) {
    return (
        <div className={styles.container}>
        <label className={styles.label}>{label}</label>
        <select
            className={styles.select}
            value={value}
            onChange={(e) => onChange(e.target.value)}
        >
            <option value="" disabled>
            選択してください
            </option>
            {options.map((option) => (
            <option key={option.value} value={option.value}>
                {option.label}
            </option>
            ))}
        </select>
        </div>
    );
}
