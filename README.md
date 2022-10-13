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
