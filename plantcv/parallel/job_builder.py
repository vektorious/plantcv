import os
import sys
import json
from copy import deepcopy
import uuid


# Build job list
###########################################
def job_builder(meta, config):
    """Build a list of image processing jobs.

    Inputs:
    meta:         Dictionary of processed image metadata.
    config:       plantcv.parallel.WorkflowConfig object.

    Returns:
    jobs:         List of image processing commands.

    :param meta: dict
    :param config: plantcv.parallel.WorkflowConfig
    :return job_stack: list
    """
    # Overall job stack. List of list of jobs
    jobs = []

    # Log the number of jobs to be run
    n_jobs = len(meta)
    print(f"Job list will include {n_jobs} images", file=sys.stderr)

    # Each grouping has a tuple of grouped metadata values and a dataframe of image metadata
    for grp, grp_df in meta:
        # Create a JSON template for each group
        img_meta = {"metadata": deepcopy(config.metadata_terms), "observations": {}}

        # Store metadata in JSON
        img_meta["metadata"]["image"] = {
                "label": "image files",
                "datatype": "<class 'str'>",
                "value": grp_df["filepath"].values.tolist()
            }

        # Convert datetime to string before serialization
        grp_df["timestamp"] = grp_df["timestamp"].dt.strftime(config.timestampformat)

        # Valid metadata
        for m in list(config.metadata_terms.keys()):
            img_meta["metadata"][m]["value"] = grp_df[m].values.tolist()

        # Create random unique output file to store the image processing results and populate with metadata
        outfile = os.path.join(config.tmp_dir, f"{uuid.uuid4()}.json")
        with open(outfile, "w") as fp:
            json.dump(img_meta, fp, indent=4)

        # Build job
        job_parts = ["python", config.workflow, "--outdir", config.img_outdir, "--result", outfile]
        # Add job to list
        if config.writeimg:
            job_parts.append("--writeimg")
        if config.other_args:
            job_parts = job_parts + config.other_args
        for fname in grp_df["filepath"].values.tolist():
            job_parts.append(fname)
        jobs.append(job_parts)

    return jobs
###########################################
