Obsidian flatpak
----------------

This distribution is not officially supported by the Obsidian team.

## Installation

First [add](https://flatpak.org/setup) Flathub repository. Then run:

```
$ flatpak install md.obsidian.Obsidian
```

## Wayland support

Wayland support can be enabled by setting the environment variable `OBSIDIAN_USE_WAYLAND=1` either using [Flatseal](https://flathub.org/apps/details/com.github.tchx84.Flatseal), or the command line, like so:

```
$ flatpak override --user --env=OBSIDIAN_USE_WAYLAND=1 md.obsidian.Obsidian
```

Wayland support can also be temporarily enabled for a single run:

```
$ flatpak run --env=OBSIDIAN_USE_WAYLAND=1 md.obsidian.Obsidian
```

## GPU acceleration

GPU acceleration may need to be disabled to avoid launching with a black window when using Nvidia GPUs:

```
$ flatpak override --user --env=OBSIDIAN_DISABLE_GPU=1 md.obsidian.Obsidian
```

Disabling the GPU sandbox may also be necessary:

```
$ flatpak override --user --env=OBSIDIAN_DISABLE_GPU_SANDBOX=1 md.obsidian.Obsidian
```

## Pandoc support

The pandoc plugin partially works with the bundled `pandoc` binary; however, it requires an extension to utilize `pdflatex`:

```
$ flatpak install flathub org.freedesktop.Sdk.Extension.texlive//22.08
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
    --env="OBSIDIAN_USE_WAYLAND=1" \
    --unshare=ipc \
    --nosocket=x11 \
    md.obsidian.Obsidian
```
