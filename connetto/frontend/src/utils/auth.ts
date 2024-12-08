import { getIdToken } from "firebase/auth";
import { auth } from "./firebase";

/**
 * @returns {Promise<string | null>} トークン文字列 (エラー時はnull)
 */
export const getFirebaseToken = async (): Promise<string | null> => {
    try {
        console.log("getFirebaseToken開始");

        // 現在のユーザーを取得
        const user = auth.currentUser;
        console.log("現在のユーザー:", user);

        if (!user) {
            throw new Error("ユーザーがログインしていません。");
        }

        // トークンを取得
        const token = await getIdToken(user);
        console.log("取得したトークン:", token);

        return token;
    } catch (err) {
        console.error("トークン取得エラー:", err);
        return null;
    }
};

