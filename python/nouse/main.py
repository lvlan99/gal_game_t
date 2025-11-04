# main.py
from story_data import story_nodes, initial_player
from game_utils import print_text, choose_option, save_game, load_game

def start_game():
    # 璇㈤棶鏄惁璇绘。
    load_choice = input("鏄惁锷犺浇瀛樻。锛?y/n)锛?).lower()
    if load_choice == 'y':
        current_node, player = load_game()
        if not current_node:  # 璇绘。澶辫触鍒欎粠澶村紑濮?
            current_node = "start"
            player = initial_player.copy()
    else:
        current_node = "start"
        player = initial_player.copy()

    print_text("===== 妫滠鍐掗橹 =====")
    
    while True:
        # 銮峰彇褰揿墠鑺傜偣鏁版嵁
        node = story_nodes.get(current_node)
        if not node:
            print("鍓ф儏缁撴潫锛?)
            break
        
        # 灞旷ず鍓ф儏鏂囨湰
        print_text(node["text"])
        
        # 瀛樻。锷熻兘锛堥殢镞跺彲瀛樻。锛?
        if input("鏄惁瀛樻。锛?y/n)锛?).lower() == 'y':
            save_game(current_node, player)
        
        # 澶勭悊阃夐」锛堟棤阃夐」鍒欑粨鏉燂级
        if not node["choices"]:
            print("娓告垙缁撴潫锛?)
            break
        
        # 阃夋嫨涓嬩竴涓妭镣?
        current_node = choose_option(node["choices"], player)
        
        # 绀轰緥锛氶€夋嫨鍚庝慨鏀硅鑹插睘镐э纸濡傝繘灞辨礊鍕囨皵+1锛?
        if current_node == "cave":
            player["courage"] += 1
            print(f"浣犵殑鍕囨皵澧炲姞浜嗭紒褰揿墠鍕囨皵锛殁player['courage']}")

if __name__ == "__main__":
    start_game()