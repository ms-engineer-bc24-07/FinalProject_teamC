"use client";

import React from "react";
import styles from "./TitleSection.module.css";

type TitleSectionProps = {
    title: string;
    subtitle?: string; 
};

export default function TitleSection({ title, subtitle }: TitleSectionProps) {
    return (
        <div className={styles.titleSection}>
        <h1 className={styles.title}>{title}</h1>
        {subtitle && <p className={styles.subtitle}>{subtitle}</p>}
        </div>
    );
}
