"use client";

import React, { useState } from 'react';
import Link from "next/link";
import AddHomeIcon from '@mui/icons-material/AddHome';
import ListAltIcon from '@mui/icons-material/ListAlt';
import EventIcon from '@mui/icons-material/Event';
import NotificationsIcon from '@mui/icons-material/Notifications';
import styles from './BottomMenu.module.css';

export default function BottomMenu() {
    const [activeTab, setActiveTab] = useState("home"); 

    return (
        <div className={styles.container}>
            {/* Home */}
            <Link 
                href="/individual/participation/add"
                className={`${styles.link} ${
                    activeTab === "home" ? styles.active : ""
                    }`}
                    onClick={() => setActiveTab("home")}
            >
                <AddHomeIcon className={styles.icon} />
                <span>Home</span>
            </Link>

            {/* My Entries */}
            <Link 
                href="/individual/entries"
                className={`${styles.link} ${
                    activeTab === "entries" ? styles.active : ""
                }`}
                onClick={() => setActiveTab("entries")}
            >
                <ListAltIcon className={styles.icon} />
                <span>My Entries</span>
            </Link>

            {/* Events */}
            <Link 
                href="/individual/events"
                className={`${styles.link} ${
                    activeTab === "events" ? styles.active : ""
                }`}
                onClick={() => setActiveTab("events")}
            >
                <EventIcon className={styles.icon} />
                <span>Events</span>
            </Link>

            {/* Notifications */}
            <Link 
                href="/individual/notifications"
                className={`${styles.link} ${
                    activeTab === "notifications" ? styles.active : ""
                }`}
                onClick={() => setActiveTab("notifications")}
            >
                <NotificationsIcon className={styles.icon} />
                <span>Notification</span>
            </Link>
        </div>
    );
};
