# CastToMPV
Share video links directly to MPV from Android (may be available for PC in the future)

<img width="256" height="256" alt="CastToMPV" src="https://github.com/user-attachments/assets/0b7b08d5-ee94-4dcc-a1fa-38d69f93b8fa" />

I came up with this idea because I have a mobile app for watching TV series, so I thought I could do this so I could transfer them to my PC and not have to install an emulator just for that.

[1. Installation](#installation)

[2. Requirements](#requirements)

[3. Usage](#usage)

[4. Arguments](#arguments)

[5. Troubleshooting](#troubleshooting)

# Installation

## PC (Server)
- `git clone https://github.com/MagmaSKV/CastToMPV` **(recommended)**

or

[Github Latest Release](https://github.com/MagmaSKV/CastToMPV/releases) **(you need a "test.mp4" file in the directory, such as the one in the repository or any file placed in the root directory, and rename it to "test.mp4")**

## Android (Client)
[Github Latest Release](https://github.com/MagmaSKV/CastToMPV-Android/releases/) **(recommended)**

or

- `git clone https://github.com/MagmaSKV/CastToMPV-Android` **(need compilation)**

# Requirements

## PC
- Python

## Android
- Android 7+

- Being able to share links through applications (like YouTube when you click share, which lets you share through applications)

# Usage

1. `python CastToMPV.py`

When you see it start like in the photo

<img width="474" height="173" alt="script_started" src="https://github.com/user-attachments/assets/56e770f7-595d-466b-8acd-e18198d401dd" />

2. Open the Android app and enter the IP address and port provided by the script. Once done, tap "💾 Save configuration".

⚠️ If the IP address you see isn't the one you're using, use "--show-ip" and search for the one you want to use. For example: If it's Zerotier, it won't be that IP address; it will be the one that appears with the interface that starts with "zt..."

<img width="365" height="391" alt="ip_port_android" src="https://github.com/user-attachments/assets/a352ac3b-9d43-4cc9-a98d-8efcc6aa535c" />

3. (optional but recommended) To test the connection to the server, press one of the two test buttons. Each one does something, so I'll explain:

📝In case of any error in any test, I would recommend checking [troubleshooting](#troubleshooting)
 or opening an issue.

- "🔗 Test Connection" > This performs a connection test to the HTTP server. The result will look like this:

- PC:

<img width="445" height="101" alt="pc_test" src="https://github.com/user-attachments/assets/94cbd704-25eb-4cb0-81d0-44bea710de6c" />

- Android:

<img width="317" height="101" alt="android_test" src="https://github.com/user-attachments/assets/d59da6e3-c962-4b9b-8f2c-3a0cafe28284" />

📝 "sdk_gphone64_x86_64" is the name of my emulated Android; the important thing is to see the same thing on both.

- "▶️ Test Video" > This performs a video test; it's mainly to check if the video will open when sent. Normally, if it opens, it almost certainly will work. If it doesn't open, the console will tell you something. And if it opens the test but not your video, it means mpv can't open the link.

⚠️ It will open the video file called "test.mp4" located in the root directory, so if you don't have it, it will almost certainly fail, although you can always change it as long as it's named "test.mp4".

- PC:

<img width="838" height="410" alt="pc_video_test" src="https://github.com/user-attachments/assets/e2cb2766-4b63-438c-bb47-16acf8205d59" />

- Android:

<img width="318" height="92" alt="android_video_test" src="https://github.com/user-attachments/assets/82032b16-ca5f-4e06-bc69-e4e922b8a127" />

📝 "sdk_gphone64_x86_64" is the name of my emulated Android; the important thing is to see the same thing on both.

4. When you're playing the video, look for any sharing option (**share link**, not screen like Chromecast (if you only see the Cast icon, check [troubleshooting](#troubleshooting))) and search for the "Cast To MPV" app.

<img width="373" height="118" alt="share_to" src="https://github.com/user-attachments/assets/3c7354ad-b1b2-413b-906c-53913007b740" />

5. The application should open on Android with a message that the video was sent from your device. On the PC, it should show that it's playing the video you sent from that same device in MPV format, and you should see the MPV window with the video you shared.

<img width="1709" height="1080" alt="video_on_mpv" src="https://github.com/user-attachments/assets/9a1dd762-6e4b-40b2-a87f-400bbc35e1d4" />

# Arguments

-  -h, --help           || Show help message
  
<img width="1123" height="294" alt="args_help" src="https://github.com/user-attachments/assets/20fd922c-5342-4d73-8dbe-28f4f8497a95" />

-  --debug              || Enable debug logging **(default: false)**

<img width="1018" height="573" alt="args_debug" src="https://github.com/user-attachments/assets/64a65d80-f812-44ed-9b74-050fd8f3e4fb" />

- --show-ip             || Show all local IP addresses

<img width="299" height="167" alt="args_show_ip" src="https://github.com/user-attachments/assets/9fe1d119-a7c6-4560-aa71-f100c63b69f5" />

-  --port PORT          || Port to listen on **(default: 8080)**
  
<img width="678" height="252" alt="args_port" src="https://github.com/user-attachments/assets/cd367fc0-1a3a-4c11-ae34-8f89591e5d69" />

-  --host HOST          || Host to bind to **(default: 0.0.0.0)**

⚠️ Changing it is not recommended; since the default IP address is 0.0.0.0, it applies to all interfaces, so it is usually not necessary to change it.
  
-  --app APP            || Application to use for video playback **(default: mpv)**

⚠️ The `--app` argument removes arguments (including the title) if they are not specified.

<img width="948" height="254" alt="args_app" src="https://github.com/user-attachments/assets/1ad09e20-792d-4b85-8624-3244b0d88bc1" />
  
-  --app_args APP_ARGS  || Arguments passed to the playback app **(default: --force-window --title TITLE)**

⚠️ The argument of `--title` within this command passes the title of the `--title` argument (or uses its default title).

<img width="1206" height="483" alt="args_app_args" src="https://github.com/user-attachments/assets/dbad7a15-c99e-45c9-931b-cb12a7218283" />

-  --title TITLE        || Window title (use {device} for device name) **(only for mpv or compatibles) (default: "Cast from {device}")**
  
<img width="1129" height="661" alt="args_title" src="https://github.com/user-attachments/assets/c3e0b8ac-c730-4f6b-87eb-6061af3d43c5" />

📝 You can use multiple arguments at the same time, such as application and arguments, or port, app, arguments, and debug simultaneously.

<img width="913" height="254" alt="multi_args" src="https://github.com/user-attachments/assets/fd50dcc4-f19f-473d-be93-d638221c044e" />

# Troubleshooting

- If the test video doesn't open, make sure you have the "test.mp4" file in the same directory as CastToMPV.py.

- As I explained in step 2 in [usage](#usage), it might not work if you enter the wrong IP address in Android. By default, the server opens at 0.0.0.0, which is the same for all the IP addresses your PC might have, like in my case: 127.0.0.1 (local), 192.168.1.101 (eth), 192.168.192.100 (zerotier)... It should work no matter which IP address you use, as long as it connects to your PC.

<img width="1167" height="919" alt="zerotier_mobile_data" src="https://github.com/user-attachments/assets/242ebe51-d9ab-4716-be3e-3bb63ae0dc73" />

- If you're using the correct IP address but still have no connection, neither during testing nor anything else, check your firewall and enable port 8080 (or whichever port you change it to) for it to work.

- If the app you're using only has Chromecast or Cast in general sharing capabilities, you'll have to figure out how to do it. In my case, the one I use only has Cast, but it's a fake Cast feature; it's through an app from the Play Store. So after opening it with that app, I can view it in a browser, share it, and use the app, and it works.

If you encounter any problems or want to suggest an option, just create an issue and say what you want. I'll try to answer as soon as possible :D
