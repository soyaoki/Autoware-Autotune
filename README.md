# Autoware-Autotune

alpha release


## Installation

1. Set up aichallenge repo with the following reference

  https://github.com/soyaoki/aichallenge2023-sim/blob/main/documentation/docfx_project/setup/index.md

2. Clone this repository

```bash
cd ./aichallenge2023-sim/docker/aichallenge/aichallenge_ws/
git clone https://github.com/soyaoki/Autoware-Autotune
```

3. Run the docker container

```bash
cd ./../..
sudo bash run_container.sh
```

4. Intstall requirements

```bash
pip install optuna optuna-dashboard
```

5. Edit target parameters in `target_param.yaml`

6. Run 

```bash
cd /aichallenge/aichallenge_ws/Autoware-Autotune/
python3 param_autotuner.py 
```
(Option) 7. Run dashboad on anothoer terminal

```bash
cd ./aichallenge2023-sim/docker
sudo bash run_container.sh
pip install optuna optuna-dashboard
cd /aichallenge/aichallenge_ws/Autoware-Autotune/
optuna-dashboard sqlite:///Autoware_turning_study.db
```

## NOTICE

・The default iteration is 50 iterations.　（TODO: Make it possible to pass the number of iterations as an argument.）

```python
study.optimize(lambda trial: objective(trial, param_ranges, param_files, target_param), n_trials=50)
```
・Comments in Autoware parameter files (e.g., obstacle_avoidance_planner.param.yaml) will disappear.
