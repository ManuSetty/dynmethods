import wishbone
import os
import sys
import json
import pandas as pd


#   ____________________________________________________________________________
#   Load data                                                               ####
p = json.load(open("/input/params.json", "r"))

# get start cell(s)
start_cell = json.load(open("/input/start_cells.json"))[0]

# get markers if given
if os.path.exists("/input/marker_feature_ids.json"):
  markers = json.load(open("/input/marker_feature_ids.json"))
else:
  markers = "~"

# get number of end states if given
if os.path.exists("/input/n_end_states.json"):
  branch = json.load(open("/input/n_end_states.json"))[0] > 1
else:
  branch = p["branch"]


#   ____________________________________________________________________________
#   Create trajectory                                                       ####
# normalise data
scdata = wishbone.wb.SCData.from_csv("/input/counts.csv", data_type='sc-seq', normalize=p["normalise"])
scdata.run_pca()
scdata.run_diffusion_map(knn=p["knn"], epsilon=p["epsilon"], n_diffusion_components=p["n_diffusion_components"], n_pca_components=p["n_pca_components"], markers=markers)

# check waypoints parameter to be lower than # cells
if p["num_waypoints"] > scdata.data.shape[0]:
  p["num_waypoints"] = scdata.data.shape[0]

# run wishbone
wb = wishbone.wb.Wishbone(scdata)
wb.run_wishbone(start_cell=start_cell, components_list=list(range(p["n_diffusion_components"])), num_waypoints=int(p["num_waypoints"]), branch=branch, k=p["k"])


#   ____________________________________________________________________________
#   Process output & save                                                   ####
# progressions
progressions = wb.trajectory.reset_index()
progressions.columns = ["cell_id", "percentage"]
if branch:
  progressions["from"] = pd.Series(["M1", "M2", "M2"])[wb.branch - 1].tolist()
  progressions["to"] = pd.Series(["M2", "M3", "M4"])[wb.branch - 1].tolist()
else:
  progressions["from"] = "M1"
  progressions["to"] = "M2"

progressions.to_csv("/output/progressions.csv", index=False)

# milestone network
if branch:
  milestone_network = pd.DataFrame({"from":["M1", "M2", "M2"], "to":["M2", "M3", "M4"], "length":1, "directed":True})
else:
  milestone_network = pd.DataFrame({"from":["M1"], "to":["M2"], "length":1, "directed":True})

milestone_network.to_csv("/output/milestone_network.csv", index=False)

# pseudotime
pseudotime = wb.trajectory.reset_index()
pseudotime.columns = ["cell_id", "pseudotime"]
pseudotime.to_csv("/output/pseudotime.csv", index=False)

# dimred
dimred = wb.scdata.diffusion_eigenvectors
dimred.index.name = "cell_id"
dimred.reset_index().to_csv("/output/dimred.csv", index=False)
