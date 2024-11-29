"use client";

import React from "react";
import styles from "./PrimaryButton.module.css";

type PrimaryButtonProps = {
    children: React.ReactNode;
    onClick?: () => void;
    disabled?: boolean;
};

export default function PrimaryButton({
    children,
    onClick,
    disabled = false,
}: PrimaryButtonProps) {
    return (
    <div className={styles.container}>
        <button
            className={`${styles.button} ${disabled ? styles.disabled : ""}`}
            onClick={onClick}
            disabled={disabled}
        >
            {children}
        </button>
    </div>
);
}
