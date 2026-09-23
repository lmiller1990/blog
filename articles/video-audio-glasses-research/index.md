+++
title: Video/Audio Glasses Research
published: 2026-09-23
description: Research notes on video and audio glasses
+++

I have Meta Rayban. Hardware and product is great, but I no longer what to be tied to Meta, accounts, cloud, smartphone apps - I just want to record some videos with audio to a device and (somehow) get the data onto my phone / computer. The Meta Raybans are a bit **too** smart for me - I don't need AI, translations, LLMs... just to be able to take photos and record videos of my adventures.

After plenty of research, I found that the combination from Meta Rayban of microphone/video/speakers is not too common. Specifically, if we drop the speakers requirement, a bunch of other glasses become viable options. One of the main use cases Meta presents is AI translation and using the glasses as a smart assistant - which required speakers.

After some basic research, I sent ChatGPT off to pull some data together. I have not verified *all* of this (yet), but here is a shortlist of video/audio glasses that I'm looking at.

| Model | Camera / video | Stabilisation | Audio recording | Speakers / Bluetooth audio | Storage | Battery / recording | Phone/app requirement | Cloud / account dependence | Weight | Weather resistance | Price | Australia | Main strengths / drawbacks |
|---|---|---|---|---|---|---|---|---|---:|---|---:|---|---|
| **[OHO Primex EIS](https://ohosunshine.com/products/primex-eis-camera-glasses)** | [2K 2560×1440 @ 30fps](https://ohosunshine.com/blogs/news/camera-glasses-2k-eis), 1080p30, 720p30; H.265 | **Yes — EIS**, specifically designed for moving POV footage | **Yes**, built-in mic; audio recorded with video | No | **Built-in 64 / 128 / 256 / 512GB** | **~60 min**; can **record while charging** | **None required.** Physical button. USB-C/OTG transfer directly to computer or compatible phone. | **None required** | 60g | Product page says **IPX4**; some OHO material claims higher protection, so I'd rely on IPX4 unless confirmed by OHO. | **US$249** for 64GB | OHO explicitly [ships to Australia](https://ohosunshine.com/pages/shipping-policy); economy international shipping listed as free | Probably the **strongest option for moving POV footage** because it combines local/offline operation with actual EIS. Resolution is lower than Brave/Edge Pro. |
| **[iVUE Denali](https://ivuecamera.com/products/denali-camera-glasses)** | **2K 2560×1440 @ 30fps**, **1080p @ 60fps**; **Sony 8MP CMOS**; very wide **135° FOV** | No EIS advertised | **Dual stereo AAC microphones** with noise cancelling | No | **Removable microSD up to 128GB**; ~22h of 2K footage on 128GB | **~90 min** internal; **unlimited while connected to USB-C power bank** | **Completely optional.** One-button standalone recording. Optional direct-Wi-Fi app provides preview, settings, remote recording and downloads. | **None.** iVUE explicitly says the direct phone connection requires **no internet** and the glasses **work without the app**. | **52g** | Everyday outdoor use; manufacturer says **not waterproof** | **US$159** no card / $179 64GB / $189 128GB | International purchase available; shipping details should be confirmed at checkout | Arguably the **cleanest architecture** here. Sony sensor, removable storage, 60fps, stereo mic, zero mandatory software. **Lack of EIS is the major drawback.** |
| **[OHO Brave 4K](https://ohosunshine.com/products/brave-4k-camera-glasses-polarized)** | **4K @ 30fps**, **24MP stills** | **No EIS advertised** | **Yes**, built-in mic | No | **Built-in 32 / 64 / 256 / 512GB** | **~30 min**, but **record-while-charging** supported | **None required.** Physical button, USB/data transfer, OTG adapter included. | **None required** | **60g** | **IPX4** | **US$149.99** base configuration | OHO [ships directly to Australia](https://ohosunshine.com/pages/shipping-policy) | **Best resolution-per-dollar.** Extremely simple standalone camera. Main concern is that 4K without stabilisation may look worse during movement than Primex's stabilized 2K. |
| **[OHO Edge Pro](https://ohosunshine.com/products/edge-pro-ai-smart-glasses-4k-camera-translation)** | **4K @ 30fps**, claimed **24MP photos** | No EIS advertised | **Yes**, mic records audio with video | **Yes — Bluetooth 5.3 + open-ear speakers**; music, calls and voice assistant | **64 / 128 / 256GB built-in** | Product specification currently says **~0.5h recording**; OHO publishes conflicting runtime figures elsewhere, so assume ~30 min until confirmed | Has **button, voice and app control**. Basic recording is button-controlled; app relates mainly to smart/translation functionality. | AI/translation functionality exists, but isn't fundamental to basic camera/audio operation | **41.5g** | Advertised protection against rain/sweat/splashes; waterproof rating is less clearly documented than Brave | **US$199.99** | OHO [ships directly to Australia](https://ohosunshine.com/pages/shipping-policy) | Potentially the **best all-in-one**: 4K camera + mic + Bluetooth audio + local storage. Main concern is OHO's inconsistent documentation and lack of advertised EIS. |
| **[Solos AirGo V2](https://solosglasses.com/products/prime-2-smartglasses-solos-airgo%E2%84%A2-v2)** | **16MP camera + 2K video** | **Yes**, manufacturer describes camera as stabilized; detailed stabilisation specs are sparse | **Yes** | **Yes — directional open-ear audio + Bluetooth 5.2**; music and calls | Solos does **not clearly publish local video-storage capacity** on the V2 product page | Solos quotes **~16h for photo shooting/AI enquiries**, but doesn't clearly state continuous video-recording runtime | **More app-centric** than OHO/iVUE. Android/iOS supported; ordinary Bluetooth music/calls use normal Bluetooth pairing. | **AI features use Solos-operated services/accounts.** They can be ignored, but this is still the most ecosystem-oriented device here. | Not clearly stated on current V2 listing | **IP54** | **US$299** | Ships to Australia; Solos currently lists approximately **US$45 AU shipping** | Most sophisticated actual **smart glasses** here. 16MP + stabilized 2K + proper audio is attractive, but least aligned with avoiding apps/accounts/cloud. |


## Additional Notes

NOTE: **AI Generated**.

### OHO Primex EIS

The manufacturer lists a 500mAh battery, 2K H.265 video, EIS, USB-C and OTG support.

That means the workflow can essentially be:

**Wear → press record → plug into phone/computer → copy MP4**

There is no account or cloud service sitting between you and your footage.

[OHO Primex EIS product page](https://ohosunshine.com/products/primex-eis-camera-glasses)

---

### iVUE Denali

This has the best-documented independence of the group.

iVUE explicitly states that:

- The app is optional
- Recording works directly from the glasses
- Wi-Fi connects **directly between the glasses and phone**
- **Internet isn't required**
- Storage is via a removable microSD card
- It supports cards up to 128GB
- It records 2K at 30fps or 1080p at 60fps
- It uses an 8MP Sony CMOS sensor
- It has dual stereo microphones
- It has a very wide 135° field of view

The removable microSD card is particularly attractive for long-term ownership because you're not dependent on internal flash storage or a proprietary cloud service.

The 135° lens is very wide. That's useful for BMX, riding, working and general POV footage, although it will look considerably more like an action camera than normal human vision.

[iVUE Denali product page](https://ivuecamera.com/products/denali-camera-glasses)

---

### OHO Brave 4K

This is almost comically simple compared with modern smart glasses:

**4K camera + microphone + internal storage + physical button**

That's attractive if what you actually want is a **wearable camera rather than "smart glasses."**

There is:

- No required account
- No required phone
- No required app
- No cloud dependency
- 4K/30fps recording
- Built-in microphone
- Local storage
- USB/OTG access to recordings
- Record-while-charging support

OHO includes an OTG connector for accessing footage from compatible devices.

The main downside is the lack of advertised electronic image stabilisation. For walking, cycling or BMX footage, stabilized 2K could potentially look considerably better than unstabilized 4K.

[OHO Brave 4K product page](https://ohosunshine.com/products/brave-4k-camera-glasses-polarized)

---

### OHO Edge Pro

This deserves more attention than I initially gave it.

On paper it comes remarkably close to the original requirements:

- **4K camera**
- Microphone
- Local storage
- Bluetooth 5.3
- Open-ear speakers
- Music playback
- Calls
- Approximately 41.5g
- Physical recording controls
- Optional smart/translation functionality

It therefore potentially gives you the simplicity of the OHO camera glasses **without giving up Bluetooth audio**.

It has optional translation/AI features, but unlike Meta, the fundamental camera/audio hardware isn't built around requiring an AI assistant.

The biggest reservation is OHO's documentation. Some of its published battery/runtime information is inconsistent, so I'd assume roughly 30 minutes of camera recording unless OHO confirms otherwise.

[OHO Edge Pro product page](https://ohosunshine.com/products/edge-pro-ai-smart-glasses-4k-camera-translation)

---

### Solos AirGo V2

The AirGo V2 has probably the most interesting camera specification among the more conventional "smart glasses":

- **16MP camera**
- **2K video**
- Electronic stabilisation
- Directional open-ear speakers
- Microphones
- Bluetooth 5.2
- Music playback
- Phone calls
- IP54
- Conventional-looking interchangeable frames

Solos also has considerably more sophisticated directional audio hardware than the dedicated camera-glasses manufacturers.

However, it's also the most software/ecosystem-oriented product in this comparison.

Solos provides an app and cloud-based AI functionality, and its AI services operate using Solos servers.

You don't have to care about those features. Ordinary Bluetooth audio can work through standard Bluetooth pairing, but media management and some camera functionality are more app-centric than the OHO or iVUE products.

So I'd think of it as:

**Solos AirGo V2 = smart glasses that contain a good camera**

whereas:

**OHO/iVUE = cameras built into glasses**

[Solos AirGo V2 product page](https://solosglasses.com/products/prime-2-smartglasses-solos-airgo%E2%84%A2-v2)

---

## The Most Interesting Comparison

For my requirements, I'd narrow the differences down to:

**OHO Primex EIS**  
2K + EIS + completely local

**iVUE Denali**  
Sony 2K + 1080p60 + 135° FOV + removable microSD + completely local

**OHO Brave**  
4K + completely local + inexpensive + extremely simple

**OHO Edge Pro**  
4K + local storage + Bluetooth audio + speakers

**Solos AirGo V2**  
16MP + stabilized 2K + Bluetooth audio + better smart-glasses hardware, but more software/ecosystem dependence

---

## Important: Resolution Isn't Image Quality

I would **not** assume:

> OHO 4K > Solos/Denali 2K

Actual image quality also depends heavily on:

- Sensor size and quality
- Lens quality
- Video bitrate
- Image processing
- Dynamic range
- Low-light performance
- Exposure control
- Electronic image stabilisation
- Motion handling

A good stabilized 2K camera can easily produce more useful footage than a cheap unstabilized 4K camera.

The iVUE Denali at least identifies its sensor as an **8MP Sony CMOS**, which gives considerably more information about the actual imaging hardware than simply advertising "4K."

For moving POV recording in particular, I'd put significant weight on **stabilisation**, not just resolution.

---

## Product Links

- [OHO Primex EIS](https://ohosunshine.com/products/primex-eis-camera-glasses)
- [iVUE Denali](https://ivuecamera.com/products/denali-camera-glasses)
- [OHO Brave 4K](https://ohosunshine.com/products/brave-4k-camera-glasses-polarized)
- [OHO Edge Pro](https://ohosunshine.com/products/edge-pro-ai-smart-glasses-4k-camera-translation)
- [Solos AirGo V2](https://solosglasses.com/products/prime-2-smartglasses-solos-airgo%E2%84%A2-v2)