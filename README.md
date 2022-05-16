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

#### 1. Use cookies extension

_Using any extensions like [editthiscookie](https://www.editthiscookie.com/) can easily help you find it_

#### 2. Chromium based browser
1. Make sure you are connected on https://open.spotify.com
2. Open the url chrome://settings/cookies/detail?site=spotify.com or edge://settings/cookies/detail?site=spotify.com based on your browser.
3. Copy the content from sp_dc cookies

#### 3. Developer Tools
_Chrome based_
1. Make sure https://open.spotify.com is opened and you are connected
2. Press Command+Option+I (Mac) or Control+Shift+I or F12. This should open the developer tools menu of your browser.
3. Go into the application section
4. In the menu on the left go int Storage/Cookies/open.spotify.com
5. Find the sp_dc and copy the value

_Firefox_
1. Make sure https://open.spotify.com is opened and you are connected
2. Press Command+Option+I (Mac) or Control+Shift+I or F12. This should open the developer tools menu of your browser.
3. Go into the Storage section. (You might have to click on the right arrows to reveal the section)
4. Select the Cookies sub-menu and then https://open.spotify.com
6. Find the sp_dc and sp_key and copy the values
