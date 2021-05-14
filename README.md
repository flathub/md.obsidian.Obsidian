# Obsidian flatpak

This distribution is currently in beta and not officially supported by the Obsidian team.

## Installation

First [add](https://flatpak.org/setup) Flathub repository. Then run:

```
flatpak install md.obsidian.Obsidian
```

## Wayland support

Obsidian can now start under Wayland, which can be enabled with `OBSIDIAN_USE_WAYLAND=1` in [Flatseal](https://flathub.org/apps/details/com.github.tchx84.Flatseal). It can also be enabled on the command line, like so:

```
flatpak override --user --env=OBSIDIAN_USE_WAYLAND=1 md.obsidian.Obsidian
```
