"use client";

import React from "react";
import styles from "./ActionButton.module.css";

type ActionButtonProps = {
    label: string;
    onClick: () => void; 
    styleClass?: string; 
};

export default function ActionButton({ label, onClick, styleClass }: ActionButtonProps) {
    return (
        <button
            onClick={onClick}
            className={`${styles.ActionButton} ${styleClass || ""}`.trim()} // 動的クラス
        >
            {label}
        </button>
    );
}
