import ActionButton from "@/components/common/ActionButton/ActionButton";
import React from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import styles from "./EntryCard.module.css";
import { formatDateTime, formatDate, formatTime } from "@/utils/dateUtils";

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
    onDeleteSuccess: () => void;
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

export default function EntryCard({ participation , onDeleteSuccess}: EntryCardProps) {
    const router = useRouter();

    const today = new Date();

    const isEditable = participation.desired_dates.some((date) => {
        const desiredDate = new Date(date);
        const editableDate = new Date(desiredDate);
        editableDate.setDate(editableDate.getDate() - 3);
        return today <= editableDate;
    });

    const handleEdit = () => {
        router.push(`entries/edit/${participation.id}`);
    };

    const handleDelete = async () => {
        const confirmDelete = window.confirm("本当にこの登録内容を削除しますか？");
        if (!confirmDelete) return;

        try {
            await axios.delete(`http://localhost:8000/api/participation/${participation.id}/`);
            alert("削除が完了しました。");
            onDeleteSuccess(); 
        } catch (error) {
            console.error("削除に失敗しました:", error);
            alert("削除に失敗しました。もう一度お試しください。");
        }
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
            <div className={styles.row}>
                <div className={styles.label}>日時</div>
                <div className={styles.value}>
                    {participation.desired_dates.map((date, index) => (
                        <div key={index}>
                            {formatDateTime(date)}
                        </div>
                    ))}
                </div>
            </div>
            <div className={styles.row}>
                <div className={styles.label}>希望条件</div>
                <div className={styles.value}>
                    {Object.entries(fieldLabels).map(([key, label]) => (
                        <li key={key}>
                            {label} ：{" "}
                            {formatConditionValue(key, participation[key as keyof Participation])}
                        </li>
                    ))}
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

