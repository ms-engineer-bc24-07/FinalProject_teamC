import axios, { AxiosInstance, AxiosResponse } from "axios";
import { getFirebaseToken } from "@/utils/auth";

// Axiosインスタンスの作成
const api: AxiosInstance = axios.create({
    baseURL: "http://localhost:8000/api",
});

// リクエストInterceptorでトークンを付与
api.interceptors.request.use(
    async (config) => {
        const token = await getFirebaseToken();

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

/**
 * 認証付きAPIリクエスト関数
 * @param endpoint APIエンドポイント
 * @param method HTTPメソッド (GET, POST, PUT, DELETE)
 * @param data リクエストボディ (POSTやPUTの場合)
 * @returns APIレスポンスデータ
 */
export const authenticatedRequest = async <T>(
    endpoint: string,
    method: "GET" | "POST" | "PUT" | "DELETE" = "GET",
    data?: Record<string, unknown>
): Promise<AxiosResponse<T>> => {
    try {
        return api.request<T>({
            url: endpoint,
            method,
            data,
        });
    } catch (error) {
        console.error("APIリクエストエラー:", error);
        throw error; 
    }
};

export default api;
