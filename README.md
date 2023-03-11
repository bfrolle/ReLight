## Usage

Press `Tab`, search for the **`piRelight`** node and add the node to your node graph. The node scans for light categories within existing layers. All layers with a `Light`, `light` or `LIGHT` prefix or suffix are considered as category. These are listed in the category knob (enumeration knob) of the `piRelight` node. 

You can add or remove selected categories using the `add` or `remove` button, which are node strings that include the consecutiv nodes  
- `Dot`,  
- `Shuffle2`,  
- `ColorCorrect`,  
- and two `Grade` nodes.  

Multiple categories are merged together by means of `Merge` nodes.

Remove all categories using the `reset` button.

## Install
Clone and rename this repository
```bash
git clone tbd ReLight
```

Copy this `ReLight` directory into NUKE's plug-in path directory `.nuke` and add the following line to the `.nuke/init.py` file:
```python
nuke.pluginAddPath("./ReLight")
```
