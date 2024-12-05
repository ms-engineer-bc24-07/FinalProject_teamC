"use client";

import { useRouter } from "next/navigation";
import InputField from "@/components/common/InputField/InputField";
import PrimaryButton from "@/components/common/PrimaryButton/PrimaryButton";

export default function AccountRegister() {
  const router = useRouter();

  const navigateToComp = () => {
    router.push("/individual/login/new/complete");
  };

  return (
    <div>
      <h1>情報登録</h1>
      <form>
        <InputField
          label="ユーザーネーム"
          type="text"
          placeholder="ユーザーネームを入力してください"
        />
        <InputField
          label="氏名"
          type="text"
          placeholder="姓と名の間にスペースを入れてください"
        />
        <InputField
          label="氏名（フリガナ）"
          type="text"
          placeholder="セイとメイの間にスペースを入れてください"
        />
        <InputField label="性別" type="text" />
        <InputField label="生まれ年" type="number" />
        <InputField label="入社年" type="number" />
        <InputField label="所属部署" type="text" />
        <InputField
          label="最寄り駅"
          type="text"
          placeholder="最寄り駅を入力してください"
        />
        <InputField
          label="パスワード"
          type="password"
          placeholder="パスワードを入力してください"
        />
        <InputField
          type="password"
          placeholder="もう一度パスワードを入力してください"
        />
      </form>
      <PrimaryButton onClick={navigateToComp}>登録</PrimaryButton>
    </div>
  );
}
