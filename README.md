# Problems solved

Tree:
	Create Binary Tree - insert, inorder, preorder, postorder
	BST in sorted order
	Check Binary tree or not
	Print all the nodes which are at k distance from root.
	Height of a tree
	Level order
	Lowest common ancestor
	Optimal search tree
	print root to leaf paths
	print anscestors
	root to leaf sum equal
	same tree or not
	search bst
	subtree
	top view
	tree nodes
	vertical order traversal

Linked list:
	Single linked list
	Single linked list check cycle
	Insert Head
	Insert Node in btw
	Insert node at last
	Del Node
	remove duplicates
	print reverse
	nth to last node
	merge list
	linked list reversal
	get node value
	find merge point of list
	compare list
	Double linked list
	Insert Node in DLL
	Revese Double LL

Stacks and Queues:
	- Parentheses balance check
	- For given lists (h1,h2,h3), find the maximum possible height of the stacks such that all of the stacks are exactly the same height.
	- Maximum number of integers that can be removed from the two stacks without the sum of elements in A and B not exceeding x.
	- Queue using two stacks
	- Rearrange array such that even index elements are smaller and odd index elements are greater

Array:

    - Left rotation of array
	- Sparse Arrays (There is a collection of input strings and a collection of query strings. For each query string, determine how many times it occurs in the list of input strings.)

DP:
	- Fibnocci series using DP
	- KnapSack
	- Longest common subsequence
	- Longest common substring
	- Longest planidromic sequence.
	- Reverse fibnocci
	- longest increasing suquence

Sorting:

	- Bubble sorting
	- Bubble sorting selection.
	- Insertion sort
	- Odd even string sort
	- Sort by digit
	- Sort the inner content of sentance.
	- Merge two sorted arrays
	- Merge Sort

General:

1. 	isAnagram or not
2. 	Char search in array
3. 	Collinear or not
4. 	Data reverse
5. 	Data persistance
6. 	Degree (Max Sequential repeated count)
7. 	Delete occurrences of an element if it occurs more than n times
8. 	Print diamond
9. 	Find given number is prime or even (if even print divisors)
10. Nonlocal: Introduces names from the enclosing namespace into the local namespace
11. Filter repeated elements
12. Filter Unique List
13. Function factory
14. Grading of students (If the difference between the  grade and the next multiple of  5 is less than 3, round  up to the next multiple of 5.
If the value of grade is less than 38, no rounding occurs as the result will still be a failing grade.)
15. Identical pair (Given an array of n elements. The task is to count the total number of indices (i, j)
such that arr[i] = arr[j] and i != j)
16. Interchange string(vijay=yijayv)
17. Possible IP
18. When two kangroos are running which started at two diff points and moves at diff rates, find the meeting point of two kangroos
19. Form largest number for given list of integers
20. Largest 5 digit number for given integer
21. Given a list of integers, find the largest product you could make from 3 integers in the list
22. In arry of arrys, find the len of missing array
23. longest repetation of char in sequential order
24. Matrix
25. Median.
26. Move zeros to right
27. Palindrom with in the string
28. Fibnocci using generator
29. Permieter square in rectangle
30. Permutations of given string
31. Print possible words for given chars (input = ['goo', 'bat', 'me', 'eat', 'goal', 'boy', 'run'], charSet = ['e', 'o', 'b', 'a', 'm', 'g', 'l'])
32. Print prime between numbers
33. String reverse by index
34. Remove duplicate characters in a given string keeping only the first occurrences.
35. Square root of number
36. Decroator example
37. Use of func tool
38. Multi decorator
39. Reversed args sample: pow 5 2 cmp 15 3 => pow 2 5, cmp 3 15
40. Multithreading
41. Multithread_condition_availability
42. Class
43. Inheritance
44. Find the smallest positive integer value that cannot be represented as sum of any subset of a given array
45. Check if a string has all characters with same frequency with one variation allowed





This project contains following projects:

Pyvmomi scripts:

    Deploy OVA
    power cycles of VM
    Export OVA

Django App:

    To create sample web url using django

Robot Framework designs:
    Web and REST, automation framewework designs
    Ozone robot framework

SSH project:

    SSH utility using paramiko library to execute commands in remote machine, upload files to remote machine

POC on Salt cloud:

    Designing of cloud driver using Salt stack (Salt cloud)

CI/CD:

    Jenkins pipeline with groovy scripting for end to end automation.

Devops:

    Sample dockerfile for CI/CD
Common:

   Dict to yaml conversion, getting value from yaml file and unit test cases.


Training:
    Code wars, hackerrank, codility, geek for geeks solved python scripts.


### Software Requirments

    Python 3.5 or 2.7


### Python Virtual Environment

1. Create Python virtual environment
    
        $ virtualenv mw_venv -p python3
    
2. Activate virtual environment 
    
        $ source mw_venv/bin/activate
    
3. Deactivate virtual environment
    
        $ deactivate
    

### Install requirements

* Install python project dependencies for dev environment
   
        $ pip3 install -r requirements/local.txt

    

### Run Flake8 before commit (run on the root of the project)

        $ flake8