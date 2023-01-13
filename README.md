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


<div align="center">

[![syrics logo](https://ik.imagekit.io/gyzvlawdz/Projects/syrics/Black_Modern_Business_Logo__600___500_px___2240___1260_px__cYRO9HGTQ.png)](https://pypi.org/project/syrics/)
 
</div>
 
 <div align="center">

A command line tool to fetch lyrics from spotify and save it to lrc file. It can fetch both synced and unsynced lyrics from spotify. You can find API version at [akashrchandran/spotify-lyrics-api](https://github.com/akashrchandran/spotify-lyrics-api).
 
</div>
 
 
## Getting started

> You will need a **spotify account**, free also works

### Install with pip

```
pip3 install syrics
```
### Upgrade with pip

```
pip3 install syrics --upgrade
```
> To get more detailed installation guide please check wiki's [installation page](https://github.com/akashrchandran/syrics/wiki/Installation)

### Finding sp_dc
> Syrics sp_dc cookie to authenticate against Spotify in order to have access to the required services.

The methods are explained in the [wiki](https://github.com/akashrchandran/syrics/wiki/Finding-sp_dc).

### Config
> When you run the program for the first time, it will directly create config and open editing.

*To edit config*

```
syrics --config
```

*To reset config to default values*

```
syrics --config reset
```
*To open config in notepad or nano text editors*
```
syrics --config open
```
> After finding sp_dc you should edit config file and set sp_dc to the value you found.

*Default values of config*

```JSON
{
    "sp_dc": "",
    "download_path": "downloads",
    "create_folder": true,
    "album_folder_name": "{name} - {artists}",
    "play_folder_name": "{name} - {owner}",
    "file_name": "{track_number}. {name}",
    "synced_lyrics": true,
    "force_download": false,
    "force_synced": false
}
```
See wiki for more details about the format tag detailts in [config keys](https://github.com/akashrchandran/syrics/wiki/Config-Keys).

### Usage
> Make sure you have set the congig before starting

#### 1. Direct
```
syrics
Enter link: https://open.spotify.com/track/2eAvDnpXP5W0cVtiI0PUxV
```
 __It will ask for the link__

#### 2. Passing link as commandline argument
```
syrics https://open.spotify.com/track/2eAvDnpXP5W0cVtiI0PUxV
```
__changing download folder command__
```
syrics --directory ~/Music/songs/ https://open.spotify.com/track/2eAvDnpXP5W0cVtiI0PUxV
```
__download current playing song on authorized account__
```
syrics --user current-playing
```
__downloading from user playlist__
```
syrics --user playlist
```
__To see available commands__
```
syrics -h
```

#### 3. Passing Folder path with music files (Experimental)

```
syrics /home/public_user/Music/songs
```

### Use as a module

```python
from syrics.api import Spotify
sp = Spotify("SP_DC here!")
sp.get_lyrics("28RQx5pH9T9LZXY02IheWc")
```
