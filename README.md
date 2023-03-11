## Usage

Press `Tab`, search for the **`piRelight`** node and the node to your node graph. The node itself is a `Group` node. The tool scans for light categories within existing layers. All layers with a 
- `Light`
- `light` 
- or `LIGHT`

 prefix or suffix are considered as category. These are listed in the category knob (enumeration knob) of the `piRelight` node. 

You can add or remove selected categories to the group node using the `add` or `remove` button, which are node strings that include the consecutive nodes  
- `Dot`,  
- `Shuffle2`,  
- `ColorCorrect`,  
- and two `Grade` nodes.  

Multiple categories are merged together using `Merge` nodes. Remove all categories with the `reset` button.

## Install
Clone this repository or download, unzip and copy it into NUKE's plug-in path directory `.nuke`.

Add the following line to the `.nuke/init.py` file:
```python
nuke.pluginAddPath("./ReLight")
```
