import pyemu

# Create PEST object from template/ins files
pst = pyemu.Pst.from_io_files(
    tpl_files=["params.tpl"],  # Template file for parameters
    in_files=["params.txt"],  # Input file for parameters
    ins_files=["output.ins"],  # Instruction file for model output
    out_files=["output.txt"]  # Output file from the model
)

# Set parameter transformation to 'none' (no log transformations)
pst.parameter_data["partrans"] = "none"

# Set reasonable bounds and initial guesses for parameters
pst.parameter_data.loc["a", "parval1"] = 1.0  # Initial guess for 'a'
pst.parameter_data.loc["a", "parlbnd"] = 0.0  # Lower bound for 'a'
pst.parameter_data.loc["a", "parubnd"] = 5.0  # Upper bound for 'a'

pst.parameter_data.loc["b", "parval1"] = 1.0  # Initial guess for 'b'
pst.parameter_data.loc["b", "parlbnd"] = 0.0  # Lower bound for 'b'
pst.parameter_data.loc["b", "parubnd"] = 5.0  # Upper bound for 'b'

# Optional: scale parameters uniformly (useful for numerical stability)
pst.parameter_data["parscale"] = 1.0

# Set observation value and weight
pst.observation_data["obsval"] = 0.0  # Target value for the observation
pst.observation_data["weight"] = 1.0  # Weight for the observation

# Set model command to run the Python model script
pst.model_command = ["python model.py"]

# Configure control data for GLM
pst.control_data.pestmode = "estimation"  # Set mode to estimation
pst.control_data.noptmax = 20             # Allow more iterations
pst.control_data.relparstp = 0.001        # Stricter parameter change threshold
pst.control_data.phiredstp = 0.001        # Stricter phi reduction threshold


# Adjust regularization in parameter groups
pst.parameter_groups.loc["pargroup1", "inctyp"] = "relative"
pst.parameter_groups.loc["pargroup1", "derinc"] = 0.1  # Increase regularization weight

# Write the updated control file
pst.write("simple_glm.pst", version=2)