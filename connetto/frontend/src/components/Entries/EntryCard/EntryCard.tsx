import ActionButton from "@/components/common/ActionButton/ActionButton";
import React from "react";
import styles from "./EntryCard.module.css";
import { formatDate, formatTime } from "@/utils/dateUtils";

type Participation = {
    id: number;
    desired_dates: string[];
    gender_restriction: string;
    age_restriction: string;
    joining_year_restriction: string;
    department_restriction: string;
    atmosphere_restriction: string;
};

type EntryCardProps = {
    participation: Participation;
};

const conditionLabels: { [key: string]: { [key: string]: string } } = {
    gender: {
        same_gender: "同性",
        no_restriction: "希望なし",
    },
    age: {
        same_age: "同年代",
        broad_age: "幅広い年代",
        no_restriction: "希望なし",
    },
    joining_year: {
        exact_match: "同期のみ",
        no_restriction: "希望なし",
    },
    department: {
        same_department: "同じ部署内",
        mixed_departments: "他部署交流",
        no_restriction: "希望なし",
    },
    atmosphere: {
        quiet: "落ち着いたお店",
        lively: "わいわいできるお店",
        no_restriction: "希望なし",
    },
};

const fieldLabels: { [key: string]: string } = {
    gender_restriction: "性別",
    age_restriction: "年齢",
    joining_year_restriction: "入社年",
    department_restriction: "部署",
    atmosphere_restriction: "お店の雰囲気",
};

export default function EntryCard({ participation }: EntryCardProps) {
    const today = new Date();

    const isEditable = participation.desired_dates.some((date) => {
        const desiredDate = new Date(date);
        const editableDate = new Date(desiredDate);
        editableDate.setDate(editableDate.getDate() - 3);
        return today <= editableDate;
    });

    const handleEdit = () => {
        alert("変更画面に遷移します");
    };

    const handleDelete = () => {
        alert("削除が確定されました");
    };

    const formatConditionValue = (key: string, value: string | number | string[]) => {
        if (typeof value === "string" && value !== "") {
            const conditionKey = key.replace("_restriction", ""); 
            return conditionLabels[conditionKey]?.[value] || "希望なし";
        }
        return "希望なし";
    };

    return (
        <div className={styles.entryCard}>
            <div className={styles.entryDetails}>
                {/* 日時の表示 */}
                <div className={styles.entrySection}>
                    <h3 className={styles.sectionTitle}>日時</h3>
                    <ul className={styles.dateList}>
                        {participation.desired_dates.map((date, index) => (
                            <li key={index}>
                                {formatDate(date)} {formatTime(date)}
                            </li>
                        ))}
                    </ul>
                </div>

                {/* 希望条件の表示 */}
                <div className={styles.entrySection}>
                    <h3 className={styles.sectionTitle}>希望条件</h3>
                    <ul className={styles.conditionList}>
                        {Object.entries(fieldLabels).map(([key, label]) => (
                            <li key={key}>
                                {label} ：{" "}
                                {formatConditionValue(key, participation[key as keyof Participation])}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>

            {/* 変更・削除ボタン */}
            <div className={styles.entryButtons}>
                {isEditable && (
                    <>
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
                    </>
                )}
            </div>
        </div>
    );
}

