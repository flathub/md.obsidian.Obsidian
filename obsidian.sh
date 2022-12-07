#!/bin/sh

set -oue pipefail

export FLATPAK_ID="${FLATPAK_ID:-md.obsidian.Obsidian}"
export TMPDIR="${XDG_RUNTIME_DIR}/app/${FLATPAK_ID}"

# Wayland support can be optionally enabled like so:
# flatpak override --user --env=OBSIDIAN_USE_WAYLAND=1 md.obsidian.Obsidian
declare -i OBSIDIAN_USE_WAYLAND="${OBSIDIAN_USE_WAYLAND:-0}"
declare -i EXIT_CODE=0

# Discord RPC
for i in {0..9}; do
    test -S "$XDG_RUNTIME_DIR"/"discord-ipc-$i" || ln -sf {app/com.discordapp.Discord,"$XDG_RUNTIME_DIR"}/"discord-ipc-$i";
done

if [[ "${OBSIDIAN_USE_WAYLAND}" -eq 1 && "${XDG_SESSION_TYPE}" == "wayland" ]]; then
    zypak-wrapper /app/obsidian --enable-features=UseOzonePlatform,WaylandWindowDecorations --ozone-platform=wayland $@ || EXIT_CODE=$?
    # Fall back to x11 if Obsidian failed to launch under Wayland. Otherwise, exit normally
    [[ "${EXIT_CODE}" -ne 133 ]] && exit "${EXIT_CODE}"
fi

zypak-wrapper /app/obsidian $@
