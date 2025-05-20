import pyemu

pst = pyemu.Pst.from_io_files(
    tpl_files=["params.tpl"],
    in_files=["params.txt"],
    ins_files=["output.ins"],
    out_files=["output.txt"]
)

pst.parameter_data["partrans"] = "none"
pst.parameter_data.loc["a", "parval1"] = 2.3
pst.parameter_data.loc["a", "parlbnd"] = 0.0
pst.parameter_data.loc["a", "parubnd"] = 4.0

pst.parameter_data.loc["b", "parval1"] = 2.8
pst.parameter_data.loc["b", "parlbnd"] = 0.0
pst.parameter_data.loc["b", "parubnd"] = 5.0

pst.observation_data["obsval"] = 0.0
pst.observation_data["weight"] = 1.0

pst.model_command = ["python model.py"]
pst.control_data.noptmax = 20
pst.control_data.pestmode = "estimation"

# Add PESTPP-IES specific settings
pst.pestpp_options["ies_num_reals"] = 100
pst.pestpp_options["ies_lambda_mults"] = "0.1,1.0,10"
pst.pestpp_options["ies_subset_size"] = 20
pst.pestpp_options["ies_subset_how"] = "phi_based"


# Write the PEST file
pst.write("simple.pst", version=2)

# Create initial ensemble
pe = pyemu.ParameterEnsemble.from_gaussian_draw(pst, num_reals=100, sigma_range=2)
pe.to_csv("simple.0.par.csv")
