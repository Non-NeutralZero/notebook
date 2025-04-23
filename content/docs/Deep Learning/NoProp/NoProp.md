# NOPROP
NOPROP: TRAINING NEURAL NETWORKS WITHOUT BACK-PROPAGATION OR FORWARD-PROPAGATION

Qinyu Li, Yee Whye Teh, Razvan Pascanu [(arxiv)](https://arxiv.org/pdf/2503.24322) <a href="https://arxiv.org/pdf/2503.24322" target="_blank" rel="noopener noreferrer">arXiv:2503.24322</a>

The authors propose NoProp, a completely gradient-free method for training neural networks. Instead of learning via layer gradients, each layer is independently trained to denoise a noisy version of the label. And during inference, the noise is removed layer by layer.

