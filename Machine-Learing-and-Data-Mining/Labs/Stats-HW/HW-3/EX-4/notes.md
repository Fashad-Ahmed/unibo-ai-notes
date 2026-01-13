
def adam(L_fn, grad_L_fn, X, y, theta0,
         eta=1e-3, epochs=200, batch_size=32,
         beta1=0.9, beta2=0.999, eps=1e-8, seed=0):
    """
    Adam optimizer (mini-batch):
      m <- beta1*m + (1-beta1)*g
      v <- beta2*v + (1-beta2)*g^2
      mhat, vhat bias-corrected
      theta <- theta - eta * mhat/(sqrt(vhat)+eps)
    Tracks full-dataset loss + accuracy at end of each epoch.
    """