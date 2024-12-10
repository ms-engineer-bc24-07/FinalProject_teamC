"use client";

import { useRouter } from "next/navigation";
import InputField from "@/components/common/InputField/InputField";
import PrimaryButton from "@/components/common/PrimaryButton/PrimaryButton";
import TitleSection from "@/components/common/TitleSection/TitleSection";
import { useState } from "react";
import api from "@/utils/api";
import axios from "axios";
import { getFirebaseToken } from "@/utils/auth";
import CustomSelectField from "@/components/common/CustomSelectField/CustomSelectField";

export default function AccountRegister() {
    const router = useRouter();

    const [formData, setFormData] = useState({
        username: "",
        full_name: "",
        furigana: "",
        gender: "",
        birth_year: "",
        join_year: "",
        department: "",
        station: "",
    });

    const currentYear = new Date().getFullYear();
    const birthYearOptions = Array.from({ length: 65 }, (_, i) => ({
        value: String(currentYear - 16 - i),
        label: `${currentYear - 16 - i}`,
    }));
    const joinYearOptions = Array.from({ length: 65 }, (_, i) => ({
        value: String(currentYear - i),
        label: `${currentYear - i}`,
    }));

    const genderOptions = [
        { value: "male", label: "男性" },
        { value: "female", label: "女性" },
    ];

    // 修正された handleChange 関数
    const handleChange = (key: keyof typeof formData, value: string) => {
        setFormData({ ...formData, [key]: value });
    };

    const isValidForm = () => {
        if (!formData.username) {
            alert("ユーザーネームを入力してください");
            return false;
        }
        if (!formData.full_name) {
            alert("氏名を入力してください");
            return false;
        }
        if (!formData.furigana) {
            alert("フリガナを入力してください");
            return false;
        }
        return true;
    };

    const handleSubmit = async () => {
        if (!isValidForm()) return;

        try {
            console.log("送信データ:", formData);

            const token = await getFirebaseToken();
            console.log("取得したトークン:", token);

            if (!token) {
                console.error("トークンが取得できませんでした。");
                return;
            }

            const response = await api.post(
                "/user-profile/",
                formData,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            console.log("登録成功:", response.data);
            router.push("/individual/login/new/complete");
        } catch (error) {
            if (axios.isAxiosError(error)) {
                console.error("エラー詳細:", error.response?.data || error.message);
            } else {
                console.error("予期しないエラー:", error);
            }
        }
    };

    return (
        <div>
            <TitleSection title="情報登録" />
            <form>
                <InputField
                    label="ユーザーネーム"
                    type="text"
                    name="username"
                    placeholder="ユーザーネームを入力してください"
                    value={formData.username}
                    onChange={(e) => handleChange("username", e.target.value)}
                />
                <InputField
                    label="氏名"
                    type="text"
                    name="full_name"
                    placeholder="姓と名の間にスペースを入れてください"
                    value={formData.full_name}
                    onChange={(e) => handleChange("full_name", e.target.value)}
                />
                <InputField
                    label="氏名（フリガナ）"
                    type="text"
                    name="furigana"
                    placeholder="セイとメイの間にスペースを入れてください"
                    value={formData.furigana}
                    onChange={(e) => handleChange("furigana", e.target.value)}
                />
                <CustomSelectField
                    label="性別"
                    value={formData.gender}
                    options={genderOptions}
                    onChange={(value) => handleChange("gender", value)}
                />
                <CustomSelectField
                    label="生まれ年"
                    value={formData.birth_year}
                    options={birthYearOptions}
                    onChange={(value) => handleChange("birth_year", value)}
                />
                <CustomSelectField
                    label="入社年"
                    value={formData.join_year}
                    options={joinYearOptions}
                    onChange={(value) => handleChange("join_year", value)}
                />
                <InputField
                    label="所属部署"
                    type="text"
                    name="department"
                    value={formData.department}
                    onChange={(e) => handleChange("department", e.target.value)}
                />
                <InputField
                    label="最寄り駅"
                    type="text"
                    name="station"
                    placeholder="最寄り駅を入力してください"
                    value={formData.station}
                    onChange={(e) => handleChange("station", e.target.value)}
                />
            </form>
            <PrimaryButton onClick={handleSubmit}>登録</PrimaryButton>
        </div>
    );
}
