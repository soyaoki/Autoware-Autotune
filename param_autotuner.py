import optuna
import yaml
import subprocess
import matplotlib.pyplot as plt
from time import sleep

# パラメータファイルを読み込む関数
def load_target_params(file):
    with open(file, "r") as f:
        return yaml.safe_load(f)

# パラメータをyamlファイルに書き込む関数
def update_yaml(file, data):
    with open(file, "r") as f:
        current_data = yaml.safe_load(f)
    
    # 既存のデータに新しい値を上書き
    for param1, value1 in data['ros__parameters'].items():
        if(isinstance(value1, (int, float))):
            current_data['/**']['ros__parameters'][param1] = value1
        else:
            for param2, value2 in data['ros__parameters'][param1].items():
                if(isinstance(value2, (int, float))):
                    current_data['/**']['ros__parameters'][param1][param2] = value2
                else:
                    for param3, value3 in data['ros__parameters'][param1][param2].items():
                        if(isinstance(value3, (int, float))):
                            current_data['/**']['ros__parameters'][param1][param2][param3] = value3
                        else:
                            for param4, value4 in data['ros__parameters'][param1][param2][param3].items():
                                if(isinstance(value4, (int, float))):
                                    current_data['/**']['ros__parameters'][param1][param2][param3][param4] = value4
                                else:
                                    for param5, value5 in data['ros__parameters'][param1][param2][param3][param4].items():
                                        if(isinstance(value5, (int, float))):
                                            current_data['/**']['ros__parameters'][param1][param2][param3][param4][param5] = value5

    with open(file, "w") as f:
        yaml.dump(current_data, f)

# Optunaによる最適化対象の評価関数
def objective(trial, param_ranges, param_files, target_param):
    params = {
        param: trial.suggest_float(param, param_ranges[param]['min'], param_ranges[param]['max']) if param_ranges[param]['type'] == 'float'
        else trial.suggest_int(param, param_ranges[param]['min'], param_ranges[param]['max'])
        for param in param_ranges
    }
    print(params)

    # ユーザーからの入力を行う部分
    print("Current parameters:")
    for param, value in params.items():
        print(f"{param}: {value}")
    
    # 各パラメータファイルを更新
    for file in param_files:
        data = {}
        if 'ros__parameters' in target_param[file]:
            data['ros__parameters'] = {}

        for param1 in target_param[file]['ros__parameters']:
            try:
                data['ros__parameters'][param1]
            except:
                data['ros__parameters'][param1] = {}

            if param1 in params:
                data['ros__parameters'][param1] = params[param1]
                continue
            else:
                for param2 in target_param[file]['ros__parameters'][param1]:
                    try:
                        data['ros__parameters'][param1][param2]
                    except:
                        data['ros__parameters'][param1][param2] = {}
                    
                    if param2 in params:
                        data['ros__parameters'][param1][param2] = params[param2]
                        continue
                    else:
                        for param3 in target_param[file]['ros__parameters'][param1][param2]:                            
                            try:
                                data['ros__parameters'][param1][param2][param3]
                            except:
                                data['ros__parameters'][param1][param2][param3] = {}

                            if param3 in params:
                                data['ros__parameters'][param1][param2][param3] = params[param3]
                                continue
                            else:
                                for param4 in target_param[file]['ros__parameters'][param1][param2][param3]:
                                    try:
                                        data['ros__parameters'][param1][param2][param3][param4]
                                    except:
                                        data['ros__parameters'][param1][param2][param3][param4] = {}

                                    if param4 in params:
                                        data['ros__parameters'][param1][param2][param3][param4] = params[param4]
                                        continue
                                    else:
                                        for param5 in target_param[file]['ros__parameters'][param1][param2][param3][param4]:
                                            try:
                                                data['ros__parameters'][param1][param2][param3][param4][param5]
                                            except:
                                                data['ros__parameters'][param1][param2][param3][param4][param5] = {}

                                            if param5 in params:
                                                data['ros__parameters'][param1][param2][param3][param4][param5] = params[param5]
                                                continue

        update_yaml(file, data)

    # run.bashを実行
    # subprocess.Popen(['bash','/aichallenge/run.sh'])

    # シミュレータを起動
    subprocess.Popen(['/aichallenge/aichallenge_ws/AWSIM/AWSIM.x86_64'])
    sleep(2)

    # ユーザーが評価値を入力
    evaluation = float(input("Enter the evaluation result: "))

    return evaluation

# メイン関数
def main():
    # 最適化対象のパラメータを含むyamlファイルを読み込む
    with open("target_param.yaml", "r") as file:
        target_param = yaml.safe_load(file)

    # 各パラメータファイルとその範囲を取得
    param_files = list(target_param.keys())
    param_ranges = {}
    for file in param_files:
         if 'ros__parameters' in target_param[file]:
            for param1, value1 in target_param[file]['ros__parameters'].items():
                if 'min' in value1 and 'max' in value1:
                    param_ranges[param1] = {
                        'min': value1['min'],
                        'max': value1['max'],
                        'type': value1['type']
                    }
                else:
                    for param2, value2 in target_param[file]['ros__parameters'][param1].items():
                        if 'min' in value2 and 'max' in value2:
                            param_ranges[param2] = {
                                'min': value2['min'],
                                'max': value2['max'],
                                'type': value2['type']
                            }
                        else:
                            for param3, value3 in target_param[file]['ros__parameters'][param1][param2].items():
                                if 'min' in value3 and 'max' in value3:
                                    param_ranges[param3] = {
                                        'min': value3['min'],
                                        'max': value3['max'],
                                        'type': value3['type']
                                    }
                                else:
                                    for param4, value4 in target_param[file]['ros__parameters'][param1][param2][param3].items():
                                        if 'min' in value4 and 'max' in value4:
                                            param_ranges[param4] = {
                                                'min': value4['min'],
                                                'max': value4['max'],
                                                'type': value4['type']
                                            }
                                        else:
                                            for param5, value5 in target_param[file]['ros__parameters'][param1][param2][param3][param4].items():
                                                if 'min' in value5 and 'max' in value5:
                                                    param_ranges[param5] = {
                                                        'min': value5['min'],
                                                        'max': value5['max'],
                                                        'type': value5['type']
                                                    }


    print(param_ranges)

    # Optunaでパラメータを最適化
    study = optuna.create_study(direction='maximize', study_name='Autoware_turning_study', storage='sqlite:///Autoware_turning_study.db', load_if_exists=True)
    study.optimize(lambda trial: objective(trial, param_ranges, param_files, target_param), n_trials=50)

    # パラメータの収束を図として表示
    for param in param_ranges:
        plt.plot([t.params[param] for t in study.trials], label=param)
    plt.legend()
    plt.xlabel("Iterations")
    plt.ylabel("Parameter Value")
    plt.show()

    # 評価関数の推移を図で表示
    plt.figure()
    plt.plot([t.values for t in study.trials], label='Evaluation Value')
    plt.xlabel('Iteration')
    plt.ylabel('Evaluation Value')
    plt.title('Evaluation Value Optimization')
    plt.show()

    # 各最適化結果をyamlファイルに保存
    # for i, trial in enumerate(study.trials):
    #     trial_params = trial.params
    #     trial_value = trial.value
    #     with open(f'optimization_result_{i + 1}.yaml', 'w') as file:
    #         yaml.dump({'params': trial_params, 'value': trial_value}, file)

if __name__ == '__main__':
    main()
