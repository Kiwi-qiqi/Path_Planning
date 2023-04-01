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
此时点击button 1，即开始寻找路径，且开始寻径过程的节点拓展可视化过程
此时需要将 start_search, gridmap_dynamic = true

button1上的文字会变成Restart Search，button2上的文字变成Pause Search
在寻径或者动态可视化过程中或完成后，如果点击了Restart search
将根据当前选中的算法进行 重新寻找路径并展示动态可视化过程

无论时Start Search还是Restart search使路径搜索开始
在寻径或者动态可视化过程中或完成后，如果点击了Pause Search，
则暂定当前可视化的过程，且将Button 1 文字修改为Resume Search

点击Resume Search将会继续刚刚暂停的可视化过程

因此Button 1 有三种状态
1. 初始化时，当起点or终点位置发生变化or地图信息信息更新时，为Start Search
2. 当搜索开始后的搜索过程可视化，未点击button2 暂停时，或者搜索结束后，只要上述所说起点、终点与障碍物为变化，则为Restart 
3. 当搜索开始后，可视化进行过程中，点击button 2 的Pause Search，此时为Resume Search

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