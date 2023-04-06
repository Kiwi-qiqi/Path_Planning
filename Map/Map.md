# Map架构
Map架构依次为
    Screen-->Panel-->Button-->GridMap-->Path

## Screen
Screen初始化设置为1000*800
Screen大小可修改，最大为屏幕尺寸，最小为500*400
Screen标题可以自定义，默认为Path_Finding

## Panel
Panel设置为恒定大小300*100
当Screen大小变化时，Panel会初始化到当前屏幕的中下方
Panel可通过鼠标拖动停靠到Screen内任意区域

## Button
Button在Panel上横向均匀布置了三个，尺寸统一为80*50
点击三个button可以分别执行不同的程序
button上均有对应文字，文字会随着点击button后出现变化，
下一次出现不同的文字，对应其他功能

### Button 1
初始化时，Button 1为Start Search，
此时点击button 1，即开始寻找路径，在算法求解出路径后
开始寻径过程的节点拓展可视化过程
此时需要将 start_search, dynamic_visualize = true

button1上的文字会变成Restart Search，button2上的文字变成Pause Search
在寻径或者动态可视化过程中或完成后，如果点击了Restart search
将根据当前选中的算法进行 重新寻找路径并展示动态可视化过程

无论是Start Search还是Restart search使路径搜索开始
在寻径或者动态可视化过程中，如果点击了Pause Search，
则暂定当前可视化的过程，且将Button 1 文字修改为Resume Search
点击Resume Search将会继续刚刚暂停的可视化过程

当搜索结束后，button 1保持Restart search，
如果起点或终点、地图出现变化，则将button1 改为start search

因此Button 1 有三种状态
1. 初始化时，当起点or终点位置发生变化or地图信息信息更新or可视化过程结束时，为Start Search
2. 当搜索开始后的搜索过程可视化，未点击 button2 暂停时，
    或者搜索结束后，只要上述所说起点、终点与障碍物未变化，则为Restart 
3. 当搜索开始后，可视化进行过程中，点击button 2 的Pause Search，此时为Resume Search

### Button 2
初始化时，button 2 为Pause Search，但此时点击Pause并无反应,可将初始化的Pause Search设置为灰色
当点击Start Search后，Button 2的Pause Search生效，此时点击将会暂停可视化的过程

当暂停可视化时，Pause Search -> Cancel Search，此时点击将会清除屏幕上已有的路径以及拓展单元格
并将Button 2重置为灰色的Pause Search

当可视化过程结束后，Pause Search -> Clear Path，此时点击会将屏幕上拓展完的网格以及路径清除
并将Button 2重置为灰色的Pause Search

因此Button 2 有三种状态
1. 初始时，为灰色的Pause Search，此时点击没有效果。可视化开始时，点击Pause Search可暂停
2. 可视化暂停时，Pause Search变为Cancel Search，实现清屏
3. 当可视化完成后，Pause Search变为Clear Path， 实现清屏

### Button 3
初始化时，Button 3为Init Walls，
此时点击button 3，开始生成随机障碍物，由于生成障碍物的过程很快
因此在障碍物生成完后，将Button 3文字改为Clear Walls，

如果通过鼠标选中单元格作为障碍物，此时也需要将Button 3改为Clear Walls

点击Clear Walls，会清除当前界面所有的障碍物网格
并将Button 3文字改为 Init Walls

因此Button 3 有两种状态
1. 初始化时，或当前界面无障碍物时，为 Init Walls
2. 只要当前界面存在障碍物，就为 Clear Walls