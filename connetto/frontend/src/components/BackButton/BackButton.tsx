"use client";

import React from "react";
import { useRouter } from "next/navigation";
import styles from "./BackButton.module.css";

type BackButtonProps = {
  label?: string;
  href?: string;
};

export default function BackButton({ label, href }: BackButtonProps) {
  const router = useRouter();

  const handleBack = () => {
    if (href) {
      router.push(href);
    } else {
      router.back();
    }
  };

  return (
    <button onClick={handleBack} className={styles.backButton}>
      <span className={styles.icon}>＜</span> {label}
    </button>
  );
}
