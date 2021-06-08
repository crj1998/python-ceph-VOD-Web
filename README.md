# Big Data Processing
## Project 3: Object-based Storage System
> Establish a Video-on-Demand (VoD) web site based on an open source object-based file system (i.e., Ceph file system).



大规模数据处理技术课程作业3：基于对象文件系统Ceph的视频点播网站。

硬件：用Machine Learning课程代金券撸来的华为云ECS（1核，2G，3M带宽）

前端：HTML, JavaScript, CSS

后端：Python Flask



[Ceph单节点配置过程](ceph.md )



文件目录

crawler.sh    从守望先锋官网下载游戏动画视频及封面

s3.py    使用python boto3 s3 API将下载的视频存入Ceph中

server.py    Flask web 服务器文件。statics 和templates为使用到的前端文件。





## 网站界面

![登陆界面——配置KEY](https://upload-images.jianshu.io/upload_images/13843118-2382749ae63d1616.PNG)

![视频列表界面1](https://upload-images.jianshu.io/upload_images/13843118-070c612432bc6fcf.PNG)

![视频列表界面2](https://upload-images.jianshu.io/upload_images/13843118-5c0bb4c6cf8e0328.PNG)

![播放器](https://upload-images.jianshu.io/upload_images/13843118-a6911034e0a3b7cf.PNG)





