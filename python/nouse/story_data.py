# story_data.py
story_nodes = {
    "start": {
        "text": "你在森林中迷路，前方有两个岔路口：\n1. 向左走（阴森的山洞）\n2. 向右走（明亮的村庄）",
        "choices": [
            {"text": "进山洞", "next_node": "cave", "require": None},  # 无前置条件
            {"text": "去村庄", "next_node": "village", "require": None}
        ]
    },
    "cave": {
        "text": "山洞里有一只熊！你需要逃跑...",
        "choices": [
            {"text": "往回跑", "next_node": "escape", "require": {"courage": 3}},  # 需要勇气≥3
            {"text": "装死", "next_node": "die", "require": None}
        ]
    },
    # 更多节点...（escape、die、village等）
}

# 初始角色属性
initial_player = {"courage": 2, "hp": 100}