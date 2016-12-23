import tensorflow as tf

from .flag import FLAGS, FlagAdder
from .estimator import def_estimator
from .inputs import Mode, def_def_train_input_fn, def_def_eval_input_fn


def def_def_experiment_fn(batch_inputs=True):
    adder = FlagAdder()

    for mode in Mode:
        mode = mode.value
        adder.add_flag("{}_steps".format(mode), type=int,
                       help="Maximum number of {} steps".format(mode))

    adder.add_flag("min_eval_frequency", type=int, default=1,
                   help="Minimum evaluation frequency in number of model "
                        "savings")

    estimator = def_estimator()
    def_train_input_fn = def_def_train_input_fn(batch_inputs)
    def_eval_input_fn = def_def_eval_input_fn(batch_inputs)

    def def_experiment_fn(model_fn, train_input_fn, eval_input_fn=None):
        def experiment_fn(output_dir):
            return tf.contrib.learn.Experiment(
                estimator(model_fn, output_dir),
                def_train_input_fn(train_input_fn),
                def_eval_input_fn(eval_input_fn or train_input_fn),
                **adder.flags)

        return experiment_fn

    return def_experiment_fn
