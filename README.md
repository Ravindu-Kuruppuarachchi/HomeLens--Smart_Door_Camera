# HomeLens: Smart Door camera with Motion Detection & Email Alert System

This Python script (`Smart_Door.py`) uses a Raspberry Pi camera (or similar camera setup) to detect motion at a door. Once motion is detected, it records a short video and emails images to a specified email address.

## Features

1. **Motion Detection**  
   Compares two consecutive images to detect changes above a certain threshold.
2. **Video Recording**  
   If motion is detected, the script triggers `libcamera-vid` to record a short video and then converts it to MP4 using `ffmpeg`.
3. **Email Alert**  
   Automatically emails captured still images (before and after motion) to a configured email address.
4. **Configurable**  
   Threshold values, email settings, and camera settings can be adjusted in the script to suit different environments.

## How It Works

1. **Image Capture**  
   - Runs `libcamera-still` command twice in quick succession to take two images (`test00.jpg` and `test01.jpg`).
   - Applies a mask to ignore specific regions in the images if desired (this script demonstrates a sample polygon mask).
   - Converts masked images to grayscale and uses Gaussian blur to reduce noise.

2. **Change Detection**  
   - Compares the grayscale images pixel-by-pixel.
   - If the difference exceeds a certain threshold, it triggers further action (recording and emailing).

3. **Recording & Conversion**  
   - If motion is detected, starts a short (5-second) video recording via `libcamera-vid`.
   - Converts the recorded `.h264` file to `.mp4` using `ffmpeg`.

4. **Email Notification**  
   - Sends the still images (`test00.jpg`, `test01.jpg`, plus processed grayscale and masked images) to a specified email.
   - Uses SMTP (Gmail in this example) to deliver the files.

## Prerequisites

1. **Hardware**  
   - Raspberry Pi (or a similar Linux-based device) with a camera module or supported USB camera.
2. **Software/Libraries**  
   - Python 3.x
   - [OpenCV](https://opencv.org/) (`import cv2`)
   - [imutils](https://github.com/jrosebr1/imutils)
   - [NumPy](https://numpy.org/)
   - [libcamera](https://www.raspberrypi.com/documentation/computers/camera_software.html) tools installed (`libcamera-still` and `libcamera-vid`).
   - [ffmpeg](https://ffmpeg.org/) installed (for `.h264` to `.mp4` conversion).
   - [smtplib](https://docs.python.org/3/library/smtplib.html) (included in Python standard library).
3. **Camera Access**  
   - Ensure the camera is enabled and accessible on your system (e.g., enable the camera via `raspi-config` on Raspberry Pi).

## Installation

1. Clone or copy this repository to your Raspberry Pi:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```
2. Install the Python libraries if they are not already installed:
   ```bash
   pip install opencv-python imutils numpy
   ```
3. Verify that `libcamera-still`, `libcamera-vid`, and `ffmpeg` are installed on your system. For a Raspberry Pi OS, you can install them (if needed) via:
   ```bash
   sudo apt-get update
   sudo apt-get install libcamera-apps ffmpeg
   ```

## Configuration

1. **Email Settings**  
   - Inside the script, locate the following section:
     ```python
     smtpUser= "email@gmail.com"
     smtpPass="password"
     toAdd= "sendemail@gmai.com"
     ```
   - Change these to the appropriate values for your setup:
     - `smtpUser`: The sender's email address.
     - `smtpPass`: The sender’s email password or app-specific password.
     - `toAdd`: The recipient's email address.

   Note: Using a Gmail account often requires enabling “Less Secure Apps” or using an App Password. See [Google’s documentation](https://support.google.com/accounts/answer/185833) for more details.

2. **Motion Threshold**  
   - `pixel_thres = 50` can be adjusted to reduce or increase sensitivity.
   - `if detector_total > 4000:` can be changed to raise or lower the overall motion threshold.

3. **Camera & Video Settings**  
   - `libcamera-still` and `libcamera-vid` commands can be customized to your resolution, framerate, or other specific needs.
   - Paths for output files can also be updated if you wish to store them in a specific directory.

## Usage

1. **Connect your camera** and ensure it is recognized by your Raspberry Pi or Linux device.
2. **Run the script**:
   ```bash
   python Smart_Door.py
   ```
3. **Monitor output** in the console. You should see messages indicating:
   - Images captured
   - Pixel difference values
   - Whether or not motion was detected
   - Video recording steps
   - Email sending status

If motion is detected, you will receive an email containing the images as attachments, and an MP4 file of the recording is saved locally.

## Troubleshooting

- If the camera fails to initialize, double-check your Raspberry Pi camera settings using `raspi-config`, or verify that your USB camera is accessible (`/dev/video0`, etc.).
- If the email fails to send:
  - Verify your internet connection.
  - Confirm the SMTP settings (port, user credentials, security).
  - Check for any firewall or ISP restrictions on SMTP ports.

## Contributing

Feel free to open issues or submit pull requests to improve this project (e.g., better masking methods, advanced motion detection techniques, or alternative notification channels).

## License

No explicit license is provided here. You are free to use or modify the code for your own projects. If you redistribute the script, please include attribution to the original author(s).

---
