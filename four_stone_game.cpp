#include <bits/stdc++.h>
using namespace std;
#define rep(i, n) for(int i = 0; i < (int)(n); i++)
#define all(x) (x).begin(),(x).end()
using ll = long long;
#define INF (long long)2e+18

// 現在の盤面を表す3次元配列
vector<vector<vector<int>>> board(4, vector<vector<int>>(4, vector<int>(4, 0)));
// 盤面出力用のMap
map<int, char> board_print_map;

// 現在の盤面を出力する
void print_now_board(){
  cout << "【現在の盤面】" << endl;
  for(int h=3; h>=0; h--){
    cout << "高さ：" << h+1 << endl;
    for(int i=0; i<4; i++){
      for(int j=0; j<4; j++){
        cout << board_print_map[board[h][i][j]];
      }
      cout << endl;
    }
  }
}

// 勝利条件を満たしているかを確認する O(300)?
int win_check(vector<vector<vector<int>>> board_now){
  int now_sum = 0;
  // 水平断面
  for(int h=0; h<4; h++){
    // 縦列チェック
    for(int j=0; j<4; j++){
      now_sum = 0;
      for(int i=0; i<4; i++){
        now_sum += board_now[h][i][j];
      }

      if(now_sum==4){
        return 1;
      }
      else if(now_sum==-4){
        return -1;
      }
    }
    
    // 横列チェック
    for(int i=0; i<4; i++){
      now_sum = 0;
      for(int j=0; j<4; j++){
        now_sum += board_now[h][i][j];
      }

      if(now_sum==4){
        return 1;
      }
      else if(now_sum==-4){
        return -1;
      }
    }

    // 斜めチェック
    now_sum = 0;
    for(int i=0; i<4; i++){
      now_sum += board_now[h][i][i];
    }

    if(now_sum==4){
      return 1;
    }
    else if(now_sum==-4){
      return -1;
    }

    now_sum = 0;
    for(int i=0; i<4; i++){
      now_sum += board_now[h][3-i][i];
    }

    if(now_sum==4){
      return 1;
    }
    else if(now_sum==-4){
      return -1;
    }
  }

  // 高さ列チェック
  for(int i=0; i<4; i++){
    for(int j=0; j<4; j++){
      now_sum = 0;
      for(int h=0; h<4; h++){
        now_sum += board_now[h][i][j];
      }

      if(now_sum==4){
        return 1;
      }
      else if(now_sum==-4){
        return -1;
      }
    }
  }

  // 縦断面の斜めチェック
  for(int j=0; j<4; j++){
    now_sum = 0;
    for(int i=0; i<4; i++){
      now_sum += board_now[i][i][j];
    }

    if(now_sum==4){
      return 1;
    }
    else if(now_sum==-4){
      return -1;
    }
  }

  // 横断面の斜めチェック
  for(int i=0; i<4; i++){
    now_sum = 0;
    for(int j=0; j<4; j++){
      now_sum += board_now[j][i][j];
    }

    if(now_sum==4){
      return 1;
    }
    else if(now_sum==-4){
      return -1;
    }
  }

  // 大斜めチェック
  now_sum = 0;
  for(int i=0; i<4; i++){
    now_sum+= board_now[i][i][i];
  }
  if(now_sum==4){
    return 1;
  }
  else if(now_sum==-4){
    return -1;
  }

  now_sum = 0;
  for(int i=0; i<4; i++){
    now_sum+= board_now[i][i][3-i];
  }
  if(now_sum==4){
    return 1;
  }
  else if(now_sum==-4){
    return -1;
  }

  now_sum = 0;
  for(int i=0; i<4; i++){
    now_sum+= board_now[i][3-i][i];
  }
  if(now_sum==4){
    return 1;
  }
  else if(now_sum==-4){
    return -1;
  }

  now_sum = 0;
  for(int i=0; i<4; i++){
    now_sum+= board_now[i][3-i][3-i];
  }
  if(now_sum==4){
    return 1;
  }
  else if(now_sum==-4){
    return -1;
  }

  return 0;
}

// 評価関数の集計に使う関数
int value_change_on_this_direction(int now_sum, int zero_count){
  if(now_sum==4){
    return -1000;
  }
  else if(now_sum==-4){
    return 1000;
  }

  if(now_sum==3 && zero_count==1){
    return -5;
  }
  else if(now_sum==-3 && zero_count==1){
    return 5;
  }

  if(now_sum==2 && zero_count==2){
    return -3;
  }
  else if(now_sum==-2 && zero_count==2){
    return 3;
  }

  return 0;
}

// 盤面の評価関数
int evaluate_board(vector<vector<vector<int>>> board_now){
  int value = 0;

  // 全体で等しく、コマ1つにつき1点の増減
  for(int h=0; h<4; h++){
    for(int i=0; i<4; i++){
      for(int j=0; j<4; j++){
        value -= board_now[h][i][j];
      }
    }
  } 

  // 角はさらに1点の増減
  for(int h=0; h<4; h+=3){
    for(int i=0; i<4; i+=3){
      for(int j=0; j<4; j+=3){
        value -= board_now[h][i][j];
      }
    }
  }

  // 中心8マスはさらに2点の増減
  for(int h=1; h<=2; h++){
    for(int i=1; i<=2; i++){
      for(int j=1; j<=2; j++){
        value -= board_now[h][i][j]*2;
      }
    }
  }

  // ここから先は4目揃いで固定±1000点リターン、3目リーチで5点、2目並びで3点の増減

  int now_sum = 0;
  int zero_count = 0;
  int value_change = 0;
  // 水平断面
  for(int h=0; h<4; h++){
    // 縦列チェック
    for(int j=0; j<4; j++){
      now_sum = 0;
      zero_count = 0;
      for(int i=0; i<4; i++){
        now_sum += board_now[h][i][j];
        if(board_now[h][i][j]==0) zero_count++;
      }

      value_change = value_change_on_this_direction(now_sum, zero_count);
      if(abs(value_change)>999){
        return value_change;
      }
      else{
        value += value_change;
      }
    }
    
    // 横列チェック
    for(int i=0; i<4; i++){
      now_sum = 0;
      zero_count = 0;
      for(int j=0; j<4; j++){
        now_sum += board_now[h][i][j];
        if(board_now[h][i][j]==0) zero_count++;
      }

      value_change = value_change_on_this_direction(now_sum, zero_count);
      if(abs(value_change)>999){
        return value_change;
      }
      else{
        value += value_change;
      }
    }

    // 斜めチェック
    now_sum = 0;
    zero_count = 0;
    for(int i=0; i<4; i++){
      now_sum += board_now[h][i][i];
      if(board_now[h][i][i]==0) zero_count++;
    }

    value_change = value_change_on_this_direction(now_sum, zero_count);
    if(abs(value_change)>999){
      return value_change;
    }
    else{
      value += value_change;
    }

    now_sum = 0;
    zero_count = 0;
    for(int i=0; i<4; i++){
      now_sum += board_now[h][3-i][i];
      if(board_now[h][3-i][i]==0) zero_count++;
    }

    value_change = value_change_on_this_direction(now_sum, zero_count);
    if(abs(value_change)>999){
      return value_change;
    }
    else{
      value += value_change;
    }
  }

  // 高さ列チェック
  for(int i=0; i<4; i++){
    for(int j=0; j<4; j++){
      now_sum = 0;
      zero_count = 0;
      for(int h=0; h<4; h++){
        now_sum += board_now[h][i][j];
        if(board_now[h][i][j]==0) zero_count++;
      }

      value_change = value_change_on_this_direction(now_sum, zero_count);
      if(abs(value_change)>999){
        return value_change;
      }
      else{
        value += value_change;
      }
    }
  }

  // 縦断面の斜めチェック
  for(int j=0; j<4; j++){
    now_sum = 0;
    zero_count = 0;
    for(int i=0; i<4; i++){
      now_sum += board_now[i][i][j];
      if(board_now[i][i][j]==0) zero_count++;
    }

    value_change = value_change_on_this_direction(now_sum, zero_count);
    if(abs(value_change)>999){
      return value_change;
    }
    else{
      value += value_change;
    }
  }

  // 横断面の斜めチェック
  for(int i=0; i<4; i++){
    now_sum = 0;
    zero_count = 0;
    for(int j=0; j<4; j++){
      now_sum += board_now[j][i][j];
      if(board_now[j][i][j]==0) zero_count++;
    }

    value_change = value_change_on_this_direction(now_sum, zero_count);
    if(abs(value_change)>999){
      return value_change;
    }
    else{
      value += value_change;
    }
  }

  // 大斜めチェック
  now_sum = 0;
  zero_count = 0;
  for(int i=0; i<4; i++){
    now_sum+= board_now[i][i][i];
    if(board_now[i][i][i]==0) zero_count++;
  }
  value_change = value_change_on_this_direction(now_sum, zero_count);
  if(abs(value_change)>999){
    return value_change;
  }
  else{
    value += value_change;
  }

  now_sum = 0;
  zero_count = 0;
  for(int i=0; i<4; i++){
    now_sum+= board_now[i][i][3-i];
    if(board_now[i][i][3-i]==0) zero_count++;
  }
  value_change = value_change_on_this_direction(now_sum, zero_count);
  if(abs(value_change)>999){
    return value_change;
  }
  else{
    value += value_change;
  }

  now_sum = 0;
  zero_count = 0;
  for(int i=0; i<4; i++){
    now_sum+= board_now[i][3-i][i];
    if(board_now[i][3-i][i]==0) zero_count++;
  }
  value_change = value_change_on_this_direction(now_sum, zero_count);
  if(abs(value_change)>999){
    return value_change;
  }
  else{
    value += value_change;
  }

  now_sum = 0;
  zero_count = 0;
  for(int i=0; i<4; i++){
    now_sum+= board_now[i][3-i][3-i];
    if(board_now[i][3-i][3-i]==0) zero_count++;
  }
  value_change = value_change_on_this_direction(now_sum, zero_count);
  if(abs(value_change)>999){
    return value_change;
  }
  else{
    value += value_change;
  }

  return value;
}

// 現在からdeep手目を全通り試す
// deepが奇数なら自手、偶数なら相手
// 返り値は{h, i, j, value}
vector<int> look_ahead(vector<vector<vector<int>>> board_now, int deep){
  // 最大n手後まで読む
  int n = 4;
  if(deep>n){
    return {-1, -1, -1, evaluate_board(board_now)};
  }

  // deep手目を打つ前に勝敗がついているなら評価値を返す
  int start_value = evaluate_board(board_now);
  if(abs(start_value)>999){
    return {-1, -1, -1, start_value};
  }

  int max_value = -1000;
  int min_value = 1000;
  vector<int> max_place(3,-1);
  vector<int> min_place(3,-1);
  // deep手目を全通り試す
  for(int i=0; i<4; i++){
    for(int j=0; j<4; j++){
      for(int h=0; h<4; h++){
        if(board_now[h][i][j]==0){
          vector<vector<vector<int>>> board_next = board_now;
          if(deep%2==1){
            board_next[h][i][j] = -1;
          }
          else{
            board_next[h][i][j] = 1;
          }
          vector<int> ret = look_ahead(board_next, deep+1);
          int now_value = ret[3];
          if(max_value<now_value){
            max_value = max(max_value, now_value);
            max_place = {h, i, j};
          }
          if(min_value>now_value){
            min_value = min(min_value, now_value);
            min_place = {h, i, j};
          }

          break;
        }
      }
    }
  }

  vector<int> ans;
  if(deep%2==1){
    ans = max_place;
    ans.push_back(max_value);
  }
  else{
    ans = min_place;
    ans.push_back(min_value);
  }

  // もうコマを置ける場所がない場合
  if(ans[0]==-1 && ans[1]==-1 && ans[2]==-1){
    return {-1, -1, -1, start_value};
  }

  return ans;
}

int main(){
  // 出力のためにMapを定義する
  board_print_map[0] = '-';
  board_print_map[1] = 'x';
  board_print_map[-1] = 'o';
  
  // これまでの盤面の履歴を作る
  stack<vector<vector<vector<int>>>> board_log;
  board_log.push(board);

  // 初期盤面を出力する
  print_now_board();
  cout << endl;
  

  // ゲーム部分
  int turn_count = 1;
  while(1){
    if(turn_count%2==1){
      // 先手(相手番)
      cout << "ターン:" << turn_count << " 次の手の座標を入力してください(高さ, 縦, 横)。" << endl;
      int input_h, input_i, input_j;
      cin >> input_h >> input_i >> input_j;

      // 入力値(-1, -1, -1)で2手巻き戻す。
      if(turn_count>1 && input_h==-1 && input_i==-1 && input_j==-1){
        turn_count-=2;
        board_log.pop();
        board = board_log.top();
        board_log.pop();

        cout << endl;
        cout << "2手巻き戻しました。" << endl;

        cout << endl;
        print_now_board();
        cout << endl;
        continue;
      }

      // 不正な入力の場合は再入力を促す
      if(input_h<1 || input_h>4 || input_i<1 || input_i>4 || input_j<1 || input_j>4){
        cout << "その場所にはコマを置けません。座標を再入力してください。"  << endl;
        cout << endl;
        continue;
      }
      else if(board[input_h-1][input_i-1][input_j-1] != 0){
        cout << "既にコマが存在する場所です。座標を再入力してください。"  << endl;
        cout << endl;
        continue;
      }
      else if(input_h!=1 && board[input_h-2][input_i-1][input_j-1] == 0){
        cout << "その場所にはコマを置けません。座標を再入力してください。"  << endl;
        cout << endl;
        continue;
      }

      // 盤面にコマを置く
      board[input_h-1][input_i-1][input_j-1] = 1;
      turn_count++;
    }
    else{
      // 後手(CPU番)
      vector<int> next_place = look_ahead(board, 1);
      board[next_place[0]][next_place[1]][next_place[2]] = -1;
      cout << "ターン:" << turn_count << " CPUは(" << next_place[0]+1 << ", " << next_place[1]+1 << ", " << next_place[2]+1 << ")にコマを置きました。" << endl;
      turn_count++;
    }

    // 現在の盤面を出力する
    cout << endl;
    print_now_board();
    cout << endl;

    board_log.push(board);

    // 勝利条件を満たしているか確認する
    if(win_check(board)==1){
      cout << "Opponent wins the game !!" << endl;
      return 0;
    }
    else if(win_check(board)==-1){
      cout << "COM player wins the game !!" << endl;
      return 0;
    }
    else if(turn_count>64){
      cout << "This game is draw !!" << endl;
      return 0;
    }

    cout << "現在の盤面評価値：" << evaluate_board(board) << endl;
    cout << endl;
  }
  
}