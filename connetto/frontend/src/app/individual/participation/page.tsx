"use client";

import React, { useState } from "react";
import BottomMenu from '@/components/layout/BottomMenu/BottomMenu';
import DrawerAppBar from '@/components/layout/DrawerAppBar/DrawerAppBar';
import PrimaryButton from '@/components/common/PrimaryButton/PrimaryButton';
import TitleSection from '@/components/common/TitleSection/TitleSection';
import DateTimeList from "@/components/forms/DateTimePicker/DateTimeList";
import ConditionLayout from "@/components/forms/ConditionLayout/ConditionLayout";
import DropdownCondition from "@/components/forms/DropdownCondition/DropdownCondition";
import ModalConfirmation from "@/components/forms/ModalConfirmation/ModalConfirmation";
import { SelectChangeEvent  } from "@mui/material";
import { getAuth } from "firebase/auth";
import { getFirebaseToken } from "@/utils/auth"; 
import axios from "axios";


type Conditions = {
    gender: string;
    age: string;
    joining_year: string;
    department: string;
    atmosphere: string;
};

export default function AddParticipation() {
    const [conditions, setConditions] = useState<Conditions>({
        gender: "",
        age: "",
        joining_year: "",
        department: "",
        atmosphere: "",
    });

    const [dates, setDates] = useState<string[]>([]); 
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleDropdownChange = (key: keyof typeof conditions) => (event: SelectChangeEvent) => {
        setConditions({ ...conditions, [key]: event.target.value });
    };

    const handleRegister = () => {
        setIsModalOpen(true); 
    };

    const handleCloseModal = () => {
        setIsModalOpen(false); 
    };

    const handleConfirm = async () => {
        try {
            setError(null);
            console.log("登録処理を開始します...");

            const auth = getAuth();
            const currentUser = auth.currentUser;

            if (!currentUser) {
                throw new Error("ログインしていません。");
            }

            const uid = currentUser.uid; 
            console.log("ログイン中のユーザーUID:", uid);

            const data = {
                desired_dates: dates, 
                gender_restriction: conditions.gender,
                age_restriction: conditions.age,
                joining_year_restriction: conditions.joining_year,
                department_restriction: conditions.department,
                atmosphere_restriction: conditions.atmosphere,
                user: uid
            };
    
            console.log("送信データ:", data);
            
            const token = await getFirebaseToken();
            if (!token) {
                throw new Error("Firebaseトークンが取得できませんでした。再ログインしてください。");
            }

            console.log("取得したトークン:", token);

            const response = await axios.post(
                "http://localhost:8000/api/participation/", 
                data,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            console.log("登録成功:", response.data);
            alert("登録が完了しました！");
            setIsModalOpen(false); 
        } catch (err) {
            console.error("登録エラー:", err);
            setError("登録に失敗しました。入力内容を確認してください。");
            setIsModalOpen(false); 
        }
    };
    

    return (
        <div style={{ marginTop: '40px', marginBottom: '60px' }}>
            <DrawerAppBar />
            <TitleSection title='日時' />
            <DateTimeList onChange={setDates} />
            <TitleSection title='希望条件(任意)' />
            <div>
                <ConditionLayout label="性別">
                    <DropdownCondition
                        value={conditions.gender}
                        onChange={handleDropdownChange("gender")}
                        options={[
                                    { value: "same_gender", label: "同性" },
                                    { value: "no_restriction", label: "希望なし" },
                                ]}
                        placeholder="未選択"
                        />
                </ConditionLayout>
                <ConditionLayout label="世代">
                    <DropdownCondition
                        value={conditions.age}
                        onChange={handleDropdownChange("age")}
                        options={[
                            { value: "same_age", label: "同年代" },
                            { value: "broad_age", label: "幅広い年代" },
                            { value: "no_restriction", label: "希望なし" },
                        ]}
                        placeholder="未選択"
                        />
                </ConditionLayout>
                <ConditionLayout label="入社年">
                <DropdownCondition
                        value={conditions.joining_year}
                        onChange={handleDropdownChange("joining_year")}
                        options={[
                            { value: "exact_match", label: "同期のみ" },
                            { value: "no_restriction", label: "希望なし" },
                        ]}
                        placeholder="未選択"
                        />
                </ConditionLayout>
                <ConditionLayout label="部署">
                    <DropdownCondition
                    value={conditions.department}
                    onChange={handleDropdownChange("department")}
                    options={[
                        { value: "same_department", label: "同じ部署内" },
                        { value: "mixed_departments", label: "他部署交流" },
                        { value: "no_restriction", label: "希望なし" },
                    ]}
                    placeholder="未選択"
                    />
                </ConditionLayout>
                <ConditionLayout label="お店の雰囲気">
                    <DropdownCondition
                    value={conditions.atmosphere}
                    onChange={handleDropdownChange("atmosphere")}
                    options={[
                        { value: "quiet", label: "落ち着いたお店" },
                        { value: "lively", label: "わいわいできるお店" },
                        { value: "no_restriction", label: "希望なし" },
                    ]}
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
                    性別: conditions.gender,
                    年齢: conditions.age ,
                    同期: conditions.joining_year, 
                    部署: conditions.department,
                    雰囲気: conditions.atmosphere, 
                },
                }}
            />
        </div>
    );
}