<!--
 Copyright (C) 2022 Akash R Chandran

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as
 published by the Free Software Foundation, either version 3 of the
 License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
-->

<h1 align="center">
Syrics
</h1>

<div align="center">

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
 
</div>
 
 <div align="center">

A command line tool to fetch lyrics from spotify and save it to file. It can fetch both synced and unsynced lyrics from spotify. 
 
</div>
 
 
## Getting started

> You will need a **spotify account**, free also works

### Install with git clone

```
git clone https://github.com/akashrchandran/syrics
cd syrics
pip install -r requirements.txt
```
### Change sample_config.json to config.json
*On Linux or Mac*
```
mv sample_config.json config.json
```
*On Windows*
```
ren sample_config.json config.json
```

### Finding sp_dc
> Syrics sp_dc cookie to authenticate against Spotify in order to have access to the required services.

To obtain the cookies, these different methods can be used:

**Do make sure are logged in on [Spotify](https://open.spotify.com) and then use any method below**
#### 1. Using cookies editor extension

_Using any extensions like [Cookie-Editor](https://cookie-editor.cgagnier.ca/#download) can easily help you find it_

![Cookie-Editor](https://i.ibb.co/zJ1KDGP/Screenshot-from-2022-05-17-23-26-33.png)

#### 2. Chromium based browser
1. Make sure you are connected on https://open.spotify.com
2. Open the url chrome://settings/cookies/detail?site=spotify.com or edge://settings/cookies/detail?site=spotify.com based on your browser.
3. Copy the content from sp_dc cookies

![Chrome_Based_Browser](https://i.ibb.co/DYrCQV0/Screenshot-from-2022-05-18-00-02-56.png)

#### 3. Developer Tools
_Chrome based_
1. Make sure https://open.spotify.com is opened and you are connected
2. Press Command+Option+I (Mac) or Control+Shift+I or F12. This should open the developer tools menu of your browser.
3. Go into the application section
4. In the menu on the left go to Storage/Cookies/open.spotify.com
5. Find the sp_dc (use the filter tab to search for it) and copy the value

![Using_Developer_Tools](https://i.ibb.co/RvwN206/Screenshot-from-2022-05-11-01-11-54.png)

_Firefox_
1. Make sure https://open.spotify.com is opened and you are connected
2. Press Command+Option+I (Mac) or Control+Shift+I or F12. This should open the developer tools menu of your browser.
3. Go into the Storage section. (You might have to click on the right arrows to reveal the section)
4. Select the Cookies sub-menu and then https://open.spotify.com
6. Find the sp_dc and copy the value

#### 4. For Android phone users
> Download [Kiwi browser](https://play.google.com/store/apps/details?id=com.kiwibrowser.browser)
1. Make sure https://open.spotify.com is opened and you are connected
2. copy this url and open it in kiwi kiwi://settings/cookies/detail?site=spotify.com
3. Find sp_dc and copy it

![Kiwi_android](https://i.ibb.co/FzGrvf3/IMG-20220518-082740.jpg)

### Config File

> You may have noticed a config.json in the code directory.
> After finding sp_dc you should edit config file and set sp_dc to the value you found.

```JSON
{
    "sp_dc": "",
    "client_id": "",
    "client_secret": "",
    "download_path": "downloads",
    "create_folder": true,
    "folder_name": "{album} - {artist}",
    "file_name": "{track_number}",
    "synced_lyrics": true,
    "force_synced": true
}
```
See wiki for more details about the tags.

### Usage
> Make sure you have set the congig before starting

1. Direct
```
python3 syrics.py
Enter link: https://open.spotify.com/track/2eAvDnpXP5W0cVtiI0PUxV
```
__It will ask for the link__

2. Command line
```
python3 syrics.py https://open.spotify.com/track/2eAvDnpXP5W0cVtiI0PUxV
```
