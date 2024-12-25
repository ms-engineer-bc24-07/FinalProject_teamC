"use client";

import React, { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import axios from "axios";
import DrawerAppBar from '@/components/layout/DrawerAppBar/DrawerAppBar';
import TitleSection from '@/components/common/TitleSection/TitleSection';
import DateTimeList from "@/components/forms/DateTimePicker/DateTimeList";
import ConditionLayout from "@/components/forms/ConditionLayout/ConditionLayout";
import DropdownCondition from "@/components/forms/DropdownCondition/DropdownCondition";
import PrimaryButton from "@/components/common/PrimaryButton/PrimaryButton";
import BottomMenu from '@/components/layout/BottomMenu/BottomMenu';
import { getFirebaseToken } from "@/utils/auth";
import ModalConfirmation from "@/components/forms/ModalConfirmation/ModalConfirmation";

type Conditions = {
    gender: string;
    age: string;
    joining_year: string;
    department: string;
    atmosphere: string;
};

export default function EditParticipation() {
    const router = useRouter();
    const { id } = useParams(); 
    const [dates, setDates] = useState<string[]>([]);
    const [conditions, setConditions] = useState<Conditions>({
        gender: "",
        age: "",
        joining_year: "",
        department: "",
        atmosphere: "",
    });

    useEffect(() => {
        const fetchParticipation = async () => {
            try {
                const token = await getFirebaseToken();
                const response = await axios.get(`http://localhost:8000/api/participation/${id}/`, {
                    headers: { Authorization: `Bearer ${token}` },
                });
                const data = response.data;

                setDates(data.desired_dates);
                setConditions({
                    gender: data.gender_restriction,
                    age: data.age_restriction,
                    joining_year: data.joining_year_restriction,
                    department: data.department_restriction,
                    atmosphere: data.atmosphere_restriction,
                });
            } catch (err) {
                console.error("データ取得エラー:", err);
            }
        };

        fetchParticipation();
    }, [id]);

    const handleDropdownChange = (key: keyof typeof conditions) => (event: any) => {
        setConditions({ ...conditions, [key]: event.target.value });
    };

    const handleUpdate = async () => {
        try {
            const token = await getFirebaseToken();
            const data = {
                desired_dates: dates,
                gender_restriction: conditions.gender,
                age_restriction: conditions.age,
                joining_year_restriction: conditions.joining_year,
                department_restriction: conditions.department,
                atmosphere_restriction: conditions.atmosphere,
            };

            await axios.put(`http://localhost:8000/api/participation/${id}/`, data, {
                headers: { Authorization: `Bearer ${token}` },
            });

            alert("更新が完了しました。");
            router.push("/participation/"); 
        } catch (err) {
            console.error("更新エラー:", err);
        }
    };

    const handleCancel = () => {
        router.back(); 
    };

    return (
        <div style={{ marginTop: '40px', marginBottom: '60px' }}>
            <DrawerAppBar />
            <TitleSection title='登録内容の変更' />
            <DateTimeList onChange={setDates} initialDates={dates.map(date => ({ date: date, time: "" }))} />

            <TitleSection title='希望条件' />
            <ConditionLayout label="性別">
                <DropdownCondition
                    value={conditions.gender}
                    onChange={handleDropdownChange("gender")}
                    options={[
                        { value: "exact_match", label: "同期のみ" },
                        { value: "no_restriction", label: "希望なし" },
                    ]}
                />
            </ConditionLayout>
            <ConditionLayout label="年齢">
                <DropdownCondition
                    value={conditions.age}
                    onChange={handleDropdownChange("age")}
                    options={[
                        { value: "same_age", label: "同年代" },
                        { value: "broad_age", label: "幅広い年代" },
                        { value: "no_restriction", label: "希望なし" }
                    ]}
                />
            </ConditionLayout>
            <ConditionLayout label="入社年">
                <DropdownCondition
                    value={conditions.joining_year}
                    onChange={handleDropdownChange("joining_year")}
                    options={[
                        { value: "exact_match", label: "同期のみ" },
                        { value: "no_restriction", label: "希望なし" }
                    ]}
                />
            </ConditionLayout>
            <ConditionLayout label="部署">
                <DropdownCondition
                    value={conditions.department}
                    onChange={handleDropdownChange("department")}
                    options={[
                        { value: "same_department", label: "同じ部署内" },
                        { value: "mixed_departments", label: "他部署交流" },
                        { value: "no_restriction", label: "希望なし" }
                    ]}
                />
            </ConditionLayout>
            <ConditionLayout label="お店の雰囲気">
                <DropdownCondition
                    value={conditions.atmosphere}
                    onChange={handleDropdownChange("atmosphere")}
                    options={[
                        { value: "quiet", label: "落ち着いたお店" },
                        { value: "lively", label: "わいわいできるお店" },
                        { value: "no_restriction", label: "希望なし" }
                    ]}
                />
            </ConditionLayout>
            <PrimaryButton onClick={handleUpdate}>変更</PrimaryButton>
            <PrimaryButton onClick={handleCancel}>キャンセル</PrimaryButton>
            <BottomMenu />
        </div>
    );
}
