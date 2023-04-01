# Button Class

button类较为复杂，除了需要在button上呈现不同的文字描述

还需要在执行对应程序后对button上的文字以及布尔状态进行更新



## 初始化

初始化button，需要在panel上绘制三个button的圆角矩形，且在button的呈现初始时的文字描述

屏幕大小变化时，panel会初始化到屏幕中下位置，此时button的位置也需要相对应地进行更新





## 按钮点击

当点击到panel，而没点击到任意button上时，可以实现拖拽panel

当点击到button上时，panel不可被拖拽



### 点击按钮一

在初始状态时点击按钮一，将开始搜索路径，

