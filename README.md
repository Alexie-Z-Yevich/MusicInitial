# MuT@b

该项目名称为MuT@b，如果不出意外的话应该是鄙人的毕设了吧。暂时没太多时间写，想到一点就写一点，当前仅记录目录结构

```
MusicInitial
  │  main.py                    ：主函数，目前启动不起来
  │  test.py
  │  test2.py
  │
  ├─function  ：主要方法拆分
  │  │  matching_cut.py         ：main的不同实现方式，完善比较之后该文件会替换主类，可以运行
  │  │  prediction_beat.py      ：节拍预测（未实现）
  │  └─ similarCompare.py       ：matching_cut中的MFCC比较方法，使用facebook/wav2vec2-base-960h模型
  │
  ├─music                       ：wav资源库，下存wav音乐资源（唯一一个mp3请忽略后期调整）
  │  │  爱的奉献.mp3
  │  │  爱的奉献.wav
  │  ├─1Point
  │  ├─2Point
  │  ├─3Point
  │  ├─4Point
  │  └─chord
  │
  ├─sound                      ：和弦库/mp3资源库，当前存储的是和弦的mp3资源，与./music/chord资源对应
  │
  └─tools                      ：工具集合
  	│   generation_chord.py    ：和弦生成器（瑕疵），生成和弦的机器音，用于之后生成wav文件
  	│   generation_sound.py    ：单音生成器，生成单个机器音，用于之后生成wav文件
  	│   mp3_to_wav.py          ：使用ffmpeg实现mp3文件转wav
    │   mp3_to_wav_chord.py    ：使用ffmpeg实现mp3文件批量转wav（./sound -> ./music/chord）	
    │   read_mp3.py            ：读取mp3文件并播放
    └─  read_wav.py            ：读取wav文件并播放
```

