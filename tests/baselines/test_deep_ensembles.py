from torch_uncertainty.baselines.classification.deep_ensembles import (
    DeepEnsembles,
)


class TestDeepEnsembles:
    """Testing the Deep Ensembles baseline class."""

    def test_standard(self):
        DeepEnsembles(
            log_path=".",
            checkpoint_ids=[],
            backbone="resnet",
            num_classes=10,
        )
