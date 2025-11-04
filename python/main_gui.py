
import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

story_nodes = {
"start": {
"text": "小蓝在公司看到温和的小绿，心生好感却不敢靠近：\n1. 尝试主动搭话 \n2. 用编程制作机器人寄托情感",
"choices": [
{"text": "主动搭话", "next_node": "talk", "require": None},
{"text": "制作机器人", "next_node": "create_robot", "require": None}
]
},
"talk": {
"text": "小蓝紧张到结巴，小绿笑着递咖啡：“新拿铁，要试试吗？”\n（社交值 + 2）",
"choices": [
{"text": "接咖啡聊工作", "next_node": "work_chat", "require": None},
{"text": "紧张跑开", "next_node": "embarrassed", "require": None}
]
},
"create_robot": {
"text": "小蓝做出机绿，机绿睁眼：“你好！”\n（编程值 + 3，获得【机绿】）",
"choices": [
{"text": "教机绿认世界", "next_node": "teach", "require": None},
{"text": "让机绿分析小绿喜好", "next_node": "robot_help", "require": None}
]
},
"work_chat": {
"text": "小蓝和小绿聊得投缘，小绿坦言：“我脸盲，靠笔记本记人。”\n（信任值 + 2）",
"choices": [
{"text": "分享自己社交困扰", "next_node": "good_end1", "require": None},
{"text": "转移话题", "next_node": "normal_end1", "require": None}
]
},
"embarrassed": {
"text": "小蓝跑回座位，机绿钻出来：“我帮你解释！”\n（机绿好感 + 1）",
"choices": [
{"text": "让机绿帮忙", "next_node": "mediator", "require": None},
{"text": "阻止机绿", "next_node": "bad_end1", "require": None}
]
},
"teach": {
"text": "机绿问：“我为什么和小绿长得一样？”\n（耐心值 + 2）",
"choices": [
{"text": "坦白喜欢小绿", "next_node": "confess", "require": None},
{"text": "岔开话题", "next_node": "avoid", "require": None}
]
},
"robot_help": {
"text": "机绿：“小绿爱买薄荷糖、看科幻片！”\n（攻略值 + 2）",
"choices": [
{"text": "便利店等小绿", "next_node": "meet", "require": None},
{"text": "买电影票", "next_node": "ticket", "require": None}
]
},
"good_end1": {
"text": "小蓝说自己怕社交，小绿笑：“我也怕麻烦人，我们很像！”\n 两人距离消失。\n【好结局：知己羁绊】",
"choices": []
},
"normal_end1": {
"text": "小蓝转移话题，小绿失落离开，两人变回客气同事。\n【普通结局：同事距离】",
"choices": []
},
"mediator": {
"text": "机绿告诉小绿真相，小绿笑：“我等他再主动。”\n（小绿好感 + 2）",
"choices": [
{"text": "找小绿道歉", "next_node": "good_end2", "require": None},
{"text": "继续犹豫", "next_node": "bad_end2", "require": None}
]
},
"bad_end1": {
"text": "小蓝阻止机绿，只能远远看小绿，孤独感加重。\n【坏结局：孤独观望】",
"choices": []
},
"confess": {
"text": "机绿兴奋：“我帮你送礼物！”\n（机绿助攻 + 3）",
"choices": [
{"text": "送薄荷糖", "next_node": "good_end3", "require": None},
{"text": "再想想", "next_node": "normal_end2", "require": None}
]
},
"avoid": {
"text": "机绿偷偷观察小绿，小蓝假装没看见。\n 两人关系无进展。\n【普通结局：原地停留】",
"choices": []
},
"meet": {
"text": "小蓝在便利店遇小绿：“我也爱这口味！” 小绿惊喜答应同行。\n（攻略值 + 3）\n【好结局：同行相伴】",
"choices": []
},
"ticket": {
"text": "机绿偷偷把电影票给小绿，小绿约小蓝周末观影。\n【好结局：电影之约】",
"choices": []
},
"good_end2": {
"text": "小蓝道歉，小绿笑：“我以前也怕交流，周末看电影吗？”\n【好结局：主动邀约】",
"choices": []
},
"bad_end2": {
"text": "小蓝犹豫，看到小绿和朋友看电影的朋友圈，后悔不已。\n【坏结局：错过机会】",
"choices": []
},
"good_end3": {
"text": "机绿送薄荷糖，小绿笑着找小蓝：“下次一起买？”\n【好结局：薄荷约定】",
"choices": []
},
"normal_end2": {
"text": "小蓝犹豫没送礼物，小绿没察觉心意，关系无进展。\n【普通结局：犹豫错过】",
"choices": []
}
}

initial_player = {"social": 1, "programming": 3, "patience": 2, "strategy": 1}

class StoryGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title ("小绿和小蓝 - 机器人篇")
        self.geometry ("700x500")
        self.current_node = "start"
        self.player = initial_player.copy ()
      
        self.create_menu()
    
        text_frame = tk.Frame(self)
        text_frame.pack(padx=15, pady=8, fill=tk.BOTH, expand=True)
        text_scroll = tk.Scrollbar(text_frame, orient=tk.VERTICAL)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area = tk.Text (
            text_frame,
            wrap=tk.WORD,
            bg="#f0f8ff",
            font=("微软雅黑", 11),
            yscrollcommand=text_scroll.set
        )
        self.text_area.pack (side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scroll.config (command=self.text_area.yview)
        self.text_area.config (state=tk.DISABLED)

        self.choices_frame = tk.Frame(self, bg="#f0f8ff")
        self.choices_frame.pack(padx=15, pady=8, fill=tk.X)
        self.update_story()
    def create_menu (self):
        menubar = tk.Menu (self)
        save_menu = tk.Menu (menubar, tearoff=0)
        save_menu.add_command (label="存档", command=self.save_game)
        save_menu.add_command (label="读档", command=self.load_game)
        menubar.add_cascade (label="游戏", menu=save_menu)
        self.config (menu=menubar)
    def update_story(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        for widget in self.choices_frame.winfo_children():
            widget.destroy()
        node = story_nodes.get (self.current_node)
        if not node:
            self.text_area.insert (tk.END, "剧情结束，感谢游玩！")
            self.text_area.config (state=tk.DISABLED)
            return

        self.text_area.insert (tk.END, f"【属性】社交: {self.player ['social']} | 编程: {self.player ['programming']} | 耐心: {self.player ['patience']} | 攻略: {self.player ['strategy']}\n\n")
        self.text_area.insert (tk.END, node ["text"])
        self.text_area.config (state=tk.DISABLED)
        for choice in node ["choices"]:
            btn = tk.Button (
                self.choices_frame,
                text=choice ["text"],
                command=lambda c=choice: self.choose_choice (c),
                font=("微软雅黑", 10),
                height=2,
                wraplength=self.winfo_width ()-30,
                bg="#b3e0ff"
            )
            btn.pack (fill=tk.X, pady=4, padx=8)
    def choose_choice(self, choice):
        next_node = choice["next_node"]

        if next_node == "talk":
            self.player["social"] += 2
        elif next_node == "create_robot":
            self.player["programming"] += 3
        elif next_node == "teach":
            self.player["patience"] += 2
        elif next_node == "robot_help" or next_node == "meet":
            self.player["strategy"] += 2 if next_node == "robot_help" else 3
        self.current_node = next_node
        self.update_story()

    def save_game (self):
        save_name = simpledialog.askstring ("存档", "输入存档名：", parent=self)
        if not save_name:
            return
        os.makedirs ("saves", exist_ok=True)
        with open (f"saves/{save_name}.json", "w", encoding="utf-8") as f:
            json.dump ({"current_node": self.current_node, "player": self.player}, f, ensure_ascii=False)
        messagebox.showinfo ("提示", f"存档 '{save_name}' 成功！")
    def load_game (self):
        save_name = simpledialog.askstring ("读档", "输入存档名：", parent=self)
        if not save_name:
            return
        try:
            with open (f"saves/{save_name}.json", "r", encoding="utf-8") as f:
                data = json.load (f)
            self.current_node = data ["current_node"]
            self.player = data ["player"]
            self.update_story ()
            messagebox.showinfo ("提示", f"读档 '{save_name}' 成功！")
        except FileNotFoundError:
            messagebox.showerror ("错误", "未找到该存档！")

if __name__ == "__main__":
    game = StoryGame()
    game.mainloop()
