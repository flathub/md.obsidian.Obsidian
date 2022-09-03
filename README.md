# Obsidian flatpak

This distribution is currently in beta and not officially supported by the Obsidian team.

## Installation

First [add](https://flatpak.org/setup) Flathub repository. Then run:

```
$ flatpak install md.obsidian.Obsidian
```

## Wayland support

Obsidian can now start under Wayland, which can be enabled with `OBSIDIAN_USE_WAYLAND=1` in [Flatseal](https://flathub.org/apps/details/com.github.tchx84.Flatseal). It can also be enabled on the command line, like so:

```
$ flatpak override --user --env=OBSIDIAN_USE_WAYLAND=1 md.obsidian.Obsidian
```

## Pandoc support

The pandoc plugin partially works with the bundled `pandoc` binary; however, it currently requires an additional SDK in order to utilize `pdflatex`:

```
$ flatpak install flathub org.freedesktop.Sdk.Extension.texlive//21.08
```

## Obsidian Git plugin support for Github login

This flatpak bundles the `gh` binary (the github cli), so use that to login from your distro's command line:

```
$ flatpak run --command=gh md.obsidian.Obsidian auth login
```
```
$ flatpak run --command=gh md.obsidian.Obsidian auth setup-git
```


