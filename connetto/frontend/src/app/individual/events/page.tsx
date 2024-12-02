"use client";

import React, { useState } from "react";
import { Box, Tabs, Tab, Typography } from "@mui/material";
import DrawerAppBar from "@/components/layout/DrawerAppBar/DrawerAppBar"; // 上部メニューバー
import BottomMenu from "@/components/layout/BottomMenu/BottomMenu"; // 下部ボトムメニュー
import EventCard from "@/components/common/EventCard/EventCard";

type Event = {
  id: number;
  name: string;
  date: string;
  description: string;
};

//モックデータ
const confirmedEvents = [
  {
    date: "2024年12月04日（水） 19:00",
    station: "新橋駅周辺",
    attendees: 8,
    restaurant: "焼肉 銀座園",
    details: "東京都港区新橋1-12-1 3F",
  },
];

const pendingEvents = [
  {
    date: "2024年12月10日（水） 19:00",
    station: "池袋駅周辺",
    attendees: 6,
    restaurant: undefined,
  },
];


export default function Events() {
  const [currentTab, setCurrentTab] = useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

  return (
    <Box sx={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
      <DrawerAppBar />
      <Box
        sx={{
          marginTop: "20px",
          position: "sticky",
          top: "60px", 
          zIndex: 100,
          backgroundColor: "#fff",
          padding: "8px 0",
          borderBottom: "1px solid #ddd",
        }}
      >
        <Tabs
          value={currentTab}
          onChange={handleChange}
          centered
          sx={{
            "& .MuiTab-root": {
              minWidth: "50%",
              fontWeight: "bold",
              fontSize: "16px", 
              padding: "12px 0", 
              backgroundColor: "#fff", 
              color: "#A09CAB", 
            },
            "& .Mui-selected": {
              backgroundColor: "#fff",
              color: "#000 !important", 
            },
            "& .MuiTabs-indicator": {
              backgroundColor: "#000", 
              height: "4px", 
              borderRadius: "2px", 
            },
          }}
        >
          <Tab label="開催予定" />
          <Tab label="参加履歴" />
        </Tabs>
      </Box>
      <Box sx={{ flex: 1, overflowY: "auto", padding: "16px" }}>
        {currentTab === 0 &&
          confirmedEvents.map((event, index) => (
            <EventCard key={index} {...event} />
          ))}
        {currentTab === 1 &&
          pendingEvents.map((event, index) => (
            <EventCard key={index} {...event} />
          ))}
      </Box>
      <BottomMenu />
    </Box>
  );
}

