"use client";

import React, { useEffect, useState } from "react";
import BottomMenu from '@/components/layout/BottomMenu/BottomMenu';
import DrawerAppBar from '@/components/layout/DrawerAppBar/DrawerAppBar';
import TitleSection from '@/components/common/TitleSection/TitleSection';
import EntryCard from "@/components/Entries/EntryCard/EntryCard";
import axios from "axios";
import { getFirebaseToken } from "@/utils/auth";

type Participation = {
    id: number;
    desired_dates: string[];
    atmosphere_restriction: string;
    gender_restriction: string;
    age_restriction: string;
    joining_year_restriction: string;
    department_restriction: string;
    created_at: string;
};

export default function MyEntries() {
    const [entries, setEntries] = useState<Participation[]>([]);

    const fetchEntries = async () => {
        try {
            const token = await getFirebaseToken();

            if (!token) {
                throw new Error("認証トークンが取得できませんでした。");
            }

            const response = await axios.get("http://localhost:8000/api/participation/", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setEntries(response.data);
        } catch (error) {
            console.error("データの取得に失敗しました:", error);
        }
    };

    useEffect(() => {
        fetchEntries();
    }, []);

    return (
        <div style={{ marginTop: '40px', marginBottom: '60px' }}>
            <DrawerAppBar />
            <TitleSection title='登録内容確認' />
            <div>
                {entries.map((entry) => (
                    <EntryCard
                        key={entry.id}
                        participation={entry}
                        onDeleteSuccess={fetchEntries}
                    />
                ))}
            </div>
            <BottomMenu />
        </div>
    );
}