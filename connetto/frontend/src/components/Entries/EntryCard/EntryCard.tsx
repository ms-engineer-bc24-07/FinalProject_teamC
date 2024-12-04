import ActionButton from "@/components/common/ActionButton/ActionButton";
import React from "react";
import styles from "./EntryCard.module.css";

export default function EntryCard() {
    const handleEdit = () => {
        alert("変更画面に遷移します");
    };

    const handleDelete = () => {
        alert("削除が確定されました");
    };

    return (
        <div className={styles.entryCard}>
        <div className={styles.entryDetails}>
            <div className={styles.entrySection}>
            <h3 className={styles.sectionTitle}>日時</h3>
            <ul className={styles.dateList}>
                <li>2024年12月16日（月） 12:00</li>
                <li>2024年12月17日（火） 12:00</li>
                <li>2024年12月18日（水） 13:00</li>
            </ul>
            </div>
            <div className={styles.entrySection}>
            <h3 className={styles.sectionTitle}>希望条件</h3>
            <p className={styles.conditionText}>雰囲気 ： 落ち着いたお店</p>
            </div>
        </div>
        <div className={styles.entryButtons}>
            <ActionButton
            label="変更"
            onClick={handleEdit}
            styleClass={styles.changeButton}
            />
            <ActionButton
            label="削除"
            onClick={handleDelete}
            styleClass={styles.deleteButton}
            />
        </div>
        </div>
    );
}
