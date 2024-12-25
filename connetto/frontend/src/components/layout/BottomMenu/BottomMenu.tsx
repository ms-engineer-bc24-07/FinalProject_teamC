"use client";

import React, { useState } from 'react';
import Link from "next/link";
import { usePathname } from "next/navigation"
import AddHomeIcon from '@mui/icons-material/AddHome';
import ListAltIcon from '@mui/icons-material/ListAlt';
import EventIcon from '@mui/icons-material/Event';
import NotificationBadge from '../../notifications/NotificationBadge/NotificationBadge';
import styles from './BottomMenu.module.css';



export default function BottomMenu() {
    const pathname = usePathname();
    const unreadCount = 2; // 未読件数（バックエンドから取得する予定）

    return (
        <div className={styles.container}>
            {/* Home */}
            <Link 
                href="/individual/participation"
                className={`${styles.link} ${
                    pathname === "/individual/participation/add" ? styles.active : ""
                }`}
            >
                <AddHomeIcon className={styles.icon} />
                <span>Home</span>
            </Link>

            {/* My Entries */}
            <Link 
                href="/individual/entries"
                className={`${styles.link} ${
                    pathname === "/individual/entries" ? styles.active : ""
                }`}
            >
                <ListAltIcon className={styles.icon} />
                <span>My Entries</span>
            </Link>

            {/* Events */}
            <Link 
                href="/individual/events"
                className={`${styles.link} ${
                    pathname === "/individual/events" ? styles.active : ""
                }`}
            >
                <EventIcon className={styles.icon} />
                <span>Events</span>
            </Link>

            {/* Notifications */}
            <Link 
                href="/individual/notifications"
                className={`${styles.link} ${
                    pathname === "/individual/notifications" ? styles.active : ""
                }`}
            >
                <NotificationBadge className={styles.icon} />
                <span>Notification</span>
            </Link>
        </div>
    );
};
