import React from "react";
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    Typography,
    Box,
} from "@mui/material";
import { formatDate, formatTime } from "@/utils/dateUtils"; 

type ModalConfirmationProps = {
    open: boolean;
    onClose: () => void;
    onConfirm: () => void;
    data: {
        dates: string[];
        conditions: { [key: string]: string };
    };
};

const conditionLabels: { [key: string]: { [key: string]: string } } = {
    gender: {
        same_gender: "同性",
        no_restriction: "希望なし",
    },
    age: {
        same_age: "同年代",
        broad_age: "幅広い年代",
        no_restriction: "希望なし",
    },
    joining_year: {
        exact_match: "同期のみ",
        no_restriction: "希望なし",
    },
    department: {
        same_department: "同じ部署内",
        mixed_departments: "他部署交流",
        no_restriction: "希望なし",
    },
    atmosphere: {
        quiet: "落ち着いたお店",
        lively: "わいわいできるお店",
        no_restriction: "希望なし",
    },
};

const conditionFieldLabels: { [key: string]: string } = {
    gender: "性別",
    age: "年齢",
    joining_year: "入社年",
    department: "部署",
    atmosphere: "お店の雰囲気",
};

export default function ModalConfirmation({
    open,
    onClose,
    onConfirm,
    data,
}: ModalConfirmationProps) {
    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>登録が完了しました！</DialogTitle>
            <DialogContent>
                <Box sx={{ padding: "16px" }}>
                    <Typography variant="subtitle1">以下の内容で登録されました：</Typography>

                    {/* 日時 */}
                    <Typography variant="h6" sx={{ marginTop: "16px" }}>
                        日時：
                    </Typography>
                    {data.dates.map((date, index) => (
                        <Typography key={index} variant="body1" sx={{ marginBottom: "8px" }}>
                            {formatDate(date)} {formatTime(date)}
                        </Typography>
                    ))}

                    {/* 希望条件 */}
                    <Typography variant="h6" sx={{ marginTop: "16px" }}>
                        希望条件：
                    </Typography>
                    {Object.entries(data.conditions).map(([key, value], index) => (
                        <Typography key={index} variant="body1">
                            {conditionFieldLabels[key] || key}：{conditionLabels[key]?.[value]}
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

