import React from "react";
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography, Box } from "@mui/material";

type ModalConfirmationProps = {
    open: boolean; 
    onClose: () => void;
    onConfirm: () => void;
        data: {
            dates: string[]; 
                conditions: { [key: string]: string };  
            };
};

export default function ModalConfirmation({ open, onClose, onConfirm, data }: ModalConfirmationProps) {
    return (
        <Dialog open={open} onClose={onClose}>
        <DialogTitle>登録が完了しました！</DialogTitle>
        <DialogContent>
            <Box sx={{ padding: "16px" }}>
            <Typography variant="subtitle1">以下の内容で登録されました：</Typography>
            <Typography variant="h6" sx={{ marginTop: "16px" }}>
                日時：
            </Typography>
            {data.dates.map((date, index) => (
                <Typography key={index} variant="body1" sx={{ marginBottom: "8px" }}>
                {date}
                </Typography>
            ))}
            <Typography variant="h6" sx={{ marginTop: "16px" }}>
                希望条件：
            </Typography>
            {Object.entries(data.conditions).map(([key, value], index) => (
                <Typography key={index} variant="body1">
                {key}：{value}
                </Typography>
            ))}
            </Box>
        </DialogContent>
        <DialogActions>
            <Button onClick={onClose} color="primary">
            戻る
            </Button>
            <Button onClick={onConfirm} color="primary" variant="contained">
            確定
            </Button>
        </DialogActions>
        </Dialog>
    );
    }
