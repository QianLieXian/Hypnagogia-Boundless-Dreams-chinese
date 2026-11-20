# Hypnagogia-Boundless-Dreams-chinese  
<img width="460" height="215" alt="header" src="https://github.com/user-attachments/assets/45a7bd54-aa01-4d53-b3dc-6fabb43e6015" />   

無限の夢 无限之梦汉化补丁  
感谢由lxgw大佬改良的小赖字体:https://github.com/lxgw/kose-font  
解包：https://github.com/Perfare/AssetStudio  
net6：https://builds.dotnet.microsoft.com/dotnet/WindowsDesktop/6.0.36/windowsdesktop-runtime-6.0.36-win-x64.exe  
打包：https://github.com/nesrak1/UABEA/releases  
老钱亲情汉化，有bug或者字体错误请提出，有时间会优化  
  
[下载 v0.3 汉化补丁](https://github.com/QianLieXian/Hypnagogia-Boundless-Dreams-chinese/releases/tag/Chinese-v0.3) · [历史版本](https://github.com/QianLieXian/Hypnagogia-Boundless-Dreams-chinese/releases)

汉化TextAsset文件链接(正常玩家不需要):https://github.com/QianLieXian/Hypnagogia-Boundless-Dreams-chinese/tree/main/TextAsset  


要是出现字体为方框的情况，请尝试安装由lxgw大佬改良的小赖字体  
~我两台电脑互相测试，解决方框的流程为安装net6和小赖字体，使用UABEA扫一遍字体就解决了，不过我感觉应该是占用问题，重启游戏解决的😋~    
~(确保自动保存后，重启游戏即可解决方框的问题，似乎每次进入新游戏，载入新地图时字体不会自动跟过来，重启解决！)~   
~~燃尽了，基本可以确定是缓存原因，游戏先载入的字符，1帧后再挂载的字体，导致的会有方框，目前只能重启游戏解决~~

**完美解决**（修复已随 v0.3 发布，切图效果待游戏内验证）

v0.2 的补丁已经内嵌小赖字体。检查发布包时发现，动态字形图集只能使用一页，部分图集也无法让 TextMeshPro 在运行时写入新字形。v0.3 开放多页图集、启用相关纹理的读写，并把内嵌的小赖字体设为全局后备字体。鬼屋和商场对白中两个使用缺失字形的特效段也已改写。太空关卡的特效角色名保留，原有装饰字符依然可能显示为方框。

#### 从 v0.2 重建 v0.3 资源包

从历史版本下载并解压 v0.2 补丁，在仓库根目录用 Python 3.12 执行以下命令。脚本读取原包的 `data.unity3d` 和当前仓库的 `TextAsset/`，生成一个新的游戏资源包。

```bash
python -m pip install UnityPy==1.25.4
python tools/rebuild_v02.py "Hypnagogia Boundless Dreams_Data/data.unity3d" "data.fixed.unity3d"
```

测试时先备份游戏的 `*_Data/data.unity3d`，正常应用 v0.2 补丁，再用生成的文件替换补丁里的同名资源包。冷启动读档后，连续切换地图并检查对白、角色名和选项是否出现方框。
