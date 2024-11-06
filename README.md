Obsidian flatpak
----------------

This distribution is verified by the Obsidian team but isn't supported.

## Installation

First [add](https://flatpak.org/setup) Flathub repository. Then run:

```
$ flatpak install md.obsidian.Obsidian
```

## Wayland support

Obsidian has a fairly complete Wayland backend which brings about several improvements over X11, including:

* fractional scaling
* multi-touch gestures such as pinch-zoom
 
Wayland support can be enabled by setting the environment variable `--socket=wayland` either using [Flatseal](https://flathub.org/apps/details/com.github.tchx84.Flatseal), or the command line, like so:

```
$ flatpak override --user --socket=wayland md.obsidian.Obsidian
```

Wayland support can also be temporarily enabled for a single run:

```
$ flatpak run --socket=wayland md.obsidian.Obsidian
```

### Broken functionality on Wayland

There are some features that don't yet work in Obsidian when running as a native Wayland client:

1. Input method frameworks
    * IBus with GNOME: **[does not work](https://github.com/flathub/md.obsidian.Obsidian/issues/317)**.
    * IBus with KDE Plasma: **[does not work as candidate window is misplaced](https://discuss.kde.org/t/ibus-candidate-window-is-misplaced-for-some-apps/3579)**.
    * Fcitx5 with GNOME: **does not work**.
    * Fcitx5 with KDE Plasma: **[works now if configured correctly](https://fcitx-im.org/wiki/Using_Fcitx_5_on_Wayland#KDE%20Plasma)**.

2. [Pen tablet support](https://github.com/flathub/md.obsidian.Obsidian/issues/345)

There don't appear to ways to work around these issues, and until they're resolved the Obsidian flatpak will use XWayland by default.

## GPU acceleration

GPU acceleration may need to be disabled to avoid launching with graphical bugs:

```
$ flatpak override --user --env=OBSIDIAN_DISABLE_GPU=1 md.obsidian.Obsidian
```


## Pandoc support

The pandoc plugin partially works with the bundled `pandoc` binary; however, it requires an extension to utilize `pdflatex`:

```
$ flatpak install flathub org.freedesktop.Sdk.Extension.texlive//24.08
```

## Obsidian Git plugin support for Github login

This flatpak bundles the `gh` binary (the github cli), so use that to login from your distro's command line:

```
$ flatpak run --command=gh md.obsidian.Obsidian auth login
```

A git repo can also be set up by running the following:

```
$ flatpak run --command=gh md.obsidian.Obsidian auth setup-git
```

The `gh` binary can resolve to `/app/bin/gh` in `~/.gitconfig` after running `gh auth setup-git` in flatpak, [which may be problematic if `gh` is needed outside of flatpak](https://github.com/cli/cli/issues/7420). This can be worked around like so:

```
$ sed -i 's@/app/bin/@@g' ~/.gitconfig
```

## Middle-click auto-scrolling

Middle-click auto-scrolling can be enabled with the following:

```
$ flatpak override --user --env=OBSIDIAN_ENABLE_AUTOSCROLL=1 md.obsidian.Obsidian
```

## Flatpak permissions

This flatpak goes into great lengths to provide a nice experience for end users. In order for the [Git plugin](https://github.com/denolehov/obsidian-git) to work it requires permission to the ssh-auth socket (`--socket=ssh-auth`). It also exposes the home directory in the sandbox (required for Drag and Drop operations). If you don't use the Git plugin you can disable the ssh-auth socket permission, e.g. using Flatseal. You can also remove access to the home directory if you want and the flatpak will continue to work, albeit with reduced functionality. In case you do remove access to the homedir, note that in order for things to not break for the Git plugin, `--persist=.ssh` flag has been passed and a bind mount to `~/.var/app/md.obsidian.Obsidian/` is created by flatpak, allowing that location to be used for persistent data (but your home directory's .ssh remains unaccessible)

### Filesystem access

Obsidian can use [XDG desktop portals](https://docs.flatpak.org/en/latest/desktop-integration.html#portals) to open vaults. If plugins aren't needed, then widespread host filesystem access can be revoked:

```
$ flatpak override --user \
    --nofilesystem=home \
    --nofilesystem=/run/media \
    --nofilesystem=/mnt \
    --nofilesystem=/media \
    --nofilesystem=xdg-run/app/com.discordapp.Discord \
    md.obsidian.Obsidian
```

### Network access

The Obsidian flatpak doesn't need OTA updates to stay up-to-date. If plugins aren't being used or are already installed, then network access can be disabled:

```
$ flatpak override --user --unshare=network md.obsidian.Obsidian
```

### SSH authentication

SSH support is commonly used with the Git plugin. If SSH support isn't needed, then it can be disabled:

```
$ flatpak override --user --nosocket=ssh-auth md.obsidian.Obsidian
```

### Pulseaudio access

Sometimes Pulseaudio access is needed, although it can be disabled under most circumstances:

```
$ flatpak override --user --nosocket=pulseaudio md.obsidian.Obsidian
```

### IPC namespace sharing

IPC namespace sharing is required for using the X11 shared memory extension so applications can perform well under X11, however it can be disabled without a performance penalty by using Obsidian's Wayland backend:

```
$ flatpak \
    override \
    --user \
    --socket=wayland \
    --unshare=ipc \
    --nosocket=x11 \
    md.obsidian.Obsidian
```
