# AI Squid Game: Trap! (Fall 2021)

The final coding challenge for COMS W4701 - Artificial Intelligence, Columbia University.

Written by: Tom Cohen, Adam Lin, Gustave Ducrest

Professor : Ansaf Salleb-Aouissi

## Outline (for internal use)

* Description and hyping of Game (Rules, ..)
* Coding (Minimax Algorithm, Alpha-Beta Pruning)
* Restrictions
* Logistics
* Grading
* Q&A
* Resources

## Preface and Learning Objectives

In this (super exciting) project, we will use Adverserial AI to defeat a strategic opponent at a mind game. 

### Learning Objective

By the end of this project you will have learned:
1. **Minimax, ExpectiMinimax, and Alpha-Beta Pruning**
2. Inventive **Heuristics**!
3. Adversarial Seach under **Time Constraints**
4. How to **collaborate effectively**
5. How to test your Player AI

## 1. Game Description

It is you against another contestant, and only one will survive! 

The players are placed on a gridded space and supplied with small traps which they can throw anywhere on the grid.

The game is simple: At each turn, a player has 5 seconds to act - move and throw a trap - lest the notorious Squid Game doll will shoot them down. 

In order to win the game, you would need to trap the opponent, i.e., surround them with traps from all sides, so that cannot move anywhere (meaning the doll will take care of them), before they do that to you!



### 1.1 Organization
The game is organized as a two-player game on a 7x7 board space. Every turn, a player first **moves** (to make sure they wouldn't die) and then **throws a trap** somewhere on the board. 

![game1](https://user-images.githubusercontent.com/55168908/142688490-83efbc0d-064d-4d14-9546-144e694eecb6.png)


### 1.2 Movement

Each turn, a player can move one step in any possible direction, diagonals included (e.g., like King in chess), *so long as there is no trap placed in that cell and that it is within the borders of the grid*

no traps             |  with traps
:-------------------------:|:-------------------------:
![image](https://user-images.githubusercontent.com/55168908/142576384-3e3c6bec-9915-43ee-9b14-28c75e82ebc4.png)  |  ![image](https://user-images.githubusercontent.com/55168908/142577318-33321ee1-2afe-432f-ad75-967f89442ae7.png)


### 1.3 Throwing a Trap

Unlike movement, a trap can be thrown to *anywhere in the board*, with the exception of the opponents location - again, we want them alive! - and the player's location. Note that throwing a trap on top of another trap is possible but useless.

**However,** sadly, we are not on the olympic throwing team, and our aiming abilities deteriorate with distance, such that there is an increasing chance the trap will land on any of its neighboring cells. In fact, the chance *p* that it will land precisely on the cell we want is given as: 

![image](https://user-images.githubusercontent.com/55168908/142582036-d19b98ad-56e0-404a-8d07-cca66f4f54a7.png). 

![image](https://user-images.githubusercontent.com/55168908/142582525-4f5b2170-a177-4233-80c4-755542f69893.png)

The *n* surrounding cells divide the remainder equally between them, that is: 

![image](https://user-images.githubusercontent.com/55168908/142585339-93cddc84-ba13-4880-88b3-8070e772a46a.png)

![image](https://user-images.githubusercontent.com/55168908/142583267-3231710e-d3ad-40c6-8452-0f38da4e324c.png)



Example:

Target             |  Probabilities of trap placement
:-------------------------:|:-------------------------:
![trap1](https://user-images.githubusercontent.com/55168908/142584513-d4e70925-a2ad-436d-895c-e4cac90fbbcf.png)| ![trap2](https://user-images.githubusercontent.com/55168908/142584586-d40bca87-99e7-4b12-b761-2f3eb83190d5.png)


### 1.4 Game Over?

To win, you must "Trap" you opponent so that they could not possibly move in any direction, while you still can! Examples:

Example 1 (Win)             |  Example 2 (Loss)
:-------------------------:|:-------------------------:
![win1](https://user-images.githubusercontent.com/55168908/142578872-d27ef016-a3e7-427b-8e33-26f84b2172f0.png) | ![lose1](https://user-images.githubusercontent.com/55168908/142579019-c88b20a1-876e-427c-9f24-b79bbba5f9ff.png)


In example 1: the player can still move down or right, whereas the opponent has no valid moves.

In example 2: the player cannot move but the opponent still has a diagnoal move. 


## 2. What to Code

Two thoughtful actions are performed at each turn: One to maximize the chance of survival (moving), and the other to maximize the chance of winning the game (Trapping). So accordingly, we have two different Adversarial Search problems to compute at each turn!

### 2.1 The Search Algorithm
For **each** of the search problems, you will have to implement the ExpectiMinimax algorithm with Alpha-Beta Pruning!

### 2.2 Expecti--What Now?
Expectiminimax (indeed a mouthful) is a simple extension of the famous Minimax algorithm that we covered in class (Adversarial Search lecture)! 
The only difference is that in the expectiminimax, we introduce an intermediate **Chance Node** that accounts for chance and uncertainty. As we have previously established, throwing the trap is not always accurate, so we have to take into account potential consequences as we navigate the game. The modification is demonstrated in the comparison below:


Minimax             |  ExpectiMinimax
:-------------------------:|:-------------------------:
<img width="347" alt="minimax" src="https://user-images.githubusercontent.com/55168908/142590520-a3e29401-726a-4585-9579-c1dd47aee108.png">| <img width="431" alt="expecti" src="https://user-images.githubusercontent.com/55168908/142590403-aec560c3-1ede-4b49-81f4-57942bbbd990.png">

As you can see, you are now trying to maximize the opponents moves, given the *chance* of them happening. For example, if we are to throw a trap and want to maximize our chance of winning, our tree will have a chance node with value *p* as well as *n* nodes with values *(1-p)/n* (see equations in 1.3: Throwing a Trap).
The rest is the same! 

Note that the player is now maximizing their *Expected Utility* in every move (if that sounds not-necessarily-optimal to you, you aren't wrong!).

### Heuristics!

Since the Search Space here is HUGE(!), you will need to come up with useful heuristics for both *restricting the search space* as well as *evaluating the utility of a move.*

A few basic ones you can start with:

- **Improved Score (IS):** the difference between the current number of moves Player (You) can make and the current number of moves the opponent can make.
- **Aggressive Improved Score (AIS):** Same as IS only with a 2:1 ratio applied to Opponent's moves.
- **One Cell Lookahead Score (OCLS):** The difference between the Player's sum of possible moves looking one step ahead and the Opponent's sum of possible moves looking one step ahead

Of course, you may choose to combine multiple heuristics and come up with your own heuristics!

### Hmm that's a lot. Where Do We Start?

Fear not! Here's a very good recipe:

1. Start with making a random move under five seconds.
2. Code basic heuristics
3. Implement a simple Minimax. Observe improvements.
4. (Save current Player and make them the Opponent from now on!)
5. Add Alpha-beta pruning. Observe improvements!
6. Extend minimax to Expectiminimax
7. Code advanced heuristics
8. DONE.

## Grading

The competition is designed so that **all groups will be able to get a good grade regardless of their placement in the competition**. We will test your code against players of three difficulty levels: Easy, Medium, and Hard (still very doable as long as you implement everything). Those will account for at least 85% of your grade on the project. After evaluating all teams against our players, we will create a tournament where you will compete against other groups and will be rewarded more points based on the number of groups you defeat!

## Submission 

Please submit the entire folder with all the files. The name of the folder must be the UNIs of all groups members, concatenated with underscores. For example, tc1234_gd5678. Additionally, you *MUST* submit a text file, named exactly as the folder (e.g., tc1234_gd5678.txt) describing each member's contribution to the project. We may take that into account when computing individual grades in the case that one member contributed significantly more than the other(s)!

**Note that we will only test the PlayerAI.py file so make sure all necessary functions are there!**

## * Q&A

#### What are we allowed to use?** 
You are definitely allowed to import commont libraries (e.g., numpy, itertools, etc.) as well as use/modify functions provided as part of the source code (e.g., the probabilistic trap throw). HOWEVER, you will need to implement all the Search Algorithms and Heuristics yourselves! 

#### How should we divide the work?

- **A group of 2:** We suggest dividing the Expectiminimax algorithms - one group member should code the Move Expectiminimax and its accompanying heuristics and the other should code the Throw expectiminimax and its heuristics. Additionally each member should code one Opponent player to play against.
- **A groupd of 3:** We suggest one group member responsible for the Move Expectiminimax, another for the Throw Expectiminimax, and the third for both heuristics as well as coding AI Opponents to test the group's code against.

