+++
title: Audio on Linux / Arch / KDE / Wayland
published: 2025-09-23
description: Some notes on audio on KDE / Linux with Arch and Wayland.
image: https://images.unsplash.com/photo-1637929476734-bd7f5f78e40a
+++

Some quick notes.

# ALSA & Device Inspection

pactl list sources short
    Lists audio sources PipeWire/PulseAudio sees.

arecord -l
    Lists available capture hardware devices at the ALSA level.

aplay -l
    Lists available playback hardware devices at the ALSA level.

arecord -D hw:X,Y -f cd -d 5 test.wav
    Records 5 seconds directly from a specific ALSA device to test the mic.

aplay test.wav
    Plays back the test recording.

# Volume & Input Control
alsamixer -c N
    Opens ALSA mixer for a specific card to unmute/raise “Mic,” “Front Mic,” “Capture,” and “Mic Boost” sliders.

(Spacebar in alsamixer Capture view)
    Selects the correct capture source (Front Mic vs. Rear Mic).

# Service & Config Resets
systemctl --user restart pipewire pipewire-pulse wireplumber
    Restarts PipeWire and its PulseAudio compatibility layer to refresh routing.

rm -rf ~/.config/pulse ~/.config/pipewire ~/.local/state/wireplumber
    Deletes per-user configuration to reset audio settings.

sudo pacman -Syu alsa-utils pipewire pipewire-pulse wireplumber
    Reinstalls and updates the audio stack packages.

# Kernel Module Tweaks
sudo nano /etc/modprobe.d/alsa-base.conf
    Removes or adds snd-hda-intel model overrides to reset driver pin mappings.

