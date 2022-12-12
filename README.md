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

## Flatpak permissions

This flatpak goes into great lengths to provide a nice experience for end users. In order for the [Git plugin](https://github.com/denolehov/obsidian-git) to work it requires permission to the ssh-auth socket (`--socket=ssh-auth`). It also exposes the home directory in the sandbox (required for Drag and Drop operations). If you don't use the Git plugin you can disable the ssh-auth socket permission, e.g. using Flatseal. You can also remove access to the home directory if you want and the flatpak will continue to work, albeit with reduced functionality. In case you do remove access to the homedir, note that in order for things to not break for the Git plugin, `--persist=.ssh` flag has been passed and a bind mount to `~/.var/app/md.obsidian.Obsidian/` is created by flatpak, allowing that location to be used for persistent data (but your home directory's .ssh remains unaccessible)
