# N Queens Genetic Algorithm
  
### N queens problem solver via genetic algorithm

#### &nbsp;&nbsp;&nbsp;&nbsp;Made by ..
<br/>&nbsp;&nbsp;&nbsp;&nbsp;Built with [Pygame](https://www.pygame.org/news), an open source game engine
<br> &nbsp;&nbsp;&nbsp;&nbsp;For CPSC 481 (Artificial Intelligence) at [***California State University Fullerton***](http://www.fullerton.edu/)<br><br>&nbsp;&nbsp;&nbsp;&nbsp;Spring 21'

***

## Table of contents
- [N Queens Genetic Algorithm](#n-queens-genetic-algorithm)
  - [Introduction](#introduction)
  - [Approach](#approach)
  - [Analysis](#analysis)
  - [Graphical User Interface](#graphical-user-interface)
  - [Evaluation](#evaluation)
  - [Conclusion](#conclusion)
  - [Demos](#demos)

***

## Introduction

- Genetic Algorithm (GA) is well known to apply the genetic concepts of selection, crossover, and mutation process into solving Computer Science problems. This report aims to focus on how to use GA to solve NQueen problems. NQueen problem is a question of how to put N queens into a board which has size of N*N that no queen attacks any others (highest fitness value)

- To implement this problem into Computer Science programs, using the based class of Problems. Each state of the NQueen movement is a state (N elements), biologically called a chromosome with N genes. To reach the solution, we must find the best state (chromosome) that has the highest fitness value. 
<br><br>

***

## Approach

1. Obtaining and inheriting base class NQueen (search.py, utils.py)
    * Defining fitness value of a state inside NQueen
    * Customize genetic search and GA itself for better result 
    * Other customization if needed <br> <br>
2. Visualization result (background.py, n_queens_game.py, images folder)
    * Preparing graphic user interface background
    * Allowing user to select mutation rate, generation numbers, and N size
    * Loading background interface of options and buttons
    * Viewing real time searching process into interface <br> <br>
3. Advance options (future studies)
    * Showing selection, crossing over, and mutation process each iteration
    * Considering adding music and animation into search process
    * Other advance features: multiple problem solver application
<br><br>

***

## Analysis 

1. Theoretically, how many pairs of queen can be place into a N*N board, without any attack? It is combination of 2, with the size of N queens or (N)(N-1)/2 <br><br>
2. The real fitness of the state is the maximum of non attack queen pairs. But, how many queen pairs attacked each other at a specific state? Recall the heuristic function which is built in NQueen problem class. 

```python
def h(self, node):
"""Return number of conflicting queens for a given node"""
    num_conflicts = 0
    for (r1, c1) in enumerate(node.state):
        for (r2, c2) in enumerate(node.state):
            if (r1, c1) != (r2, c2):
                num_conflicts += self.conflict(r1, c1, r2, c2)
``` 
<br>

3. Therefore, the fitness value at a specific state would be (1)-(2) or


```python
def value(self, state):
    myNode = Node(state)
    return int((self.N) * ((self.N) - 1) / 2 - self.h(myNode))
```
<br>
As students, we reuse code of NQueen class, and base on that, build up one more function called value(self, state). 

Calling a combination of N queens in a board is a state, the purpose of this function is to evaluate the fitness value of that state. The higher this value is, the better we look for the resulting solution.
<br>

4. Reminding that the self.h(mode) is the total conflict of a state, by looking through all chromosomes that are randomly processed by GA’s population, we aim to seek for the smallest as we can, so that the fitness value (above) is the highest. <br><br>

5. Together with the based class of NQueen and our fitness value implemented, let initialize the NQueen problem in main function:

```python
n = int(input("Enter Queen number: "))   #i.e. 5
ngen = 31
pmut = 0.1
#initialize problem
myNQueen = NQueensProblem(n)
print("Beginning!")
genetic_search(myNQueen, ngen, pmut, n)
```

Basically, the value n is the input value of how many queens you want to place in the board. It is input by the user. <br><br>

6. Now, let’s go through the genetic_search(function) with parameter of problem(myNQueen), how generations we will loop through(ngen), what is the rate of mutation (pmut), and the default value of gene numbers inside a state (n)

```python
def genetic_search(problem, ngen, pmut, n):
    s = problem.initial
    states = [problem.result(s, a) for a in problem.actions(s)]
    random.shuffle(states)
    gene_pool = range(0,n)
    genetic_algorithm(states[:n], problem.value, 
                      gene_pool, n * (n - 1) / 2, ngen, pmut)
```

<br>

7. By defining all states before shuffling, and declaring gene_pool(all valid value of a gene), we can start to look through the core algorithm genetic_algorithm
    1. The first step is to define the population (init_population function)
    ```python
    population = init_population(ngen, gene_pool, len(gene_pool))
    ```
    <br>
    
    2. Next step, let looping through each population(loop), select (select function), then crossover (recombine function), and then mutate them (mutate). These processes will be looped for each population (for loop)
    
    ```python
    for i in range(ngen):
        population = [mutate(recombine(*select(2, population, fitness_fn)),
                      gene_pool, pmut) for j in range(len(population))]
    ```
    <br>
    
    3. For easier to keep track the fitness value and chromosomes in each loop, let show those information into the screen (this code part is commented at this moment)
    ```python
    for j in range(len(population)):
        print("---Element",j,":",population[j],'f=',fitness_fn(population[j]))
    ```
    
    * And show the maximum fitness value and the best fit individual of that loop
    ```python
    fittest_individual = max(population, key=fitness_fn)
    fitness_value = fitness_fn(fittest_individual)
    print("Max fitness at loop ", i, " is ", fittest_individual, 
          " with f= ", fitness_value)
    ```
    <br>
    
    4. If we see the fittest individual (its fitness value >= f_thres) then we output that individual to screen and stop looping. For the fittest individual, f_thres = N*(N-1)/2
    ```python
    if fitness_value >= f_thres:
       print("Best fittest found!", fittest_individual, "with f=", fitness_value)
    return None
    ```
    <br>
    
    5. Otherwise, keeping looping without the fitness individual found yet, we end up show up the best fit individual from last loop (this code part is commented at this moment)
    ```python
    print("Not the best but I found :")
    temp = max(population, key=fitness_fn)
    print(temp, "f = ", fitness_fn(temp))
    ```
<br>

***

## Graphical User Interface

- This project uses PyGame, an open source game engine to render both a menu scene and a puzzle scene to the screen as well as properly respond to user input. We developed a dynamic interface that responds to user-inputted changes in N’s value in real time by increasing/decreasing the board size. 


### UI Demo Images

  * **Main Menu Scene** <br>
  ![6](https://user-images.githubusercontent.com/47490318/134795409-5ef18a0b-de7f-4c70-a40d-b02e92fdf5db.png)
    * Note: Pressing start takes the user to the puzzle scene  <br> <br>

  * **Puzzle Scene #1** <br>
  ![5](https://user-images.githubusercontent.com/47490318/134795408-b306ca73-f3d0-4601-90a5-aac176f2a27d.png)
    * Note: These are the default values for N, NGen & Mutation  <br><br>

  * **Puzzle Scene #2** <br>
  ![4](https://user-images.githubusercontent.com/47490318/134795406-72986043-f4a0-406d-94a2-70a54d2c7e22.png) 
    * Note: 4 is the minimum value for N <br><br>
    
  * **Puzzle Scene #3** <br>
  ![3](https://user-images.githubusercontent.com/47490318/134795405-c61a42ce-a6ff-4551-a221-c73bd633fb61.png)
    * Note: 10 is the maximum value for N <br><br>
    
  * **Puzzle Scene #4** <br>
  ![2](https://user-images.githubusercontent.com/47490318/134795403-b24a2317-f18e-4846-9cc5-5fa719591c28.png)
    * Note: After the find solution button is pressed, the following message is printed to the screen prior to a solution being found: <br>*Please wait<br>Current Iteration: x* <br><br>

  * **Puzzle Scene #5** <br>
  ![1](https://user-images.githubusercontent.com/47490318/134795381-5b08ebb2-6230-44e5-adf2-06f6cafac74f.png)
    * Note: After a solution is found the following message  is printed to the screen: <br>*Solution: [ v1, v2, v3, .., vn ]<br>Total Iterations: k*

<br>

***

## Evaluation

- Recall that it is impossible to seek a solution at N from 1 to 3. Hence, the conductors measure application performance with N starting at 4:
- Within 10 runtimes per N value, the average time, iterations, time per iteration result are:

N | Average overall time(s) | Iterations (#) | Average time/iteration(s)
------------ | ------------ | ------------ | ------------
4 | 1 - 3 | 3 - 10 | 0.2 - 0.4
5 | 5 - 10 | 10 - 30 | 0.3 - 1
6 | 20 - 40 | 1000 - 2500 | 0.2 - 0.3
7 | 120 - 480 | 2000 - 4500 | 0.2 - 0.4
8, 9 | 600 - 1200 | 4000 - 6000 | 0.5 - 0.9


<br>

***

## Conclusion

- There are some remaining issue needs to work on here:

1. Since the selection, crossover, and mutation are random, there is no guarantee that GA will precisely find out the fittest individual with the highest value with no conflict at all.
    * Suggestion: Customize the loop, not end by generation number but until seek out for the highest fitness of N chromosome’s size. The downside of this idea is long time committed when running code with big value of N, start at 6

2. Attempting to implement the while loop with stop looping condition of seeking for the fittest individual seems ambiguous in many cases, especially if N is big and it strongly depends on every runtime compile.
    * Suggest using a better computational engine instead. High cost of using this way

3. Duplicate during GA process and showing the best fit individuals per generation
    * Suggest to customize the crossover step of GA program in two main options, either by crossovering at the mid of the chromosome, or by crossovering at 2 differently random points of the chromosome.

4. In conclusion, the GA is a good algorithm, in the sense of discovering solutions for tough and required resource problems like N queen attackers. This project approaches the problem in terms of biologically solver of genetic concepts, brings up opening topics for further application and improves many other hot Computer Science topics in the future.


<br>

***

### Demos
##### Click to watch demo on YouTube (Readme file doesn't allow video playback)
[![ezgif com-optimize](https://github.com/dguido1/n-queens-gen-algo/blob/main/n-queens-gen-algo/demo/yt_ss.png)](https://youtu.be/tw97i1rLPtM)

##### N queens solution with N = 6 found in only 2 iterations!
![ezgif com-optimize](https://github.com/dguido1/n-queens-gen-algo/blob/main/n-queens-gen-algo/demo/n-queen-demo02.gif)

##### N queens solution with N = 4 found in 4 iterations!
![111](https://user-images.githubusercontent.com/47490318/134796233-9202270a-97db-420a-9044-362d4f5955bd.png)

##### N queens solution with N = 8 found in 138 iterations!
![222](https://user-images.githubusercontent.com/47490318/134796232-65e332e7-74f5-497c-b191-28935a443ec7.png)

<br>

***

<br/>
Thanks for reading!<br/><br/>
 
If you like what you see give this repo  
a star and share it with your friends.

Your support is greatly appreciated!<br/><br/>

<br/><br/>

