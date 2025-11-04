# game_utils.py
import json
import os
from time import sleep

# 文本逐字打印效果
def print_text(text, speed=0.05):
    for char in text:
        print(char, end='', flush=True)
        sleep(speed)
    print()  # 换行

# 处理选项选择（带容错）
def choose_option(choices, player):
    print("\n请选择：")
    valid_choices = []
    for i, choice in enumerate(choices, 1):
        # 检查选项是否满足条件（如勇气值）
        if choice["require"]:
            require_key = list(choice["require"].keys())[0]
            require_val = choice["require"][require_key]
            if player[require_key] < require_val:
                print(f"{i}. {choice['text']}（需要{require_key}≥{require_val}，当前不足）")
                continue
        valid_choices.append(choice)
        print(f"{i}. {choice['text']}")
    
    if not valid_choices:
        print("没有可用选项，游戏结束")
        return None
    
    while True:
        try:
            selected = int(input("输入选项编号：")) - 1
            if 0 <= selected < len(valid_choices):
                return valid_choices[selected]["next_node"]
            else:
                print("输入无效，请重试")
        except ValueError:
            print("请输入数字")

# 存档/读档（用JSON）
def save_game(current_node, player, save_name="save1"):
    if not os.path.exists("saves"):
        os.makedirs("saves")
    data = {"current_node": current_node, "player": player}
    with open(f"saves/{save_name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("存档成功！")

def load_game(save_name="save1"):
    try:
        with open(f"saves/{save_name}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        print("读档成功！")
        return data["current_node"], data["player"]
    except FileNotFoundError:
        print("没有找到存档")
        return None, None