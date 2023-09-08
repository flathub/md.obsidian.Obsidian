#!/bin/sh

set -oue pipefail

EXTRA_ARGS=()

add_argument() {
    declare -i "$1"=${!1:-0}

    if [[ "${!1}" -eq 1 ]]; then
        EXTRA_ARGS+=(${@:2})
    fi
}

# Nvidia GPUs may need to disable GPU acceleration:
# flatpak override --user --env=OBSIDIAN_DISABLE_GPU=1 md.obsidian.Obsidian
add_argument OBSIDIAN_DISABLE_GPU         --disable-gpu
add_argument OBSIDIAN_DISABLE_GPU_SANDBOX --disable-gpu-sandbox

# Wayland support can be optionally enabled like so:
# flatpak override --user --env=OBSIDIAN_USE_WAYLAND=1 md.obsidian.Obsidian
if [[ "${XDG_SESSION_TYPE:-''}" == "wayland" ]] || [[ "${WAYLAND_DISPLAY:-''}" =~ wayland-* ]]; then
    add_argument OBSIDIAN_USE_WAYLAND     --ozone-platform=wayland \
                                          --ozone-platform-hint=auto \
	                                  --enable-features=UseOzonePlatform,WaylandWindowDecorations
fi

add_argument OBSIDIAN_ENABLE_AUTOSCROLL   --enable-blink-features=MiddleClickAutoscroll

echo "Debug: Will run Obsidian with the following arguments: ${EXTRA_ARGS[@]}"
echo "Debug: Additionally, user gave: $@"

export FLATPAK_ID="${FLATPAK_ID:-md.obsidian.Obsidian}"
export TMPDIR="${XDG_RUNTIME_DIR}/app/${FLATPAK_ID}"

# Discord RPC
for i in {0..9}; do
    test -S "$XDG_RUNTIME_DIR"/"discord-ipc-$i" || ln -sf {app/com.discordapp.Discord,"$XDG_RUNTIME_DIR"}/"discord-ipc-$i";
done

zypak-wrapper /app/obsidian $@ ${EXTRA_ARGS[@]}
