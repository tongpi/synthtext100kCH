## 说明

> 本程序根据[SynthText项目](https://github.com/ankush-me/SynthText)，分别生成数据集对应的模型，用于最终的自然场景图片文本数据合成。

## 用法

### 1 深度和分割文件生成

> 参考SynthText项目中data目录下面的程序运行后下载的数据文件中dset.h5文件,
使用generate\_h5.py将输入图片对应的深度数据depth.h5、切割数据seg\_uint16.h5、
以及原始图片对应数据image.h5（使用generate\_h5.py可以生成原始图片对应image.h5）合成为最终的dset.h5文件。

### 2 newsgroup数据文件和模型文件生成

> 使用readData.py可以将中文数据处理成类似SynthText项目中data目录下面英文数据newsgroup数据文件的格式，
使用char\_frequency.py可以将readData.py处理过的文件进行处理得到最终的char\_freq.cp模型文件。

###  3 颜色模型生成

>使用train_color_model.py可以生成SynthText项目中data目录下面model文件夹中的color_new.cp模型文件，
该程序使用IIIT5K数据集。
