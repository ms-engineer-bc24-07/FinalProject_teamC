"use client";

import React, { useState } from "react";
import BottomMenu from '@/components/layout/BottomMenu/BottomMenu';
import DrawerAppBar from '@/components/layout/DrawerAppBar/DrawerAppBar';
import TitleSection from '@/components/common/TitleSection/TitleSection';
import EntryCard from "@/components/Entries/EntryCard/EntryCard";


export default function MyEntries() {

    return (
        <div style={{ marginTop: '40px', marginBottom: '60px' }}>
            <DrawerAppBar />
            <TitleSection title='登録内容確認' />
            <div>
              <EntryCard />
            </div>
            <BottomMenu />
        </div>
    );
}