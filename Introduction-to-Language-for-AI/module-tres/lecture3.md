functions

given x,y sets,

X x Y = {(x, y) | x  belongsto X, Y BELONGSTO Y}

A relation on X,Y is a subset of XxY. 
A function from X (the domain) to Y (The Codomain) is a relation fC_ XxY such that for every x belongsto X ther is one y belongsto Y such that (x, y) belongs fc (fucniton)


and we write f: X -> Y



A bijection (or bijective function) is a function between two sets that establishes a perfect "one-to-one correspondence," where every element in the domain maps to a unique element in the codomain, and every element in the codomain is mapped to exactly once. It is both injective (one-to-one) and surjective (onto). 

 #### Key characteristics of a bijection:
 - Injective (One-to-One): Distinct inputs always map to distinct outputs, ensuring no two elements in the domain share the same image.
- Surjective (Onto): Every element in the codomain is mapped to by at least one element from the domain, meaning the codomain equals the range.
- Invertibility: A function is bijective if and only if it is invertible, meaning a unique inverse function exists that maps the codomain back to the domain.
- Cardinality: If a bijection exists between two sets, they have the same number of elements (or the same cardinality if infinite).



characterisitic funcitons (boolean functions)


Asymptotic notation is used in computer science to describe the performance or complexity of an algorithm (how its runtime or space requirements grow as the input size, , gets infinitely large).

**1. Big-O (): The Upper Bound**

* **Concept:** It describes the worst-case scenario. It guarantees that a function will not grow faster than a certain rate.
* **Math:** . The function  is always less than or equal to  (multiplied by some constant ) once  gets large enough.
* **Image Example:**  is  because the  term dictates the maximum growth rate. It is also  and  because those grow even faster and easily "cap" . It is not  because  grows much faster than .

**2. Big-Omega (): The Lower Bound**

* **Concept:** It describes the best-case scenario. It guarantees that a function will grow *at least* this fast.
* **Math:** . The function  is always greater than or equal to  (multiplied by some constant ) once  gets large enough.
* **Image Example:**  is  and  because its growth will never be slower than those rates. It is not  because  grows much faster, meaning  cannot act as a lower floor for .

**3. Big-Theta (): The Tight Bound**

* **Concept:** It describes the exact asymptotic behavior. It means the function grows at the exact same rate as the bound.
* **Math:** A function is  if it is **both** bounded above by  and bounded below by .
* **Image Example:**  is exactly . When determining , you drop all lower-order terms ( and ) and constants () because, at infinity, only the highest power of  () matters.