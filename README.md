# 自用脚本 / My Helper Scripts

**\[ Under contruction / 在建 \]**

代码本自用，使用须谨慎；盲目运行，系统炸了，后果自负！<img src="https://bryango.github.io/assets/coolemoji/tieba_emotion_89.png" width="24px"/><br/>
This repo consists of scripts that I write to make my life easier.

**Disclaimer:** I'm NOT a qualified programmer; rather, I'm a physics student who loves Linux & tinkering. Please check the code before you actually use it on your system. No compatibility is guaranteed.

### 测试环境 / Environments

- 系统 / OS: `Manjaro Linux v18.0.1 Illyria x86_64` - 基于 Arch, 使用 `pacman`
- 桌面 / Desktop: `GNOME v3.30.2`

  - **注意：** 本 repo 中的大量代码是针对 GNOME 编写的，为绕过其若干脑残的设计；这些脚本对非 GNOME 桌面而言可能意义不大。<br/>
    **Note:** Most scripts in this repo are tailored to GNOME, to circumvent many of its unreasonable design. These scripts might not be meaningful for other DEs.

### 说明 / Note

- 此 repo 对应本人的 `$HOME`, 为安全起见，建议：

  - `git clone` 到某个非 `$HOME` 的地方；<br/>
    / clone to somewhere other than `$HOME`;
  - 把需要的脚本逐渐移到（或链接到） `$HOME`; <br/>
    / move or link the wanted scripts to corresponding paths under `$HOME`;
  - 在 `$HOME` 下面先自建一个 git 仓库（注意配置好 `.gitignore`）然后再按需合并，**这是坠吼的！**<br/>
    / **Recommended:** `git merge` to your own `$HOME` repo.

## 内容 / Contents

   * [`~/bin/`](#bin)
   * [`~/.shrc`](#shrc)
   * [`~/.config/argos/`](#configargos)

_TOC Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)_

### `~/bin/`

各种脚本，该目录加入 `$PATH`, 方便调用 / All kinds of fun scripts

👉 详见 `~/docs/README-bin.md`

### `~/.shrc`

Bash 和 Zsh 共用的 `rc` 文件 / `rc` file shared between bash & zsh, sourced by `.bashrc` & `.zshrc`

### `~/.config/argos/`

Argos 脚本，在 GNOME 状态栏上显示各种有趣的东西 / Argos scripts for GNOME

**依赖 / Dependencies:**

- GNOME 桌面
  - Argos 插件：[p-e-w/argos](https://github.com/p-e-w/argos), 了不起的好东西！

👉 详见 `~/.config/argos/README.md`

<br/>

> _发布策略：`git merge --squash --no-commit --allow-unrelated-histories HOME`_
