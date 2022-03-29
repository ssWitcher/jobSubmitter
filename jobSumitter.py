import chunk
import outline
import outline.cuerun
import outline.modules.shell
import uuid
 
def buildLayer(layerData, command, lastLayer=None):
    """Creates a PyOutline Layer for the given layerData.
    """
    threadable = float(layerData["cores"]) >= 2
    threadable = False
    layer = outline.modules.shell.Shell(
        layerData["name"], command=command.split(), chunk=layerData["chunk"],
        threads=float(layerData["cores"]), threadable=threadable)
 
    return layer
 
"""Submits the job using the PyOutline API."""
def submitJob(q):
    tempDict = q.get()
    input_file_path = tempDict["input_file_path"]
    output_file = tempDict["output_file"]
    jobData = {}
    jobData["name"] = input_file_path.split("/")[-1]+"_"+uuid.uuid4()
    jobData["shot"] = "Shot_name"
    jobData["show"] =  "testing"
    jobData["username"] = "vivek.bhardwaj"
   
    ol = outline.Outline(
        jobData['name'], shot=jobData['shot'], show=jobData['show'], user=jobData['username'])
 
    layerData = {}
    layerData["cores"] = 1
    layerData["name"] = "layer101"
    layerData["chunk"] = 1
    cmd = "/usr/local/blender/blender -b "+input_file_path+"  -noaudio -o /home/assets/"+output_file+"_##### -F PNG -f 20"
 
    layer = buildLayer(layerData, cmd)
    
    ol.add_layer(layer)
    print (jobData)
    print(layer)
    return outline.cuerun.launch(ol, use_pycuerun=False)