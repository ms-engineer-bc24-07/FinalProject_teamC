"use client";

import React from "react";
import { Button } from "@mui/material";
import LogoutIcon from "@mui/icons-material/Logout";
import { useRouter } from "next/navigation";
import { getAuth, signOut } from "firebase/auth";

export default function LogoutButton() {
    const router = useRouter();

    const handleLogout = async () => {
        const auth = getAuth();
        try {
            await signOut(auth); 
            alert("ログアウトしました。");
            router.push("/"); 
        } catch (error) {
            console.error("ログアウトに失敗しました:", error);
            alert("ログアウトに失敗しました。もう一度お試しください。");
        }
    };

    return (
        <Button
            variant="contained"
            color="error"
            startIcon={<LogoutIcon />}
            onClick={handleLogout}
        >
            ログアウト
        </Button>
    );
}