# TeddyStick

An app for [M5StickC Plus](https://shop.m5stack.com/products/m5stickc-plus-esp32-pico-mini-iot-development-kit) that allows to change source for Tonies in [TeddyCloud](https://github.com/toniebox-reverse-engineering/teddycloud). See [this video](https://youtube.com/shorts/VxreeAtIGkQ) for an illustration.

## Installation
* Use [M5Burner](https://docs.m5stack.com/en/download) to install UIFlow2 to your M5StickC Plus (unless it came pre-flashed with it already).
* Clone the repository, rename `flash/sample_config.py` to `flash/config.py` and update its contents accordingly.
* Create the 135x180 JPG images for your tonies and put them in `flash/res/img`. Mention these images in your `flash/config.py`.
* Connect your M5StickC to your computer over USB and copy the contents of the `flash/` folder over (leaving the existing files intact and overwriting `main.py` and `boot.py`). I currently know of two ways to do it.
  * One option is to use the [Thonny](https://thonny.org/) editor. Click in the lower right corner to connect to your M5StickC, then click View->Files and you should see a panel that will allow you to move files between the M5StickC and your computer.
  * A somewhat less convenient option, which does not require installing any additional software is to use the UIFlow2 web IDE. First connect to your device over USB. Then click the "Device File Manager" icon to the right of the "USB Device: StickCPlus" button. It opens the Web terminal that has a "File" button on top that lets you copy files over to flash one by one.   

## License
* MIT