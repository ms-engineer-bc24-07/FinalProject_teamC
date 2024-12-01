"use client";

import React, { useState } from "react";
import BottomMenu from '@/components/BottomMenu/BottomMenu';
import DrawerAppBar from '@/components/Header/DrawerAppBar';
import PrimaryButton from '@/components/PrimaryButton/PrimaryButton';
import TitleSection from '@/components/TitleSection/TitleSection';
import ToggleSwitch from '@/components/ToggleSwitch/ToggleSwitch';
import DateTimeList from "@/components/DateTimePicker/DateTimeList";
import ConditionLayout from "@/components/ConditionLayout/ConditionLayout";
import DropdownCondition from "@/components/DropdownCondition/DropdownCondition";
import ModalConfirmation from "@/components/ModalConfirmation/ModalConfirmation";
import { SelectChangeEvent  } from "@mui/material";


type Conditions = {
    sameGender: boolean;
    closeAge: boolean;
    coworkers: boolean;
    department: string;
    atmosphere: string;
};

export default function AddParticipation() {
    const [conditions, setConditions] = useState<Conditions>({
        sameGender: false,
        closeAge: false,
        coworkers: false,
        department: "",
        atmosphere: "",
    });

    // 登録内容（モックデータとして定義）
    const [dates, setDates] = useState<string[]>(["2024年12月08日（金） 19:00", "2024年12月10日（水） 18:00"]); // ダミーデータ
    const [isModalOpen, setIsModalOpen] = useState(false);
        
    const handleDropdownChange = (key: keyof typeof conditions) => (event: SelectChangeEvent) => {
        setConditions({ ...conditions, [key]: event.target.value });
    };
    
    const handleToggleChange = (key: keyof Conditions) => (event: React.ChangeEvent<HTMLInputElement>) => {
        setConditions({ ...conditions, [key]: event.target.checked });
    };

    const handleRegister = () => {
        setIsModalOpen(true); // モーダルを開く
    };
    
    const handleCloseModal = () => {
        setIsModalOpen(false); // モーダルを閉じる
    };
    
    const handleConfirm = () => {
        console.log("登録が確定しました:", { dates, conditions });
        setIsModalOpen(false); // モーダルを閉じる
        // 登録確定の処理をここに追加
    };

    return (
        <div style={{ marginTop: '40px' }}>
            <DrawerAppBar />
            <TitleSection title='日時' />
            <DateTimeList />
            <TitleSection title='希望条件(任意)' />
            <div>
                <ConditionLayout label="同性のみを希望">
                    <ToggleSwitch
                        checked={conditions.sameGender}
                        onChange={handleToggleChange("sameGender")}
                    />
                </ConditionLayout>
                <ConditionLayout label="同年代を希望">
                    <ToggleSwitch
                        checked={conditions.closeAge}
                        onChange={handleToggleChange("closeAge")}
                    />
                </ConditionLayout>
                <ConditionLayout label="同期を希望">
                    <ToggleSwitch
                        checked={conditions.coworkers}
                        onChange={handleToggleChange("coworkers")}
                    />
                </ConditionLayout>
                <ConditionLayout label="部署の指定">
                    <DropdownCondition
                    value={conditions.department}
                    onChange={handleDropdownChange("department")}
                    options={["同じ部署内", "他部署交流"]}
                    placeholder="未選択"
                    />
                </ConditionLayout>
                <ConditionLayout label="お店の雰囲気">
                    <DropdownCondition
                    value={conditions.atmosphere}
                    onChange={handleDropdownChange("atmosphere")}
                    options={["落ち着いた", "賑やか"]}
                    placeholder="未選択"
                    />
                </ConditionLayout>
            </div>
            <PrimaryButton onClick={handleRegister}>登録</PrimaryButton>
            <BottomMenu />
            {/* 確認モーダル */}
            <ModalConfirmation
                open={isModalOpen}
                onClose={handleCloseModal}
                onConfirm={handleConfirm}
                data={{
                dates: dates,
                conditions: {
                    性別: conditions.sameGender ? "同性のみ" : "指定なし",
                    年齢: conditions.closeAge ? "同年代" : "指定なし",
                    同期: conditions.coworkers ? "同期" : "指定なし",
                    部署: conditions.department || "未選択",
                    雰囲気: conditions.atmosphere || "未選択",
                },
                }}
            />
        </div>
    );
}