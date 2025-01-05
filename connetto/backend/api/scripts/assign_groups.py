from api.services.group_service import assign_users_to_groups

def run_group_assignment():
    print("グループ分けを開始します...")
    try:
        groups, leaders = assign_users_to_groups()
    except ValueError as e:
        print(f"[ERROR] assign_users_to_groups の戻り値に問題があります: {e}")
        return
    
    # デバッグ: groups と leaders の型と中身を確認
    print(f"[DEBUG] groups の型: {type(groups)}")
    print(f"[DEBUG] groups の中身: {groups}")
    print(f"[DEBUG] leaders の型: {type(leaders)}")
    print(f"[DEBUG] leaders の中身: {leaders}")

    print("\n==== 結果 ====")
    for group in groups:
        print(f"\nグループ日時: {group['meeting_date']}")
        print("メンバー:")
        for user in group['users']:
            # デバッグ: user の型と内容を確認
            print(f"[DEBUG] user の型: {type(user)}")
            print(f"[DEBUG] user の中身: {user}")
            
            # メンバー情報の表示
            print(f"- {user.username}")
    
    print("\nリーダー:")
    for group_name, leader in leaders.items():
        # デバッグ: leader の型と内容を確認
        print(f"[DEBUG] group_name: {group_name}")
        print(f"[DEBUG] leader の型: {type(leader)}")
        print(f"[DEBUG] leader の中身: {leader}")

        # リーダー情報の表示
        print(f"{group_name}: {leader}")
    

# 関数を呼び出し
run_group_assignment()
