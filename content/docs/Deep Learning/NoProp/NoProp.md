# NOPROP
NOPROP: TRAINING NEURAL NETWORKS WITHOUT BACK-PROPAGATION OR FORWARD-PROPAGATION

Qinyu Li, Yee Whye Teh, Razvan Pascanu [(arxiv)](https://arxiv.org/pdf/2503.24322) <a href="https://arxiv.org/pdf/2503.24322" target="_blank" rel="noopener noreferrer">arXiv:2503.24322</a>

The authors propose NoProp, a completely gradient-free method for training neural networks. No prop does not require back-prop or forwrad prop. Instead of learning via layer gradients, each layer is independently trained to denoise a noisy version of the label. And during inference, the noise is removed layer by layer.

### Problematic
- Biological implausibility of back-propagation.
- Memory costs due to storing activations during forward pass to facilitate backward passes.
- Sequential dependencies of propagation hinders parallel computing.
- Catastrophic forgetting in continual learning.

### Ideation
The authors were inspired by recent advances in generative modeling, specifically diffusion models and flow matching methods. The key insight is to ***reconceptualize neural network training*** - which we can be broken down to:

- Reframing the problem : denoising at each layer vs sequentially propagating information across layers.
- Fixing the representation at each layer beforehand to a noised version of the target.
- Questioning the assumption that hierarchical representations are necessary for effective learning.

### Contribution
Introducing NoProp and its variants.

**Variants**
- Discrete-Time NoProp (NoProp-DT): has a fixed number of denoising steps.
- Continuous-Time NoProp (NoProp-CT): learns a dynamic denoising process.
- Flow Matching (NoProp-FM): learns a vector field to carry noise to the label embedding.

**Modeling Considerations**
- NoProp requires pre-fixing representations at each layer -> careful modeling and design.
- The authors experimented with different **initialization strategies** for the class embedding matrix, including one-hot vectors, orthogonal matrices, and prototype-based approaches.
- For the continuous-time variants, there was added complexity in conditioning on time.

### Validation
- NoProp-DT performs on par or better than backprop on MNIST and CIFAR-10.
- NoProp variants outperform prior backprop-free methods like Forward-Forward (Hinton, 2022), Difference Target Propagation, Local Greedy Forward Gradient.
- NoProp uses less memory during training.



