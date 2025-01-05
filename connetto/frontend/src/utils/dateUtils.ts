/**
 * UTCの日付をそのままフォーマットする関数（タイムゾーン変換を避ける）
 * @param dateString ISO 8601形式のUTC日時
 * @returns 日本時間でフォーマット済みの文字列（元のデータそのまま表示）
 */
export function formatDateTime(dateString: string): string {
    const date = new Date(dateString); // この時点でUTCとして解釈される

    const year = date.getUTCFullYear();
    const month = date.getUTCMonth() + 1; // 月は0から始まるため+1
    const day = date.getUTCDate();
    const weekday = ["日", "月", "火", "水", "木", "金", "土"][date.getUTCDay()];

    const hours = String(date.getUTCHours()).padStart(2, "0");
    const minutes = String(date.getUTCMinutes()).padStart(2, "0");

    return `${year}年${month}月${day}日（${weekday}） ${hours}:${minutes}`;
}

export function generateDateOptions(): string[] {
    const today = new Date();
    const start = new Date(today.setDate(today.getDate() + 4)); 
    const end = new Date(today.setDate(today.getDate() + 60)); 

    const options: string[] = [];
    for (let date = start; date <= end; date.setDate(date.getDate() + 1)) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const day = String(date.getDate()).padStart(2, "0");
        const weekDay = ["日", "月", "火", "水", "木", "金", "土"][date.getDay()];
        options.push(`${year}年${month}月${day}日（${weekDay}）`);
    }
    return options;
}

export function generateTimeOptions(): string[] {
    const options: string[] = [];
    for (let hour = 11; hour < 23; hour++) {
        for (let minute = 0; minute < 60; minute += 30) {
            const formattedHour = String(hour).padStart(2, "0");
            const formattedMinute = String(minute).padStart(2, "0");
            options.push(`${formattedHour}:${formattedMinute}`);
        }
    }
    return options;
}

export function formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString("ja-JP", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        weekday: "short",
    });
}

export function formatTime(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleTimeString("ja-JP", {
        hour: "2-digit",
        minute: "2-digit",
    });
}

export function formatDateTimeUTC(dateString: string): string {
    if (!dateString || typeof dateString !== "string") {
        console.error("Invalid dateString:", dateString);
        return "Invalid Date";
    }

    const [datePart, timePart] = dateString.split("T");
    if (!datePart || !timePart) {
        console.error("dateString のフォーマットが不正です:", dateString);
        return "Invalid Date";
    }

    const [hours, minutes] = timePart.split(":");
    const utcDate = new Date(dateString);

    // 曜日の取得
    const weekday = ["日", "月", "火", "水", "木", "金", "土"][utcDate.getUTCDay()];

    return `${datePart.replace(/-/g, "年").replace(/$/, "日")}（${weekday}） ${hours}:${minutes}`;
}