# Argos 脚本

Argos 脚本，在 GNOME 状态栏上显示各种有趣的东西 / Argos scripts for GNOME

**依赖 / Dependencies:**

- GNOME 桌面
  - Argos 插件：[p-e-w/argos](https://github.com/p-e-w/argos), 了不起的好东西！

👉 内含脚本如下：

## `./Z29-aqi.1000c.30m+.sh` & `./aqi/`

从 [aqicn.org](https://aqicn.org) 和 [pm25.in](http://www.pm25.in/) （爬取，备用）获取空气质量指数，并显示在状态栏上 / get Air Quality Index (AQI):

&emsp;&emsp;<img src="/.screenshots/aqi.png" width="360px"/>

**依赖 / Dependencies:**

- **文件 / Files:** `~/.shrc`, 获取正确的 python 路径与 token;
- **变量 / Const:** `TOKEN_AQICN`, 用于访问 aqicn 的 API
  - 请自行前往 [aqicn.org/api](http://aqicn.org/api/) 申请，否则将 fallback 到 `token = demo` , 功能受限；
  - 获得 token 后，将其以 `TOKEN_AQICN='insert_token_here'` 形式保存到 `~/.tokens` 或直接保存到 `~/.shrc`.
- **包 / Packages:** `python 3.7` 的 `requests[socks], pandas, beautifulsoup4` 模块，建议使用 Anaconda, 或用以下命令安装：

  ```
  pip install --user requests[socks] pandas beautifulsoup4
  ```

**使用方法 / Usage:**

```
cd ~/.config/argos; chmod +x z_aqi.1000c.30m+.sh
cd aqi; chmod +x widget.py
```

## `./030-eject.0r.1d+.sh`

分区信息及硬盘断电功能<br/>
/ Disks info & power-off option<br/>

方便地在状态栏启动 `lsblk-more` 与 `udisksctl-off` （见 `~/bin`）<br/>
/ Just an easy access to disk utils in `~/bin`

**依赖 / Dependencies:**

- `~/bin/lsblk-more`: 展示硬盘及分区信息 / Show disks info
- `~/bin/udisksctl-off`: 硬盘断电命令 / Power off drives
