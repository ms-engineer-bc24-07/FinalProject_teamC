import React from "react";
import { Switch } from "@mui/material";

type ToggleSwitchProps = {
    checked: boolean; 
    onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
};

export default function ToggleSwitch({ checked, onChange }: ToggleSwitchProps) {
    return <Switch checked={checked} onChange={onChange} />;
}


