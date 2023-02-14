import random
import numpy as np
import wandb
import gym
import multiprocessing as mp


def FIFO_worker(default_config):
    wandb.init(config=default_config)
    config = wandb.config
    env = gym.make('JSSEnv:jss-v1', env_config={'instance_path': config['instance_path']})
    env.seed(config['seed'])
    random.seed(config['seed'])
    np.random.seed(config['seed'])
    done = False
    state = env.reset()
    while not done:
        real_state = np.copy(state['real_obs'])
        legal_actions = state['action_mask'][:-1]
        reshaped = np.reshape(real_state, (env.jobs, 7))
        remaining_time = reshaped[:, 5]
        illegal_actions = np.invert(legal_actions)
        mask = illegal_actions * -1e8
        remaining_time += mask
        FIFO_action = np.argmax(remaining_time)
        assert legal_actions[FIFO_action]
        state, reward, done, _ = env.step(FIFO_action)
    env.reset()
    make_span = env.last_time_step
    wandb.log({"nb_episodes": 1, "make_span": make_span})
    print("Makespan:", make_span)


if __name__ == "__main__":
    default_config = {
        'env': 'jss_env',
        'seed': 0,
        'framework': 'tf',
        'log_level': 'WARN',
        'num_gpus': 1,
        'instance_path': '../instances/rl500',
        'evaluation_interval': None,
        'metrics_smoothing_episodes': 2000,
        'gamma': 1.0,
        'num_workers': mp.cpu_count(),
        'layer_nb': 2,
        'train_batch_size': mp.cpu_count() * 4 * 704,
        'num_envs_per_worker': 4,
        'rollout_fragment_length': 704,  # TO TUNE
        'sgd_minibatch_size': 33000,
        'layer_size': 319,
        'lr': 0.0006861,  # TO TUNE
        'lr_start': 0.0006861,  # TO TUNE
        'lr_end': 0.00007783,  # TO TUNE
        'clip_param': 0.541,  # TO TUNE
        'vf_clip_param': 26,  # TO TUNE
        'num_sgd_iter': 12,  # TO TUNE
        "vf_loss_coeff": 0.7918,
        "kl_coeff": 0.496,
        'kl_target': 0.05047,  # TO TUNE
        'lambda': 1.0,
        'entropy_coeff': 0.0002458,  # TUNE LATER
        'entropy_start': 0.0002458,
        'entropy_end': 0.002042,
        'entropy_coeff_schedule': None,
        "batch_mode": "truncate_episodes",
        "grad_clip": None,
        "use_critic": True,
        "use_gae": True,
        "shuffle_sequences": True,
        "vf_share_layers": False,
        "observation_filter": "NoFilter",
        "simple_optimizer": False,
        "_fake_gpus": False,
    }
    FIFO_worker(default_config)
