"use client";

import React from "react";
import styles from "./InputField.module.css";

type InputFieldProps = {
    type?: string;
    placeholder?: string;
    value?: string;
    onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
    label?: string;
};

export default function InputField({
    type = "text",
    placeholder,
    value,
    onChange,
    label,
}: InputFieldProps) {
    return (
        <div className={styles.inputContainer}>
            {label && <label className={styles.label}>{label}</label>}
            <input
                type={type}
                placeholder={placeholder}
                value={value}
                onChange={onChange}
                className={styles.input}
                />
        </div>
        );
}
