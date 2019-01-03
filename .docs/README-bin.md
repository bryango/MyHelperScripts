# `~/bin`

各种脚本，该目录加入 `$PATH`, 方便调用 / All kinds of fun scripts

👉 内含脚本如下：

## `./lsblk-more`

显示挂载分区的详细信息，只不过是 `lsblk` 命令调整了一下显示项 / `lsblk` with relevant options<br/>
独立为脚本，以方便 `./udisksctl-off` 与 `~/.config/argos/aeject.0r.1d+.sh` 调用

## `./udisksctl-off`

拔出移动硬盘前使之停转 / Spin down hard drive before unplug

**依赖 / Dependencies:**

- `~/bin/lsblk-more`: 展示硬盘及分区信息 / Show disks info
- 可选 / Optional: `xdotool`, 最大化当前命令窗口以完整显示列表 / Maximize current terminal emulator

