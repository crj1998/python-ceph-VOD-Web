> 以下内容均在华为云ECS Centos7.4上测试。

### 修改主机名，后面使用到的节点名称就是对应的主机名称
```
# 把主机名称修改为ceph1
hostnamectl  set-hostname ceph1
```
### 关闭selinux和firewall
```
setenforce 0
sed -i  "s/SELINUX=enforcing/SELINUX=permissive/g" /etc/selinux/config
systemctl disable firewalld.service
systemctl stop firewalld.service
```

### 修改hosts文件
首先使用`$ ip addr`查看主机的内网IP地址，结果如下图示，主机内网IP地址为`192.168.0.119/24`，此IP地址非常重要，之后频繁使用。
![查看内网IP.png](https://upload-images.jianshu.io/upload_images/13843118-b65918c18c8bf6c9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
然后将IP地址和主机名称写入hosts文件
```
# 192.168.0.119 为内网IP，ceph1为节点名称
echo "192.168.0.119 ceph1" >> /etc/hosts
```

### 安装ceph-deploy
首先配置 ceph 源，可以自己编写，也可使用如下阿里云提供的源：
```
wget -O /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo

cat <<END >/etc/yum.repos.d/ceph.repo
[norch]
name=norch
baseurl=https://mirrors.aliyun.com/ceph/rpm-nautilus/el7/noarch/
enabled=1
gpgcheck=0

[x86_64]
name=x86_64
baseurl=https://mirrors.aliyun.com/ceph/rpm-nautilus/el7/x86_64/
enabled=1
gpgcheck=0
END

```

配置源后，开始安装
```
yum -y install  ceph-deploy  && yum -y install ceph ceph-radosgw python-setuptools python2-subprocess32
```

### 运行Ceph
创建配置文件目录，后续命令都是在该目录下执行
```
mkdir ~/ceph
cd ~/ceph
```
初始化ceph集群
```
ceph-deploy new ceph1
```
![ceph deploy new](https://upload-images.jianshu.io/upload_images/13843118-777adf90e04e764a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
修改ceph.conf配置文件为单节点：
```
echo "osd pool default min_size = 1" >>ceph.conf
echo "osd pool default size = 1" >>ceph.conf
echo "public_network =192.168.0.119/24" >>ceph.conf
```

初始化ceph的监控，启动mon 进程。目录下会新生成ceph.client.admin.keyring 等5个配置文件
```
ceph-deploy mon create-initial
```
![ceph deploy mon](https://upload-images.jianshu.io/upload_images/13843118-ebcbf52ea0f9caf4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

将ceph.client.admin.keyring拷贝到各个节点上
```
ceph-deploy admin ceph1
```
![ceph deploy admin](https://upload-images.jianshu.io/upload_images/13843118-ee1329df08f1397d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

启动mgr进程
```
ceph-deploy mgr create ceph1
```
![ceph deploy mgr create](https://upload-images.jianshu.io/upload_images/13843118-ddc039452ace42d3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

`$ ceph -s` 查看集群状态，如图所示，`HEALTH_OK`, `HEALTH_WARN`都表明ceph集群安装成功可以使用了
![ceph s](https://upload-images.jianshu.io/upload_images/13843118-a8a2ceda8c5fa9a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 准备数据盘
```
fdisk -l
```
![fdisk -l](https://upload-images.jianshu.io/upload_images/13843118-35e7152f837441bd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
上图表明主机已经有一块系统盘`/dev/vda`还有一块`/dev/vdb`未分区
我们对`/dev/vdb`进行分区并作为数据盘使用。

```
fdisk  /dev/vdb
```
在键盘上依次输入
```
# 添加一个分区
n
# 主分区
P
# 第一个回车指是开始的磁盘扇区大小
ENTER
# 第二个回车指是结束的磁盘扇区大小
ENTER
# 写入磁盘
w
```
此时数据盘被分好了。
![fdisk -l](https://upload-images.jianshu.io/upload_images/13843118-9e10c1f694b80b71.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

格式化磁盘
```
mkfs.ext4 /dev/vdb
```
![mkfs4](https://upload-images.jianshu.io/upload_images/13843118-9e3c95f7f098f801.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

创建osd
```
ceph-deploy osd create --data  /dev/vdb ceph1
```

### 启动rgw
启动rgw对象存储进程
```bash
ceph-deploy rgw create ceph1
```

输入以下命令，查看集rgw是否正常启动。RGW服务默认启动的7480端口
```bash
curl 192.168.0.119:7480
curl 公网IP:7480
```
出现如下结果表示RGW进程正常启动
![rgw](https://upload-images.jianshu.io/upload_images/13843118-156ea4589127437e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

设置pool 和 pgs的值：

```bash
ceph osd pool set .rgw.root pg_num 64
ceph osd pool set .rgw.root pgp_num 64
```
利用s3创建 桶来测试，先输入以下命令，创建用户，并赋予读写权限  ：
```bash
radosgw-admin user create --uid="admin" --display-name="administrator"
radosgw-admin caps add --uid="admin" --caps="users=read, write; usage=read,write; buckets=read,write"
```
查看用户信息，记录access_key和secret_access_key的值
```
radosgw-admin user info --uid="admin"
```

![key](https://upload-images.jianshu.io/upload_images/13843118-defaca417acb5f00.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

输入以下命令，利用python脚本来验证 桶是否创建成功：
```
yum install python-boto -y
vi s3.py

import boto
import boto.s3.connection
host =  '192.168.0.119'
access_key = ''
secret_key = ''
conn = boto.connect_s3(
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_key,
    host =host, port=7480,
    is_secure=False,
    calling_format = boto.s3.connection.OrdinaryCallingFormat()
)
bucket = conn.create_bucket('py-first')
for bucket in conn.get_all_buckets():
    print "{name}\t{created}".format(name = bucket.name, created = bucket.creation_date)

```
![test](https://upload-images.jianshu.io/upload_images/13843118-0ad878f94a99e738.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
出现上述内容说明ceph部署成功。之后可以使用python操作ceph。推荐boto3。


----
[Reference]：
[Centos--单节点Ceph对象存储部署](https://blog.csdn.net/qq_33553493/article/details/103851749)
[单节点Ceph对象存储简单部署(1)](https://blog.csdn.net/weixin_42562106/article/details/109660009)
[Centos挂载硬盘完整图文教程（查看、分区、格式化、挂载）磁盘](https://www.fujieace.com/linux/centos-mount.html)