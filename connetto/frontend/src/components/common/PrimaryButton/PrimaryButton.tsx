"use client";

import React from "react";
import styles from "./PrimaryButton.module.css";

type PrimaryButtonProps = {

    children: React.ReactNode;
    onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
    disabled?: boolean;
    type?: "button" | "submit" | "reset";
};

export default function PrimaryButton({
    children,
    onClick,
    disabled = false,
    type = "button",

}: PrimaryButtonProps) {
  return (
    <div className={styles.container}>

        <button
            type={type} 
            className={`${styles.button} ${disabled ? styles.disabled : ""}`}
            onClick={onClick}
            disabled={disabled}
        >
            {children}
        </button>

    </div>
  );
}
