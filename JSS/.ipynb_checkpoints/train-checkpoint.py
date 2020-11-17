import ray
import wandb
from ray import tune

from ray.rllib.agents.impala import ImpalaTrainer

from JSS.CustomCallbacks import CustomCallbacks

from JSS.default_config import default_config
from ray.rllib.agents import with_common_config
from ray.rllib.utils import try_import_torch
from ray.rllib.models import ModelCatalog
from ray.tune import CLIReporter, register_env
from JSS.env_wrapper import BestActionsWrapper
from JSS.env.JSS import JSS

from JSS.models import FCMaskedActionsModel

def env_creator(env_config):
    return BestActionsWrapper(JSS(env_config))


register_env("jss_env", env_creator)


def train_func():
    torch, nn = try_import_torch()
    ModelCatalog.register_custom_model("fc_masked_model", FCMaskedActionsModel)
    wandb.init(config=default_config, project="impala-jss")
    config = wandb.config
    config['model'] = {
        "fcnet_activation": "tanh",
        "custom_model": "fc_masked_model",
        'fcnet_hiddens': [config['layer_size'] for k in range(config['layer_nb'])],
    }
    config['env_config'] = {
        'instance_path': config['instance_path']
    }

    config['train_batch_size'] = config['num_workers'] * config['num_envs_per_worker'] * config[
        'rollout_fragment_length']
    config = with_common_config(config)
    config['callbacks'] = CustomCallbacks

    config.pop('instance_path', None)
    config.pop('layer_size', None)
    config.pop('layer_nb', None)

    ray.init()

    stop = {
        "time_total_s": 10 * 60,
    }

    analysis = tune.run(ImpalaTrainer, config=config, stop=stop, name="ppo-jss")
    wanb.sweep(analysis)
    result = analysis.results_df.to_dict('index')
    last_run_id = list(result.keys())[0]
    result = result[last_run_id]
    wandb.log({'time_step_min': result['custom_metrics.time_step_min']})
    if result['custom_metrics.time_step_max'] != float('inf'):
        wandb.log({'time_step_max': result['custom_metrics.time_step_max']})
        wandb.log({'time_step_mean': result['custom_metrics.time_step_mean']})
    wandb.log({'episode_reward_max': result['episode_reward_max']})
    wandb.log({'episode_reward_min': result['episode_reward_min']})
    wandb.log({'episode_reward_mean': result['episode_reward_mean']})
    wandb.log({'episodes_total': result['episodes_total']})
    wandb.log({'training_iteration': result['training_iteration']})

    ray.shutdown()


if __name__ == "__main__":
    train_func()
