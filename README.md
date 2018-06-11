## About
![icon](https://github.com/mzkii/jbt-simulator/blob/master/img/icon.png)

[#memo2](http://yosh52.web.fc2.com/jubeat/fumenformat.html) 形式の譜面を mac/windows 上で再生するシミュレータです．


## Sample
![sample01](https://github.com/mzkii/jbt-simulator/blob/master/screenshots/sample01.png)

## [WIP] 機能👷
基本的に，jubeatLab に準拠する．
- 譜面再生
  - 任意倍速，シーク
- 譜面作成


## [WIP] jubeat-memo 形式から譜面を再生するアルゴリズム
```
2

口口口① |①ーーー|

口④口口 |ーーーー|

口口③口 |ーー②ー|

口②口口 |③ー④ー|
```

- **|** から **|** までを **1拍** と呼ぶ

- 1拍が **4つ分** で **1小節** になる <-- ここ重要
  - あくまでも4拍で1小節なので，小節の手前にある小節数(2とか16とか)は構文解析には関係ない．
  - 単に編集時に見やすくするために付け加えているだけ．
  - 以下の例では，この小節を構成する条件を利用して，4行で位置情報を定義できない場合に，分割して表現している．
    - ⑭は③と位置が重なっているため，16小節目を2小節分に分けて表現している．**しかし，生成される小節データは①小節分である．**

```
16
口⑧口① |①②③④|
⑥⑨②⑩ |⑤⑥⑦⑧|
⑫③⑪④ |⑨⑩⑪⑫|
⑬⑤口⑦ |⑬ー⑭ー|

口口口口
口口口口
口⑭口口
口口口口
```

 
## 譜面を構成する型
### Note型
- 譜面を構成する最小単位
- Note(note: String, t: Double, position: Int, bpm: Double)
- note; その小節におけるノーツを特定するための Key (①, ②, ...)
- bpm; そのノーツが出現する際のBPM
- t; そのノーツが，現在の小節内において，ノーツをタップすべき時間

```
2
t=60
口口口① |①ーーー|

口④口口 |ーーーー|

口口③口 |ーー②ー|

口②口口 |③ー④ー|
```

  - 上記2小節目の①ノーツの例
```
bpm が 60 なので，1分間に 60 拍存在することになる．

すなわち一拍あたり 1000ms， 1ノーツあたり 250ms，

すなわち①ノーツは Note(①, 250, 4, 60) と求まる．
```
- position; そのノーツが表示すべきパネル番号(1~16)
```
パネル番号対応表;

01  02  03  04
05  06  07  08
09  10  11  12
13  14  15  16
```

### Measure型
- Note型 の集合体
- Measure(measure: Int, notes: List < Note >)
- measure; 何小節目か
- notes; measure 小節目に出現する Note 型の配列

### Chart型
- Measure型 の集合体
- 譜面の全体を構成する
- Chart(difficulty: Difficulty, level: Int, measures: List < Measure >)
- difficulty; 難易度(BASIC or ADVANCED or EXTREME)
- level; レベル(lv1 ~ lv10)
- measures; 小節の配列

### Music型
- 楽曲情報を保持
- 楽曲データに対して1対1に対応する
- Music(title: String, artist: String, charts: List < Chart >)
- title; 楽曲名
- artist; アーティスト名
- charts; 楽曲データ1曲分に対応する譜面データ(基本的には3難易度分存在する)

```
>> music.print()
Music(hogehoge, fugafuga, 
Chart(Difficulty.BASIC, 3, 
Measure(1, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
Measure(2, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
Measure(3, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
)
--------------------------------
Chart(Difficulty.ADVANCED, 7, 
Measure(1, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
Measure(2, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
Measure(3, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
)
--------------------------------
Chart(Difficulty.EXTREME, 9, 
Measure(1, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
Measure(2, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
Measure(3, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
)
--------------------------------
)

Process finished with exit code 0
```
## 解析アルゴリズム
- とりあえず，譜面ファイルを一行づつ読んでいく
- 以下の例の2小節目のデータを読んでいくことを考える
- ちなみに，ノーツデータが生成されるタイミングは2つある
```
2
t=60
口口口① |①ーーー|

口④口口 |ーーーー|

口口③口 |ーー②ー|

口②口口 |③ー④ー|
```
- 上の④では，**盤面データからノーツデータを生成** することになる．④が最初に出現した段階では，表示位置は6番パネルという情報は把握できるが，表示時間は未確定の状態である．すなわち Note(④, None, 6, 60) となる．Noneは未確定という意味．

- 上の②では，**時間データからノーツデータを生成** することになる．②が最初に出現した段階では，表示時間は **11x250=2750ms** という情報は把握できるが，表示位置は未確定の状態である．すなわち Note(②, 2750, None 60) となる．Noneは未確定という意味．

## fumen/sample.jbt を解析してみる
jbt-simulator 内では，一小節ごとを measure(配置データ，タイミングデータ) として表現し，

譜面一枚あたり measures という measure の配列で管理する．

例えば， sample.jbt の出力結果中の2小節目の譜面データを読み込むとすれば以下のようになる．
```
2 ['口口口①口④口口口口③口口②口口', ['①ーーー', 'ーーーー', 'ーー②ー', '③ー④ー']]
```

以下は，fumen/sample.jbtを読み込んで解析した結果．
len(measures)は 81 となり， sample.jbt の小節数と一致する．
15小節目のように，複数小節分にまたがって一小節を表現した場合は，自動的に配置データが連結される．

```
1 ['口口口口口口口口口口口口口口口口', ['ーーーー', 'ーーーー', 'ーーーー', 'ーーーー']]
2 ['口口口①口④口口口口③口口②口口', ['①ーーー', 'ーーーー', 'ーー②ー', '③ー④ー']]
3 ['口⑥①口③口口⑤口口口口④口②口', ['①ー②ー', '③ー④ー', '⑤ーーー', '⑥ーーー']]
4 ['⑧口口⑨⑦⑥④口口⑤③②口口口①', ['①②③④', '⑤⑥⑦⑧', '⑨ーーー', 'ーーーー']]
5 ['⑧④②⑥口口口口口口口口③⑦⑤①', ['①②ーー', '③④ーー', '⑤⑥ーー', '⑦⑧ーー']]
6 ['⑦口口口口①⑥口口口③口⑧⑤④②', ['①ー②ー', 'ー③④ー', 'ーー⑤⑥', '⑦ー⑧ー']]
7 ['口口③①口⑤口口⑦口口口⑧⑥④②', ['①ー②ー', '③ー④ー', '⑤ー⑥ー', '⑦ー⑧ー']]
8 ['口口口口口口⑥①口口③口⑦⑤④②', ['①ー②ー', 'ー③④ー', 'ーー⑤⑥', 'ーー⑦ー']]
9 ['口口口口口⑥口口口口②口⑤④③①', ['ーー①ー', 'ー②③ー', 'ーー④ー', 'ーー⑤⑥']]
10 ['⑤⑤①④③⑧①口②③⑥①口⑦口口', ['①ー②ー', '③④ーー', '⑤ーー⑥', '⑦ー⑧ー']]
11 ['口②①口口⑥⑤口⑥⑤④③②④③①', ['①ーーー', '②ーーー', '③ー④ー', '⑤ー⑥ー']]
12 ['④口①⑤①⑥⑤口口⑧⑦③①口③②', ['①ー②ー', '③④ーー', '⑤ーー⑥', '⑦ー⑧ー']]
13 ['④②①③④④③③口口口口②④③①', ['①ーーー', '②ーーー', '③ーーー', '④ーーー']]
14 ['⑥⑦⑧口口⑪⑩⑨④口③②口口⑤①', ['①ー②ー', '③④⑤ー', '⑥ー⑦ー⑧ー', '⑨ー⑩ー⑪ー']]
15 ['⑥⑥⑧口口⑧口⑧②③⑧④①⑤⑦⑦口口口口口口口口⑨口口口⑩口口口', ['①ー②ー', '③④⑤ー', '⑥ー⑦ー', '⑧ー⑨⑩']]
16 ['口⑧口①⑥⑨②⑩⑫③⑪④⑬⑤口⑦口口口口口口口口口⑭口口口口口口', ['①②③④', '⑤⑥⑦⑧', '⑨⑩⑪⑫', '⑬ー⑭ー']]
17 ['③③①①⑦⑦⑤⑤⑧⑨⑨口⑩④②⑥', ['①ー②ー③ー', '④ー⑤ー⑥ー', '⑦ー⑧ー⑨ー', '⑩ーーー']]
18 ['①口口＜口口口口口口口口口①＜口②口④口口口③⑤口口②⑥口②口⑦', ['①ーーー', 'ーーーー', '②ー③ー④ー', '⑤ー⑥ー⑦ー']]
19 ['⑨①⑨①④⑤⑥口③⑨⑦口②口⑧口口⑪口⑩口口口口口口口口口⑬口⑫', ['①②③④', '⑤⑥⑦⑧', '⑨ーーー', '⑩⑪⑫⑬']]
20 ['④⑥⑤⑤③口⑧⑤②口⑦口①口⑤口', ['①ー②ー', '③ー④ー', '⑤ー⑥ー', '⑦ー⑧ー']]
21 ['③⑨⑧④③⑤⑧④①口⑥②①⑦口②', ['①ー②ー', '③ー④ー', '⑤ー⑥ー⑦ー', '⑧ー⑨ー']]
22 ['②⑪⑩②③⑫⑨口④⑬⑧①⑤⑥⑦①', ['①ーーー', '②③④⑤', '⑥⑦⑧⑨', '⑩⑪⑫⑬']]
23 ['⑤⑨⑧④口⑩口③口⑪口②⑥⑫⑦①', ['①②③④', '⑤ー⑥ー', '⑦ー⑧ー', '⑨⑩⑪⑫']]
24 ['⑤⑭⑭④⑥⑫⑨③⑦⑪⑩②⑧口⑬①', ['①②③④', '⑤⑥⑦⑧', '⑨⑩⑪⑫', '⑬ー⑭ー']]
25 ['②口⑥⑥④口⑥①③口口①口⑤⑤①⑦⑦口口口⑦口口口口口口口口口口', ['①ー②ー', '③ー④ー', '⑤ー⑥ー', 'ーー⑦ー']]
26 ['口⑨⑨口④口⑥口①⑤③⑦①⑧⑧②⑩口口口口口口⑪⑩口口口口口口⑪', ['①ー②③', '④⑤⑥⑦', '⑧ー⑨ー', '⑩ー⑪ー']]
27 ['⑨⑦⑥①①②⑤口口③④⑧⑨口口口口口口⑩口口口口⑪口口口口口⑪口', ['①ー②③', '④⑤⑥⑦', '⑧ー⑨ー', '⑩⑪ーー']]
28 ['⑦⑤⑨口口①口口口②⑥⑧⑦③⑨④', ['①②③ー', '④ー⑤ー', '⑥ー⑦ー', '⑧ー⑨ー']]
29 ['⑨④口②⑤④③②口⑥③口⑦①口⑧', ['①ー②ー', '③ー④ー', '⑤ー⑥ー⑦ー', '⑧ー⑨ー']]
30 ['口⑧⑦①⑫⑨⑥⑬②⑩⑤③口⑪④口', ['①②③ー', '④⑤⑥⑦', '⑧⑨⑩⑪', '⑫ー⑬ー']]
31 ['⑤⑧⑤⑨口口⑦口口⑥④③⑥口①②', ['①②③④', '⑤ー⑥ー', 'ーー⑦⑧', '⑨ーーー']]
32 ['⑬口⑬口⑤⑥⑦⑧⑫⑪⑩⑨④③②①口口口口口口口口口口口口口⑭口⑭', ['①②③④', '⑤⑥⑦⑧', '⑨⑩⑪⑫', '⑬ー⑭ー']]
33 ['⑥⑦口①⑤③⑥口口④口口②口①口口口⑧⑧口口口口口口口口口口口口', ['①ー②ー', '③ー④ー', '⑤ー⑥⑦', 'ーー⑧ー']]
34 ['口⑤口口④⑥口①⑤口①口②③③①口口口口口口⑦口口口⑧口口口口⑦', ['①ー②ー', '③④ーー', '⑤ー⑥ー', '⑦ー⑧ー']]
35 ['①⑤⑤①口口口口②口⑦③⑥②口④', ['ーー①ー', '②③ーー', '④ー⑤⑥', '⑦ーーー']]
36 ['②⑦⑧①②②①①③④⑤⑥口②①口口口口⑨口口口口口口口口⑩口口口', ['①ーーー', '②ーーー', '③④⑤⑥⑦⑧', '⑨ー⑩ー']]
37 ['⑤口口⑧①⑥⑨③⑦口口⑩口②④口', ['①ー②ー', '③ー④ー', '⑤ー⑥ー⑦ー', '⑧ー⑨ー⑩ー']]
38 ['口⑤口口④⑥口①⑤口①口②③③①口口口口口口⑦口口口⑧口口口口⑦', ['①ー②ー', '③④ーー', '⑤ー⑥ー', '⑦ー⑧ー']]
39 ['①⑤⑤①口口口口②口⑦③⑥②口④', ['ーー①ー', '②③ーー', '④ー⑤⑥', '⑦ーーー']]
40 ['口⑦⑧⑨①①②②③④⑤⑥⑩①②口', ['①ーーー', '②ーーー', '③④⑤⑥⑦⑧', '⑨ー⑩ー']]
41 ['⑤口口⑧①⑥⑨③⑦口口⑩口②④口', ['①ー②ー', '③ー④ー', '⑤ー⑥ー⑦ー', '⑧ー⑨ー⑩ー']]
42 ['口③④④⑥⑥口⑤⑦口②口口①口口', ['①ー②ー', '③ーーー', '④ー⑤ー', '⑥ー⑦ー']]
43 ['②口②口口口①口口①④①③口①口', ['ーーーー', '①ーーー', '②ー③ー', '④ーーー']]
44 ['②③口①②②①①口⑥⑤④口②①口', ['①ーーー', '②ーーー', '③ーーー', '④⑤⑥ー']]
45 ['①⑦⑥⑦②口⑨口③口口口④⑧⑧⑤', ['①②③④⑤ーーー', '⑥ーーー', '⑦ーー⑧', 'ーー⑨ー']]
46 ['①④口④①①口③②口③③口⑤口口口口口口⑥口⑥口口口口口口口⑦口', ['①ーーー', '②ー③ー', '④ー⑤ー', '⑥ー⑦ー']]
47 ['⑧⑤①口⑦④⑩口⑥③⑨口②口口口口口⑪口口口口口口口口口口口口口', ['①ー②ー', '③ー④ー⑤ー', '⑥ー⑦ー⑧ー', '⑨ー⑩ー⑪ー']]
48 ['⑤④⑥⑤④③⑦⑥③②⑧⑦②①①⑧', ['①ー②ー', '③ー④ー', '⑤ー⑥ー', '⑦ー⑧ー']]
49 ['口④④口③②口④②③⑤口⑤①①⑤口口口口口⑥⑥口口口口口口⑥⑥口', ['①ー②ー', '③ーーー', '④ーー⑤', 'ーー⑥ー']]
50 ['①口＜口口口口口①口＜口口口口口', ['①ーーー', 'ーーーー', 'ーーーー', 'ーーーー']]
51 ['①口口口口＞口①①口口口口＞口①', ['①ーーー', 'ーーーー', 'ーーーー', 'ーーーー']]
52 ['口①口＜口口口①口①口＜口口口①', ['①ーーー', 'ーーーー', 'ーーーー', 'ーーーー']]
53 ['口①口口＞口①口口①口口＞口①口', ['①ーーー', 'ーーーー', 'ーーーー', 'ーーーー']]
54 ['①②③④口口①口＞①口口口口①口', ['①ーーー', '②ーーー', '③ーーー', '④ーーー']]
55 ['口口口口口口口①口①①＜口口口口口口口口口口口口口口口②口口④③', ['①ーーー', '②ーーー', '③ーーー', '④ーーー']]
56 ['口口口口＞①口口③口①口②①口口口口口口④口口口口口口口口口口口', ['①ーーー', '②ーーー', '③ーーー', '④ーーー']]
57 ['①②③④口①①＜口口口口口口口口', ['①ーーー', '②ーーー', '③ーーー', '④ーーー']]
58 ['③④⑤口⑥口①⑤⑦口⑤②①口口口', ['①ー②ー', '③④ーー', '⑤ーー⑥', '⑦ーーー']]
59 ['口口口①口①①口口②②口②口口口', ['①ーーー', '②ーーー', 'ーーーー', 'ーーーー']]
60 ['③④⑤口⑥口口⑤⑦口⑤②①口口口', ['①ー②ー', '③④ーー', '⑤ーー⑥', '⑦ーーー']]
61 ['口④④①③①①③③②②③②④④口', ['①ーーー', '②ーーー', '③ーーー', '④ーーー']]
62 ['⑤口⑦⑥口③口④⑤口②口口口口①', ['①ー②ー', '③④ーー', '⑤ーー⑥', '⑦ーーー']]
63 ['⑤⑤⑦口④⑦③⑦⑧②⑦口①口⑥⑥口口口口口口口口口口口口⑨口口口', ['①ー②ー', '③④ーー', '⑤ー⑥ー', '⑦ー⑧⑨']]
64 ['⑤③口④⑤口②⑥口口⑦①口口口口', ['①ー②ー', '③④ーー', '⑤ーー⑥', '⑦ーーー']]
65 ['口①①口③口口④③口口④口②②口', ['①ーーー②ー', 'ーー③ーーー', '④ーーー', 'ーーーー']]
66 ['口⑨⑤①⑦⑤③⑦⑩③⑥⑨①⑧②④⑪口口⑪口口口口口⑫口口口口口口', ['①ー②ー③ー', '④ー⑤ー⑥ー', '⑦ー⑧ー⑨ー', '⑩ー⑪ー⑫ー']]
67 ['口口口口口②Ｖ＜口口口口口口①口口④口＜口口口③口口口口口口口∧口口口口口口口口口口口口⑥＞＜⑤', ['①ーーー②ー', 'ーー③ーーー', '④ーーー⑤ー', 'ーー⑥ーーー']]
68 ['口⑤口口口③口④口口口口口口②⑥⑤⑨⑦⑥⑦③④⑤①口①③①⑧②⑨口口口口口⑭⑮口⑩⑪⑫⑬口口口口', ['①ー②ー③ー', '④ー⑤ー⑥ー', '⑦ー⑧ー⑨ー', '⑩⑪⑫⑬⑭⑮']]
69 ['③⑥⑤③④口口②⑦口＜口①⑤①口口Ｖ口口口口口Ｖ口⑨口口口口口⑧', ['①ー②ー③ー', '④ー⑤ー⑥ー', '⑦ーーー⑧ー', 'ーー⑨ーーー']]
70 ['口口口口口口口口⑧口口口口口口⑨①⑤⑦⑤⑦⑨③①⑩①⑥④③⑧②⑨⑪口口口口口口⑪口⑫口口口口口口', ['①ー②ー③ー', '④ー⑤ー⑥ー', '⑦ー⑧ー⑨ー', '⑩ー⑪ー⑫ー']]
71 ['⑨③⑥③⑤⑦①⑨口⑩④⑤①⑧②⑦口⑫口口口口⑪口⑪口口口口口口口', ['①ー②ー③ー', '④ー⑤ー⑥ー', '⑦ー⑧ー⑨ー', '⑩ー⑪ー⑫ー']]
72 ['⑦⑨③①⑧⑤⑩⑥口⑨②③⑤⑦①④口口口⑪口口口口口口⑪口口口⑫口', ['①ー②ー③ー', '④ー⑤ー⑥ー', '⑦ー⑧ー⑨ー', '⑩ー⑪ー⑫ー']]
73 ['⑦⑪①⑩口③口⑥②⑨⑧④③⑤⑫①', ['①ー②ー③ー', '④ー⑤ー⑥ー', '⑦ー⑧ー⑨ー', '⑩ー⑪ー⑫ー']]
74 ['口⑪⑫口①②③④⑨⑧⑦⑥⑤⑬口⑩', ['①②③④', '⑤ー⑥⑦', '⑧⑨⑩ー', '⑪⑫ー⑬']]
75 ['口口口⑦⑥口口口口⑤④口②口①③', ['①ーーー', '②ーーー', '③④⑤⑥', '⑦ーーー']]
76 ['①口口口⑨②③⑧⑬⑩⑦④⑤⑥⑪⑫口口⑮⑯口⑭口口口口口口口口口口', ['①②③④', '⑤⑥⑦⑧', '⑨⑩⑪⑫', '⑬⑭⑮⑯']]
77 ['③①口⑬⑥⑦⑧⑨口⑩⑤②④⑫⑪口', ['①②ー③', 'ー④ー⑤', '⑥⑦⑧⑨', '⑩⑪⑫⑬']]
78 ['②③①⑧口口⑨口口⑦⑤口⑥口口④⑩口口口口⑪口口口口口口口口口口', ['①ー②③', 'ー④⑤ー', '⑥⑦ー⑧', '⑨ー⑩⑪']]
79 ['⑪④⑤⑫口⑬⑩③②⑨⑧口⑦⑥①⑭', ['①②③④', '⑤⑥ー⑦', '⑧⑨⑩⑪', 'ー⑫⑬⑭']]
80 ['⑪①④⑫⑤⑮⑭⑧⑬⑨⑩②⑦③⑥⑯口⑰⑳口口口口口口口口⑱口⑲口口', ['①②③④', '⑤⑥⑦⑧', '⑨⑩⑪⑫', '⑬⑭⑮⑯⑰⑱⑲⑳']]
81 ['口口口口①口口口口口口口口口口口', ['①ーーー', 'ーーーー', 'ーーーー', 'ーーーー']]
elapsed_time:0.004356861114501953[sec]
```
