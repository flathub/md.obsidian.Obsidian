#!/bin/sh

# This wrapper requires the following permission:
# --talk-name=org.freedesktop.Flatpak

set -oue pipefail

APP="$(basename $0)"

if [[ "$(basename "$(realpath $0)")" == "${APP}" ]]; then
    echo "Error: Must be called from a symlink. Exiting."
    exit 1
fi

flatpak-spawn --host /var/lib/flatpak/exports/bin/${APP} $@
