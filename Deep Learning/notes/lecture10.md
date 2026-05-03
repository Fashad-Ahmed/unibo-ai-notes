![alt text](image-46.png)

![alt text](image-47.png)

![alt text](image-48.png)

![alt text](image-49.png)

![alt text](image-50.png)

![alt text](image-51.png)


Why Residual Learning works?
- it seems to be a good idea to try to learn non-linear
corrections over a linear baseline

- during back propagation, the gradient at higher layers
can easily pass to lower layers, withouth being
mediated by the weight layers, which may cause vanishing
gradient or exploding gradient problem.


![alt text](image-52.png)


##### When Transfer Learning makes sense
transferring knowledge from problem A to problem
B makes sense if

- the two problems have “similar” inputs
- we have much more training data for A
than for B